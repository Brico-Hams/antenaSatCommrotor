// PortableSatLite - ESP32 rotor controller: Wi-Fi AP + web UI, SGP4 tracking, GNSS, tilt/heading compensation, 2 steppers.
// Written against the Arduino-ESP32 2.x/3.x core. NOT compiled in the authoring environment; the maths it calls is (tests/).
#include <Arduino.h>
#include <WiFi.h>
#include <WebServer.h>
#include <HTTPClient.h>
#include <WiFiClientSecure.h>
#include <LittleFS.h>
#include <Preferences.h>
#include <Wire.h>
#include <TinyGPSPlus.h>
#include <FastAccelStepper.h>
#include "config.h"
#include "satcore.h"
#include "Sgp4.h"
#include "tracker.h"
#include "tle.h"

// ---------------- state ----------------
static WebServer server(80);
static Preferences prefs;
static TinyGPSPlus gps;
static FastAccelStepperEngine engine;
static FastAccelStepper *azS = nullptr, *elS = nullptr;

struct Catalog { const char *id; const char *alias; double dl, ul; } ;
static const char *ALIASES[8]; static String CAT_ID[8]; static double CAT_DL[8], CAT_UL[8]; static int N_CAT = 0;
static TleEntry tles[8]; static int n_tles = 0;
static Tracker trk[8];
static PassInfo passes[8][6]; static int n_passes[8];
static volatile bool passes_dirty = true;

static double site_lat = 38.0, site_lon = -1.3, site_alt = 100.0; static bool site_manual = true;
static double decl_deg = 0.0;                 // magnetic declination, east positive (NOAA). Set in the web UI.
static double north_manual = NAN;             // if set: true azimuth of the rotor zero direction (deg) overrides the compass
static satcore::V3 mag_min{1e9,1e9,1e9}, mag_max{-1e9,-1e9,-1e9}, mag_off{0,0,0}; static bool cal_running = false;
static satcore::Frame frame{{0,0,0},{0,0,0},{0,0,0}, false};
static double roll_deg = 0, pitch_deg = 0, heading_true = NAN;
static long unix_offset = 0; static bool have_time = false;       // unix = millis()/1000 + unix_offset (GNSS or phone)
static int tracking = -1; static bool flip_allowed = true;
static double tgt_az = 0, tgt_el = 0, rot_az_cmd = 0, rot_el_cmd = 0, dop_rx = 0, dop_tx = 0, rr_now = 0, sat_az = 0, sat_el = 0;
static String sta_ssid, sta_pass; static String ap_ssid;
static String api_key;                        // required for API calls arriving over the home Wi-Fi (STA); the AP side stays open

static unsigned long now_unix() { return (unsigned long)(millis() / 1000UL) + unix_offset; }
static double az_now() { return azS ? azS->getCurrentPosition() / STEPS_PER_DEG : 0; }
static double el_now() { return elS ? elS->getCurrentPosition() / STEPS_PER_DEG : 0; }

// ---------------- sensors (raw I2C, no libraries) ----------------
static void i2c_write(TwoWire &w, uint8_t a, uint8_t r, uint8_t v) { w.beginTransmission(a); w.write(r); w.write(v); w.endTransmission(); }
static bool i2c_read(TwoWire &w, uint8_t a, uint8_t r, uint8_t *buf, int n) {
  w.beginTransmission(a); w.write(r); if (w.endTransmission(false) != 0) return false;
  if (w.requestFrom((int)a, n) != n) return false; for (int i = 0; i < n; i++) buf[i] = w.read(); return true;
}
// Sensor axes -> body frame (x forward = rotor zero azimuth, y right, z down). Edit the sign/permutation to match how the pod is glued to the base.
static satcore::V3 to_body(double sx, double sy, double sz) { return {sx, sy, sz}; }
static bool read_imu(satcore::V3 &up) {
  uint8_t b[6]; if (!i2c_read(Wire, 0x68, 0x3B, b, 6)) return false;       // MPU6050 accel, +-2 g (16384 LSB/g); at rest it reads +1 g UP
  double ax = (int16_t)((b[0] << 8) | b[1]), ay = (int16_t)((b[2] << 8) | b[3]), az = (int16_t)((b[4] << 8) | b[5]);
  up = satcore::unit(to_body(ax, ay, az)); return true;
}
static bool read_mag(satcore::V3 &m) {
  uint8_t b[6]; if (!i2c_read(Wire, 0x0D, 0x00, b, 6)) return false;       // QMC5883L little-endian X,Y,Z
  double x = (int16_t)(b[0] | (b[1] << 8)), y = (int16_t)(b[2] | (b[3] << 8)), z = (int16_t)(b[4] | (b[5] << 8));
  satcore::V3 v = to_body(x, y, z);
  if (cal_running) { mag_min = {fmin(mag_min.x, v.x), fmin(mag_min.y, v.y), fmin(mag_min.z, v.z)}; mag_max = {fmax(mag_max.x, v.x), fmax(mag_max.y, v.y), fmax(mag_max.z, v.z)}; }
  m = {v.x - mag_off.x, v.y - mag_off.y, v.z - mag_off.z}; return true;
}
static void update_orientation() {
  satcore::V3 up, m;
  if (!read_imu(up)) { if (isnan(north_manual)) return; up = {0, 0, -1}; }   // fixed install without MPU6050: assume a levelled base
  roll_deg = atan2(up.y, up.z) * satcore::R2D; pitch_deg = atan2(-up.x, hypot(up.y, up.z)) * satcore::R2D;
  if (!isnan(north_manual)) {
    frame = satcore::frame_from_heading(up, north_manual);        // manual / sun-aligned north: rotor zero points to this true azimuth
  } else if (read_mag(m)) frame = satcore::frame_from_sensors(up, m, decl_deg);
  if (frame.valid) { double a, e; satcore::rotor_to_target(frame, 0, 0, a, e); heading_true = a; }
}

// ---------------- time / GNSS ----------------
static void poll_gps() {
  while (Serial2.available()) gps.encode(Serial2.read());
  if (gps.location.isValid() && gps.location.age() < 5000 && !site_manual) { site_lat = gps.location.lat(); site_lon = gps.location.lng(); site_alt = gps.altitude.meters(); }
  if (gps.date.isValid() && gps.time.isValid() && gps.time.age() < 3000) {
    int y = gps.date.year(), mo = gps.date.month(), d = gps.date.day();
    long days = 0; for (int k = 1970; k < y; k++) days += ((k % 4 == 0 && k % 100 != 0) || k % 400 == 0) ? 366 : 365;
    static const int dm[] = {31,28,31,30,31,30,31,31,30,31,30,31}; for (int k = 1; k < mo; k++) days += dm[k-1] + ((k == 2 && ((y % 4 == 0 && y % 100 != 0) || y % 400 == 0)) ? 1 : 0);
    days += d - 1; unsigned long u = days * 86400UL + gps.time.hour() * 3600UL + gps.time.minute() * 60UL + gps.time.second();
    unix_offset = (long)u - (long)(millis() / 1000UL); have_time = true;
  }
}

// ---------------- TLE / passes ----------------
static void load_catalog() {
  File f = LittleFS.open("/satellites.json", "r"); if (!f) return; String s = f.readString(); f.close();
  static String alias_store[8]; int pos = 0; N_CAT = 0;
  while (N_CAT < 8) {   // minimal field scanner for our own fixed-format file
    int a = s.indexOf("\"id\"", pos); if (a < 0) break; int b = s.indexOf('"', s.indexOf(':', a) + 1) + 1; CAT_ID[N_CAT] = s.substring(b, s.indexOf('"', b));
    int c = s.indexOf("\"alias\"", a); int d = s.indexOf('"', s.indexOf(':', c) + 1) + 1; alias_store[N_CAT] = s.substring(d, s.indexOf('"', d)); ALIASES[N_CAT] = alias_store[N_CAT].c_str();
    int e = s.indexOf("\"dl\"", a); CAT_DL[N_CAT] = s.substring(s.indexOf(':', e) + 1, s.indexOf(',', e)).toDouble();
    int g = s.indexOf("\"ul\"", a); CAT_UL[N_CAT] = s.substring(s.indexOf(':', g) + 1, s.indexOf(',', g)).toDouble();
    pos = g + 4; N_CAT++;
  }
}
static void load_tles() {
  n_tles = 0; File f = LittleFS.open("/tle.txt", "r"); if (!f) return; String s = f.readString(); f.close();
  tle::parse(s.c_str(), ALIASES, N_CAT, tles, 8, n_tles);
  for (int i = 0; i < 8; i++) trk[i].loaded = false;
  for (int i = 0; i < n_tles; i++) trk[tles[i].cat].load(tles[i].name, tles[i].l1, tles[i].l2, site_lat, site_lon, site_alt);
  passes_dirty = true;
}
static bool http_get(const String &url, String &out) {
  HTTPClient http; WiFiClientSecure sec; sec.setInsecure();     // TLE data is public and checksummed; see ADR-012 for the integrity note
  if (url.startsWith("https")) http.begin(sec, url); else http.begin(url);
  http.setFollowRedirects(HTTPC_STRICT_FOLLOW_REDIRECTS); http.setTimeout(15000);
  int code = http.GET(); if (code != 200) { http.end(); return false; } out = http.getString(); http.end(); return true;
}
static String update_tle_online() {
  static const char *URLS[] = {"http://www.celestrak.org/NORAD/elements/gp.php?GROUP=amateur&FORMAT=tle", "http://www.amsat.org/tle/current/dailytle.txt", "http://tle.pe0sat.nl/kepler/mykepler.txt"};
  if (WiFi.status() != WL_CONNECTED) return "STA not connected: set a Wi-Fi (phone hotspot) in Settings";
  String all, msg; for (auto u : URLS) { String t; bool ok = http_get(u, t); msg += String(ok ? "OK " : "FAIL ") + u + "\n"; if (ok) all += t + "\n"; }
  if (all.length() > 100) { File f = LittleFS.open("/tle.txt", "w"); f.print(all); f.close(); load_tles(); }
  return msg;
}
static void passes_task(void *) {
  for (;;) {
    if (passes_dirty && have_time) {
      passes_dirty = false; unsigned long t0 = now_unix();
      for (int i = 0; i < N_CAT; i++) { n_passes[i] = 0; if (trk[i].loaded) { trk[i].sat.site(site_lat, site_lon, site_alt); n_passes[i] = trk[i].find_passes(t0, 24.0, 0.0, 10.0, passes[i], 6); } vTaskDelay(1); }
    }
    vTaskDelay(pdMS_TO_TICKS(1000));
    static unsigned long last = 0; if (millis() - last > 600000) { last = millis(); passes_dirty = true; }
  }
}

// ---------------- motion ----------------
static void move_to_rotor(double az, double el) {
  az = constrain(az, AZ_MIN_DEG, AZ_MAX_DEG); el = constrain(el, EL_MIN_DEG, EL_MAX_DEG);
  rot_az_cmd = az; rot_el_cmd = el; if (azS) azS->moveTo((int32_t)(az * STEPS_PER_DEG)); if (elS) elS->moveTo((int32_t)(el * STEPS_PER_DEG));
}
static void stop_all() { tracking = -1; if (azS) azS->stopMove(); if (elS) elS->stopMove(); }
static bool limit_hit(int pin) { return digitalRead(pin) == HIGH; }       // NC switch: closed to GND at rest (LOW); HIGH = pressed or wire broken
static void home_axis(FastAccelStepper *s, int pin, int dir) {
  s->setSpeedInHz(STEPS_PER_DEG * 3); s->setAcceleration(STEPS_PER_DEG * 10); unsigned long t = millis();
  while (!limit_hit(pin) && millis() - t < 90000) { if (dir > 0) s->runForward(); else s->runBackward(); delay(5); }
  s->forceStopAndNewPosition(0);
}
static void tracking_step() {
  if (tracking < 0 || !trk[tracking].loaded || !have_time || !frame.valid) return;
  Sample s; if (!trk[tracking].sample(now_unix(), s)) return; sat_az = s.az; sat_el = s.el; rr_now = s.range_rate_kms;
  dop_rx = satcore::doppler_rx(CAT_DL[tracking] * 1e6, s.range_rate_kms); dop_tx = satcore::doppler_tx(CAT_UL[tracking] * 1e6, s.range_rate_kms);
  if (s.el < 0) { return; }                                                 // below the horizon: hold position
  double az_r, el_r; satcore::target_to_rotor(frame, s.az, s.el, az_r, el_r);
  tgt_az = az_r; tgt_el = el_r;
  double cur = az_now();
  if (flip_allowed && el_r > 80) { satcore::flip(az_r, el_r, az_r, el_r); }   // simple over-the-top policy near the zenith of the rotor frame
  move_to_rotor(satcore::unwrap_az(az_r, cur, AZ_MAX_DEG), el_r);
}

// ---------------- web API ----------------
static bool from_ap() { IPAddress c = server.client().remoteIP(), a = WiFi.softAPIP(); return c[0] == a[0] && c[1] == a[1] && c[2] == a[2]; }
static bool authorized() {
  if (from_ap()) return true;
  if (api_key.length() >= 16 && server.arg("key") == api_key) return true;
  server.send(403, "text/plain", "API key required from the home network (set it from the SatLite AP: /api/key)"); return false;
}
static void send_json(const String &s) { server.sendHeader("Cache-Control", "no-store"); server.send(200, "application/json", s); }
static void api_state() {
  if (!authorized()) return;
  String j = "{\"ssid\":\"" + ap_ssid + "\",";
  j += "\"unix\":" + String(now_unix()) + ",\"have_time\":" + String(have_time) + ",\"gps_fix\":" + String(gps.location.isValid() && gps.location.age() < 5000) + ",\"sats\":" + String(gps.satellites.isValid() ? gps.satellites.value() : 0);
  j += ",\"lat\":" + String(site_lat, 5) + ",\"lon\":" + String(site_lon, 5) + ",\"alt\":" + String(site_alt, 0) + ",\"site_manual\":" + String(site_manual);
  j += ",\"roll\":" + String(roll_deg, 1) + ",\"pitch\":" + String(pitch_deg, 1) + ",\"heading\":" + (isnan(heading_true) ? String("null") : String(heading_true, 1)) + ",\"decl\":" + String(decl_deg, 1) + ",\"north_manual\":" + (isnan(north_manual) ? String("null") : String(north_manual, 1)) + ",\"frame_ok\":" + String(frame.valid);
  j += ",\"az\":" + String(az_now(), 2) + ",\"el\":" + String(el_now(), 2) + ",\"tgt_az\":" + String(tgt_az, 1) + ",\"tgt_el\":" + String(tgt_el, 1);
  j += ",\"tracking\":" + String(tracking) + ",\"sat_az\":" + String(sat_az, 1) + ",\"sat_el\":" + String(sat_el, 1) + ",\"rr\":" + String(rr_now, 3) + ",\"dop_rx\":" + String(dop_rx, 0) + ",\"dop_tx\":" + String(dop_tx, 0) + ",\"cal\":" + String(cal_running);
  j += ",\"sta\":" + String(WiFi.status() == WL_CONNECTED) + ",\"tle_count\":" + String(n_tles) + ",\"catalog\":[";
  for (int i = 0; i < N_CAT; i++) j += String(i ? "," : "") + "{\"i\":" + i + ",\"id\":\"" + CAT_ID[i] + "\",\"dl\":" + String(CAT_DL[i], 3) + ",\"ul\":" + String(CAT_UL[i], 3) + ",\"have_tle\":" + String(trk[i].loaded) + "}";
  j += "]}"; send_json(j);
}
static void api_passes() {
  if (!authorized()) return;
  String j = "["; bool first = true;
  for (int i = 0; i < N_CAT; i++) for (int k = 0; k < n_passes[i]; k++) { PassInfo &p = passes[i][k];
    j += String(first ? "" : ",") + "{\"sat\":" + i + ",\"id\":\"" + CAT_ID[i] + "\",\"aos\":" + p.aos + ",\"tca\":" + p.tca + ",\"los\":" + p.los + ",\"max_el\":" + String(p.max_el, 1) + ",\"az_aos\":" + String(p.az_aos, 0) + ",\"az_los\":" + String(p.az_los, 0) + "}"; first = false; }
  j += "]"; send_json(j);
}
static void api_cmd() {
  if (!authorized()) return;
  String c = server.uri();
  if (c == "/api/track") { int i = server.arg("sat").toInt(); if (i >= 0 && i < N_CAT && trk[i].loaded) { tracking = i; send_json("{\"ok\":1}"); } else server.send(400, "text/plain", "no TLE for that satellite"); }
  else if (c == "/api/stop") { stop_all(); send_json("{\"ok\":1}"); }
  else if (c == "/api/goto") { tracking = -1; move_to_rotor(server.arg("az").toFloat(), server.arg("el").toFloat()); send_json("{\"ok\":1}"); }
  else if (c == "/api/goto_true") { tracking = -1; double a, e; if (!frame.valid) { server.send(409, "text/plain", "north reference missing"); return; } satcore::target_to_rotor(frame, server.arg("az").toFloat(), server.arg("el").toFloat(), a, e); move_to_rotor(satcore::unwrap_az(a, az_now(), AZ_MAX_DEG), e); send_json("{\"ok\":1}"); }
  else if (c == "/api/home") { tracking = -1; home_axis(elS, PIN_EL_LIM, -1); home_axis(azS, PIN_AZ_LIM, -1); send_json("{\"ok\":1}"); }
  else if (c == "/api/location") { site_lat = server.arg("lat").toFloat(); site_lon = server.arg("lon").toFloat(); site_alt = server.arg("alt").toFloat(); site_manual = true; prefs.putDouble("lat", site_lat); prefs.putDouble("lon", site_lon); prefs.putDouble("alt", site_alt); load_tles(); send_json("{\"ok\":1}"); }
  else if (c == "/api/location_gps") { site_manual = false; send_json("{\"ok\":1}"); }
  else if (c == "/api/decl") { decl_deg = server.arg("deg").toFloat(); prefs.putDouble("decl", decl_deg); send_json("{\"ok\":1}"); }
  else if (c == "/api/north") { if (server.arg("deg") == "auto") north_manual = NAN; else north_manual = server.arg("deg").toFloat(); prefs.putDouble("north", north_manual); send_json("{\"ok\":1}"); }
  else if (c == "/api/key") { String k = server.arg("key"); if (!from_ap()) server.send(403, "text/plain", "set the key from the SatLite AP"); else if (k.length() < 16) server.send(400, "text/plain", "key: 16 characters or more"); else { api_key = k; prefs.putString("apikey", api_key); send_json("{\"ok\":1}"); } }
  else if (c == "/api/time") { unix_offset = (long)server.arg("unix").toInt() - (long)(millis() / 1000UL); have_time = true; passes_dirty = true; send_json("{\"ok\":1}"); }
  else if (c == "/api/compass_cal") { if (server.arg("op") == "start") { mag_min = {1e9,1e9,1e9}; mag_max = {-1e9,-1e9,-1e9}; cal_running = true; } else { cal_running = false; mag_off = {(mag_min.x + mag_max.x) / 2, (mag_min.y + mag_max.y) / 2, (mag_min.z + mag_max.z) / 2}; prefs.putBytes("magoff", &mag_off, sizeof(mag_off)); } send_json("{\"ok\":1}"); }
  else if (c == "/api/wifi") { sta_ssid = server.arg("ssid"); sta_pass = server.arg("pass"); prefs.putString("ssid", sta_ssid); prefs.putString("spass", sta_pass); WiFi.begin(sta_ssid.c_str(), sta_pass.c_str()); send_json("{\"ok\":1}"); }
  else if (c == "/api/tle_update") { server.send(200, "text/plain", update_tle_online()); }
  else if (c == "/api/tle_upload") { File f = LittleFS.open("/tle.txt", "w"); f.print(server.arg("plain")); f.close(); load_tles(); send_json("{\"ok\":1}"); }
}
static void serve_index() { File f = LittleFS.open("/index.html", "r"); if (!f) { server.send(500, "text/plain", "upload filesystem image (pio run -t uploadfs)"); return; } server.streamFile(f, "text/html"); f.close(); }

void setup() {
  Serial.begin(115200); LittleFS.begin(true); prefs.begin("satlite", false);
  site_lat = prefs.getDouble("lat", 38.0); site_lon = prefs.getDouble("lon", -1.3); site_alt = prefs.getDouble("alt", 100); decl_deg = prefs.getDouble("decl", 0);
  if (prefs.getBytesLength("magoff") == sizeof(mag_off)) prefs.getBytes("magoff", &mag_off, sizeof(mag_off));
  sta_ssid = prefs.getString("ssid", ""); sta_pass = prefs.getString("spass", "");
  north_manual = prefs.getDouble("north", NAN); api_key = prefs.getString("apikey", "");
  Wire.begin(PIN_SDA0, PIN_SCL0, 400000); Wire1.begin(PIN_SDA1, PIN_SCL1, 400000);
  i2c_write(Wire, 0x68, 0x6B, 0x00); i2c_write(Wire, 0x0D, 0x0B, 0x01); i2c_write(Wire, 0x0D, 0x09, 0x1D);   // MPU6050 wake; QMC5883L 200 Hz continuous
  Serial2.begin(9600, SERIAL_8N1, PIN_GPS_RX, PIN_GPS_TX);
  pinMode(PIN_AZ_LIM, INPUT_PULLUP); pinMode(PIN_EL_LIM, INPUT_PULLUP);
  engine.init(); azS = engine.stepperConnectToPin(PIN_AZ_STEP); elS = engine.stepperConnectToPin(PIN_EL_STEP);
  if (azS) { azS->setDirectionPin(PIN_AZ_DIR); azS->setEnablePin(PIN_EN, true); azS->setAutoEnable(true); azS->setSpeedInHz(STEPS_PER_DEG * MAX_SPEED_DEG_S); azS->setAcceleration(STEPS_PER_DEG * ACCEL_DEG_S2); }
  if (elS) { elS->setDirectionPin(PIN_EL_DIR); elS->setEnablePin(PIN_EN, true); elS->setAutoEnable(true); elS->setSpeedInHz(STEPS_PER_DEG * MAX_SPEED_DEG_S); elS->setAcceleration(STEPS_PER_DEG * ACCEL_DEG_S2); }
  uint8_t mac[6]; WiFi.macAddress(mac); char b[24]; snprintf(b, sizeof b, "SatLite-%02X%02X", mac[4], mac[5]); ap_ssid = b;
  WiFi.mode(WIFI_AP_STA); WiFi.softAP(ap_ssid.c_str(), AP_PASS); if (sta_ssid.length()) WiFi.begin(sta_ssid.c_str(), sta_pass.c_str());
  load_catalog(); load_tles();
  server.on("/", serve_index); server.on("/api/state", api_state); server.on("/api/passes", api_passes);
  for (const char *p : {"/api/track", "/api/stop", "/api/goto", "/api/goto_true", "/api/home", "/api/location", "/api/location_gps", "/api/decl", "/api/north", "/api/time", "/api/compass_cal", "/api/wifi", "/api/tle_update", "/api/tle_upload", "/api/key"}) server.on(p, api_cmd);
  server.begin();
  xTaskCreatePinnedToCore(passes_task, "passes", 12288, nullptr, 1, nullptr, 0);
}
void loop() {
  server.handleClient(); poll_gps();
  static unsigned long t1 = 0, t2 = 0;
  if (millis() - t1 > 100) { t1 = millis(); update_orientation(); }
  if (millis() - t2 > 500) { t2 = millis(); tracking_step(); }
  if ((limit_hit(PIN_AZ_LIM) && az_now() > 5 && azS && azS->isRunning() && azS->getCurrentPosition() < 5 * STEPS_PER_DEG) ) azS->stopMove();   // safety: do not drive past the AZ0 switch
}
