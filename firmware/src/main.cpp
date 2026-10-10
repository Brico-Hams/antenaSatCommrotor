#include <Arduino.h>
#include <WiFi.h>
#include <WebServer.h>
#include <WiFiClientSecure.h>
#include <HTTPClient.h>
#include <LittleFS.h>
#include <Preferences.h>
#include <Wire.h>
#include <TinyGPS++.h>
#include <ArduinoJson.h>
#include <NimBLEDevice.h>
#include <Sgp4.h>
#include <sys/time.h>
#include <mbedtls/sha256.h>
#include <vector>
#include <functional>
#include "board_config.h"
#include "control_logic.h"
#include "ble_protocol.h"

WebServer server(80);
Preferences prefs;
TinyGPSPlus gps;
HardwareSerial gnss(2);
TwoWire azBus(0), elBus(1);
SemaphoreHandle_t mutex;
struct Guard {
  Guard() { xSemaphoreTake(mutex, portMAX_DELAY); }
  ~Guard() { xSemaphoreGive(mutex); }
};
enum Mode { DISARMED, HOMING, READY, MOVING, TRACKING, FAULT };
const char *modeNames[] = {"DISARMED","HOMING","READY","MOVING","TRACKING","FAULT"};
Mode mode = DISARMED;
Control::Axis az, el;
bool hardware = false, homed = false, calibrated = false, level = false;
bool encoderZero = false, fsOK = false;
String apSsid, apPassword, apiToken, staSsid, staPassword;
bool provisioning = false, carrierChecked = false;
String serialLine;
bool serialOverflow = false;
enum Transport { NONE, HTTP_CONTROL, BLE_CONTROL };
Transport owner = NONE, transport = HTTP_CONTROL;
String requestBody, requestToken, requestPath, bleResponse;
int bleResponseCode = 500;
struct ApiRoute { String path; HTTPMethod method; std::function<void()> handler; };
std::vector<ApiRoute> apiRoutes;
bool bleConfigured = false;
uint32_t blePasskey = 0;
volatile bool bleConnected = false, bleSecure = false;
uint16_t bleHandle = BLE_HS_CONN_HANDLE_NONE;
NimBLEServer *bleServer = nullptr;
NimBLECharacteristic *bleTx = nullptr;
ControlBLE::Assembler bleAssembly;
String blePending, bleOutput;
uint32_t bleFragmentAt = 0, bleSendAt = 0, bleLastId = 0;
uint16_t bleOutputSequence = 0;
size_t bleOutputOffset = 0;
int bleProtocolError = 0;
String tleUpload, tleUploadHash;
uint32_t tleUploadId = 0, tleUploadAt = 0;
size_t tleUploadLength = 0;
Transport tleUploadOwner = NONE;
double encoderAz = 0, encoderEl = 0, north = 0;
double latitude = 0, longitude = 0, altitude = 0;
bool siteValid = false, manualSite = false;
uint32_t timeStamp = 0, fixStamp = 0, trackStamp = 0;
int64_t unixTime = 0;
String fault, downloadStatus = "Sin descarga";
int homeAxis = 0, homePhase = 0;
uint32_t homeStarted = 0, switchSince = 0;
bool switchStable = false;
struct Satellite { String name, one, two; int64_t epoch; };
std::vector<Satellite> satellites;
Sgp4 orbit;
int selected = -1;
double skyAz = 0, skyEl = 0, rangeKm = 0, rangeRate = 0;
bool orbitLoaded = false;
struct Pass { int64_t aos, los, peak; double maxEl; bool partial; };
std::vector<Pass> passes;
bool predicting = false, above = false;
bool predictionCached = false;
uint32_t predictionAt = 0;
int64_t predictionTime = 0, predictionEnd = 0;
Pass activePass{};

bool input(int pin) { return digitalRead(pin) == LOW; }
bool limit(int pin) { return digitalRead(pin) == HIGH; } // NC opens at limit
void enable(bool on) { if (hardware) digitalWrite(Board::enable, on ? LOW : HIGH); }
bool busy() { return mode == HOMING || mode == MOVING || mode == TRACKING; }
void abortUpload() {
  tleUpload = tleUploadHash = ""; tleUploadLength = 0; tleUploadOwner = NONE;
}
void halt(bool hard, const String &reason = "") {
  az.stop(); el.stop(); enable(false); owner = NONE;
  if (hard) {
    homed = calibrated = encoderZero = false;
    mode = FAULT; fault = reason;
  } else mode = homed ? READY : DISARMED;
}
int64_t nowUTC() { return unixTime + uint32_t(millis() - timeStamp) / 1000; }
bool validUTC() { return unixTime > 0 && uint32_t(millis() - timeStamp) < 3000; }
bool validSite() {
  return siteValid && (manualSite || uint32_t(millis() - fixStamp) < 5000);
}
String trackingBlocker() {
  if (!hardware) return "Pines no configurados";
  if (mode == FAULT) return fault;
  if (!homed) return "Requiere homing";
  if (!calibrated || !level) return "Requiere norte verdadero y nivelacion";
  if (!validUTC()) return "UTC GNSS invalida/caducada";
  if (!validSite()) return "Ubicacion GNSS invalida/caducada";
  if (selected < 0 || selected >= int(satellites.size())) return "Seleccione satelite";
  if (!Control::fresh(nowUTC(), satellites[selected].epoch)) return "TLE caducado/futuro";
  return "";
}
bool readEncoder(TwoWire &bus, double &angle) {
  bus.beginTransmission(0x36); bus.write(0x0B);
  if (bus.endTransmission(false) != 0 || bus.requestFrom(0x36, 1) != 1) return false;
  uint8_t status = bus.read();
  if (!(status & 0x20) || (status & 0x18)) return false;
  bus.beginTransmission(0x36); bus.write(0x0C);
  if (bus.endTransmission(false) != 0 || bus.requestFrom(0x36, 2) != 2) return false;
  angle = ((bus.read() & 15) * 256 + bus.read()) * 360.0 / 4096.0;
  return true;
}
void pulse(int stepPin, int dirPin, int step, int polarity) {
  if (!step) return;
  digitalWrite(dirPin, step * polarity > 0 ? HIGH : LOW);
  delayMicroseconds(3);
  digitalWrite(stepPin, HIGH); delayMicroseconds(3); digitalWrite(stepPin, LOW);
}
void motorTask(void *) {
  uint32_t previous = micros(), feedbackAt = 0;
  unsigned badFeedback = 0;
  for (;;) {
    {
      Guard guard;
      uint32_t us = micros();
      double dt = uint32_t(us - previous) / 1000000.0; previous = us;
      if (hardware && !input(Board::estop)) halt(true, "E-stop abierto");
      if (owner == BLE_CONTROL && !bleConnected && (mode == MOVING || mode == HOMING))
        halt(true, "BLE desconectado durante movimiento manual/homing");
      if (busy() && dt > .02) halt(true, "Plazo motor excedido");
      if (mode == TRACKING && (uint32_t(millis() - trackStamp) > 1500 ||
          !validUTC() || !validSite())) halt(true, "Seguimiento/UTC/ubicacion caducados");
      if (hardware && busy()) {
        if (limit(Board::azMin) && limit(Board::azMax)) halt(true, "Limites AZ contradictorios");
        if (limit(Board::elMin) && limit(Board::elMax)) halt(true, "Limites EL contradictorios");
        if (mode == HOMING) {
          bool changedAxis = false;
          Control::Axis &axis = homeAxis == 0 ? az : el;
          int pin = homeAxis == 0 ? Board::azMin : Board::elMin;
          if (uint32_t(millis() - homeStarted) > 240000) halt(true, "Timeout homing");
          else {
            bool contact = limit(pin);
            if (contact != switchStable) { switchStable = contact; switchSince = millis(); }
            if (uint32_t(millis() - switchSince) > 30) {
              if (homePhase == 0 && contact) {
                axis.stop(); homePhase = 1; axis.target = axis.position + 700;
              } else if (homePhase == 1 && !contact && std::fabs(axis.target - axis.position) < 1) {
                homePhase = 2; axis.target = axis.position - 1500;
              } else if (homePhase == 2 && contact) {
                axis.stop();
                axis.position = homeAxis == 0 ? -40000 : 0; axis.stop();
                if (homeAxis == 0) {
                  homeAxis = 1; homePhase = 0; homeStarted = millis();
                  el.target = el.position - 25000;
                  changedAxis = true;
                } else {
                  homed = true; mode = READY; enable(false);
                  if (Board::encoders) {
                    encoderZero = readEncoder(azBus, encoderAz) && readEncoder(elBus, encoderEl);
                    if (!encoderZero) halt(true, "AS5600 ausente/iman invalido");
                  }
                }
              }
            }
            if (mode == HOMING && !changedAxis && std::fabs(axis.target - axis.position) < 1 &&
                (homePhase == 0 || homePhase == 2 || switchStable))
              halt(true, "Limite homing no responde");
          }
        }
        if (busy()) {
          int sa = az.tick(dt), se = el.tick(dt);
          // Only the selected homing minimum switch is exempt when approaching it.
          bool azExempt = mode == HOMING && homeAxis == 0 && homePhase != 1;
          bool elExempt = mode == HOMING && homeAxis == 1 && homePhase != 1;
          if ((sa < 0 && limit(Board::azMin) && !azExempt) ||
              (sa > 0 && limit(Board::azMax)) ||
              (se < 0 && limit(Board::elMin) && !elExempt) ||
              (se > 0 && limit(Board::elMax))) halt(true, "Limite fisico");
          else if (mode != HOMING && !Control::inRange(
              az.position / Control::stepsPerDegree, el.position / Control::stepsPerDegree))
            halt(true, "Limite mecanico");
          else {
            pulse(Board::azStep, Board::azDir, sa, Board::azDirection);
            pulse(Board::elStep, Board::elDir, se, Board::elDirection);
          }
          if (mode == MOVING && std::fabs(az.target - az.position) < 1 &&
              std::fabs(el.target - el.position) < 1 && std::fabs(az.speed) < 1 &&
              std::fabs(el.speed) < 1) halt(false);
        }
      }
      if (Board::encoders && encoderZero && homed &&
          uint32_t(millis() - feedbackAt) > 100) {
        feedbackAt = millis(); double a, e;
        bool ok = readEncoder(azBus, a) && readEncoder(elBus, e);
        if (ok) ok = std::fabs(Control::difference(
          Board::azEncoderDirection * (a - encoderAz),
          (az.position + 40000) / Control::stepsPerDegree)) < 3 &&
          std::fabs(Control::difference(Board::elEncoderDirection * (e - encoderEl),
          el.position / Control::stepsPerDegree)) < 3;
        badFeedback = ok ? 0 : badFeedback + 1;
        if (badFeedback >= 3) halt(true, "AS5600 perdida/desviacion >3 grados");
      }
    }
    vTaskDelay(pdMS_TO_TICKS(1));
  }
}

void sendResponse(int code, const String &result) {
  if (code == 202 && (requestPath == "/api/home" || requestPath == "/api/move" ||
                     requestPath == "/api/track")) owner = transport;
  if (transport == BLE_CONTROL) { bleResponseCode = code; bleResponse = result; }
  else server.send(code, "application/json", result);
}
void route(const char *path, HTTPMethod method, std::function<void()> handler) {
  apiRoutes.push_back({path, method, handler});
  server.on(path, method, [path, handler] {
    transport = HTTP_CONTROL; requestPath = path;
    requestToken = server.header("X-Control-Token"); requestBody = server.arg("plain");
    handler();
  });
}
bool auth() {
  if (!ControlBLE::authorized(provisioning, transport != BLE_CONTROL || bleSecure,
      apiToken.c_str(),requestToken.c_str())) {
    sendResponse(401, "{\"error\":\"Token y enlace seguro requeridos\"}"); return false;
  }
  if (busy() && owner != NONE && owner != transport && requestPath != "/api/stop" &&
      requestPath != "/api/status" && requestPath != "/api/tle") {
    sendResponse(409, "{\"error\":\"Movimiento pertenece a otro transporte; STOP disponible\"}"); return false;
  }
  if (tleUploadOwner != NONE && requestPath != "/api/status" && requestPath != "/api/stop" &&
      requestPath != "/api/catalog" && !requestPath.startsWith("/api/tle/")) {
    sendResponse(409,"{\"error\":\"Transferencia TLE activa; commit/abort primero\"}"); return false;
  }
  return true;
}
void reply(int code, const String &message) {
  DynamicJsonDocument doc(512); doc[code < 400 ? "message" : "error"] = message;
  String body; serializeJson(doc, body); sendResponse(code, body);
}
bool body(DynamicJsonDocument &doc) {
  if (requestBody.length() > 50000 ||
      deserializeJson(doc, requestBody)) { reply(400, "JSON invalido"); return false; }
  return true;
}
void json(DynamicJsonDocument &doc) {
  String result; serializeJson(doc, result);
  if (transport == HTTP_CONTROL) server.sendHeader("Cache-Control", "no-store");
  sendResponse(200, result);
}
bool number(JsonVariant value, double &out) {
  if (!value.is<double>()) return false;
  out = value.as<double>(); return std::isfinite(out);
}
bool parseTles(const String &text, std::vector<Satellite> &out) {
  String name, one;
  int start = 0;
  while (start < int(text.length())) {
    int end = text.indexOf('\n', start); if (end < 0) end = text.length();
    String line = text.substring(start, end); if (line.endsWith("\r")) line.remove(line.length()-1);
    start = end + 1;
    if (!line.length()) continue;
    if (line.startsWith("1 ")) { if (one.length()) return false; one = line; }
    else if (line.startsWith("2 ")) {
      if (!one.length() || !Control::validTle(one.c_str(), line.c_str())) return false;
      String id = one.substring(2,7);
      for (auto &s : out) if (s.one.substring(2,7) == id) return false;
      out.push_back({name.length() ? name : id, one, line, Control::tleEpoch(one.c_str())});
      if (out.size() > 100) return false;
      one = name = "";
    } else {
      if (one.length() || line.length() > 64) return false;
      name = line.startsWith("0 ") ? line.substring(2) : line;
    }
  }
  return !one.length() && !out.empty();
}
bool cacheTles(const String &text) {
  std::vector<Satellite> candidate;
  if (!parseTles(text, candidate) || !fsOK) return false;
  File file = LittleFS.open("/tle.new", "w");
  if (!file) return false;
  size_t count = file.print(text); file.close();
  if (count != text.length()) return false;
  // ESP32 LittleFS rename replaces the destination atomically.
  if (!LittleFS.rename("/tle.new", "/tle.txt")) return false;
  satellites.swap(candidate); selected = -1; orbitLoaded = false;
  predicting = predictionCached = false; passes.clear(); return true;
}
bool loadOrbit(int index) {
  if (index < 0 || index >= int(satellites.size())) return false;
  selected = index;
  // The upstream class has uninitialized line1 and mutates its input buffers.
  memset(orbit.line1, 0, sizeof(orbit.line1));
  char a[130] = {}, b[130] = {};
  satellites[index].one.toCharArray(a, sizeof(a));
  satellites[index].two.toCharArray(b, sizeof(b));
  orbitLoaded = orbit.init(satellites[index].name.c_str(), a, b);
  orbit.site(latitude, longitude, altitude);
  return orbitLoaded && orbit.satrec.error == 0;
}
bool propagate(int64_t when) {
  orbit.findsat(double(when) / 86400 + 2440587.5);
  return orbit.satrec.error == 0 && std::isfinite(orbit.satAz) &&
    std::isfinite(orbit.satEl) && std::isfinite(orbit.satDist);
}
void routes() {
  route("/api/catalog",HTTP_POST,[] {
    if(!auth()) return;
    DynamicJsonDocument request(256); if(!body(request)) return; Guard guard;
    if(!request["offset"].is<int>() || !request["limit"].is<int>() ||
        request["offset"].as<int>()<0 || request["limit"].as<int>()<1 ||
        request["limit"].as<int>()>10) { reply(400,"offset>=0 limit1..10 requeridos"); return; }
    int offset=request["offset"], limit=request["limit"];
    DynamicJsonDocument d(4096); d["total"]=satellites.size();
    JsonArray list=d.createNestedArray("satellites");
    int end=std::min(offset+limit,int(satellites.size()));
    for(int i=offset;i<end;++i) {
      JsonObject s=list.createNestedObject(); s["id"]=i; s["name"]=satellites[i].name;
      s["epoch"]=satellites[i].epoch;
      s["fresh"]=validUTC() && Control::fresh(nowUTC(),satellites[i].epoch);
    }
    d["nextOffset"]=end<int(satellites.size())?end:-1; json(d);
  });
  route("/api/tle/begin",HTTP_POST,[] {
    if(!auth()) return;
    DynamicJsonDocument d(512); if(!body(d)) return; Guard guard;
    if(busy() || tleUploadOwner!=NONE) { reply(409,"Motores/transferencia ocupados"); return; }
    String hash=d["sha256"] | "";
    if(!d["length"].is<int>() || d["length"].as<int>()<1 ||
        d["length"].as<int>()>48000 || hash.length()!=64) {
      reply(400,"length1..48000 y sha256 lowercase64hex requeridos"); return;
    }
    for(unsigned i=0;i<hash.length();++i) {
      char c=hash[i];
      if(!((c>='0'&&c<='9')||(c>='a'&&c<='f'))) {
        reply(400,"sha256 invalido"); return;
      }
    }
    tleUploadLength=d["length"]; tleUploadHash=hash; tleUpload="";
    if(!tleUpload.reserve(tleUploadLength+1)) { abortUpload(); reply(503,"RAM insuficiente"); return; }
    ++tleUploadId; if(!tleUploadId) ++tleUploadId;
    tleUploadAt=millis(); tleUploadOwner=transport;
    DynamicJsonDocument response(256); response["message"]="Transferencia iniciada";
    response["uploadId"]=tleUploadId; json(response);
  });
  route("/api/tle/chunk",HTTP_POST,[] {
    if(!auth()) return;
    DynamicJsonDocument d(1800); if(!body(d)) return; Guard guard;
    if(busy() || tleUploadOwner!=transport || !d["uploadId"].is<uint32_t>() ||
        d["uploadId"].as<uint32_t>()!=tleUploadId) { reply(409,"Transferencia/propietario invalido"); return; }
    String text=d["text"] | "";
    if(!d["offset"].is<uint32_t>() || d["offset"].as<uint32_t>()!=tleUpload.length() ||
        !d["text"].is<const char *>() || text.length()<1 || text.length()>512 ||
        tleUpload.length()+text.length()>tleUploadLength) {
      reply(400,"offset secuencial/text1..512/length requeridos"); return;
    }
    size_t expected=tleUpload.length()+text.length();
    tleUpload+=text;
    if(tleUpload.length()!=expected) { abortUpload(); reply(503,"RAM insuficiente"); return; }
    tleUploadAt=millis(); DynamicJsonDocument response(256);
    response["message"]="Chunk recibido"; response["received"]=tleUpload.length(); json(response);
  });
  route("/api/tle/commit",HTTP_POST,[] {
    if(!auth()) return;
    DynamicJsonDocument d(256); if(!body(d)) return; Guard guard;
    if(busy() || tleUploadOwner!=transport || !d["uploadId"].is<uint32_t>() ||
        d["uploadId"].as<uint32_t>()!=tleUploadId) { reply(409,"Transferencia/propietario invalido"); return; }
    if(tleUpload.length()!=tleUploadLength) { reply(400,"Transferencia incompleta"); return; }
    uint8_t digest[32]; char hex[65];
    int result=mbedtls_sha256_ret(reinterpret_cast<const unsigned char*>(tleUpload.c_str()),
      tleUpload.length(),digest,0);
    for(int i=0;i<32;++i) sprintf(hex+i*2,"%02x",digest[i]); hex[64]=0;
    if(result || tleUploadHash!=hex) { abortUpload(); reply(400,"SHA256 no coincide; cache conservada"); return; }
    bool saved=cacheTles(tleUpload); abortUpload();
    if(!saved) { reply(400,"TLE/almacenamiento invalidos; cache conservada"); return; }
    reply(200,"TLE validado y guardado");
  });
  route("/api/tle/abort",HTTP_POST,[] {
    if(!auth()) return;
    DynamicJsonDocument d(256); if(!body(d)) return; Guard guard;
    if(tleUploadOwner!=transport || !d["uploadId"].is<uint32_t>() ||
        d["uploadId"].as<uint32_t>()!=tleUploadId) { reply(409,"Transferencia/propietario invalido"); return; }
    abortUpload(); reply(200,"Transferencia abortada; cache conservada");
  });
  route("/api/status", HTTP_GET, [] {
    if (!auth()) return; Guard guard;
    DynamicJsonDocument d(2048);
    d["apiVersion"] = ControlBLE::apiVersion;
    d["protocolVersion"] = ControlBLE::protocolVersion;
    d["firmwareVersion"] = ControlBLE::firmwareVersion;
    d["mode"] = modeNames[mode]; d["fault"] = fault; d["hardwareConfigured"] = hardware;
    d["controlOwner"] = owner == BLE_CONTROL ? "BLE" : owner == HTTP_CONTROL ? "HTTP" : "none";
    d["bleConfigured"] = bleConfigured; d["bleConnected"] = bleConnected;
    d["bleSecure"] = bleSecure; d["encoderZeroVerified"] = encoderZero;
    d["homed"] = homed; d["calibrated"] = calibrated; d["level"] = level;
    d["enabled"] = busy(); d["utcValid"] = validUTC(); d["utc"] = nowUTC();
    d["siteValid"] = validSite(); d["manualSite"] = manualSite;
    d["lat"] = latitude; d["lon"] = longitude; d["alt"] = altitude; d["northOffset"] = north;
    d["azMechanical"] = az.position / Control::stepsPerDegree;
    d["el"] = el.position / Control::stepsPerDegree; d["skyAz"] = skyAz; d["skyEl"] = skyEl;
    d["rangeKm"] = rangeKm; d["rangeRateKmS"] = rangeRate;
    d["doppler145Hz"] = -rangeRate / 299792.458 * 145000000;
    d["doppler435Hz"] = -rangeRate / 299792.458 * 435000000;
    d["trackingBlocker"] = trackingBlocker(); d["download"] = downloadStatus;
    d["staConnected"] = WiFi.status() == WL_CONNECTED; d["encoders"] = Board::encoders;
    d["selected"] = selected; d["pttCat"] = false; json(d);
  });
  route("/api/stop", HTTP_POST, [] {
    if (!auth()) return; Guard guard;
    if (mode == HOMING) halt(true, "Homing interrumpido");
    else if (mode != FAULT) halt(false);
    reply(200, "Motores deshabilitados; no borra fallos");
  });
  route("/api/clear", HTTP_POST, [] {
    if (!auth()) return; Guard guard;
    if (!hardware || !input(Board::estop)) { reply(409, "E-stop/pines"); return; }
    halt(false); homed = calibrated = encoderZero = false; mode = DISARMED; fault = "";
    reply(200, "Fallo borrado; requiere homing y calibracion");
  });
  route("/api/home", HTTP_POST, [] {
    if (!auth()) return; Guard guard;
    if (!hardware || mode == FAULT || busy() || !input(Board::estop)) {
      reply(409, "No disponible: pines/fallo/ocupado/e-stop"); return;
    }
    homed = calibrated = encoderZero = false; az.stop(); el.stop();
    homeAxis = homePhase = 0; homeStarted = switchSince = millis();
    switchStable = limit(Board::azMin); az.target = az.position - 85000;
    mode = HOMING; enable(true); reply(202, "Homing AZ y EL iniciado");
  });
  route("/api/move", HTTP_POST, [] {
    if (!auth()) return;
    DynamicJsonDocument d(512); if (!body(d)) return; Guard guard;
    double a, e;
    if (!number(d["az"], a) || !number(d["el"], e) || !Control::inRange(a,e)) {
      reply(400, "AZ mecanico -180..180, EL 0..90"); return;
    }
    if (!hardware || !homed || mode == FAULT || busy()) { reply(409, "Requiere homing/estado libre"); return; }
    az.target = round(a * Control::stepsPerDegree); el.target = round(e * Control::stepsPerDegree);
    mode = MOVING; enable(true); reply(202, "Movimiento iniciado");
  });
  route("/api/site", HTTP_POST, [] {
    if (!auth()) return;
    DynamicJsonDocument d(512); if (!body(d)) return; Guard guard;
    if (busy()) { reply(409, "Detenga antes de cambiar sitio"); return; }
    double a,b,c;
    if (!d["manual"].is<bool>() || !number(d["lat"],a) || !number(d["lon"],b) ||
        !number(d["alt"],c) || a < -90 || a > 90 || b < -180 || b > 180 || c < -500 || c > 9000) {
      reply(400, "manual boolean y lat/lon/alt numericos requeridos"); return;
    }
    latitude=a; longitude=b; altitude=c; manualSite=d["manual"]; siteValid=manualSite;
    prefs.putDouble("lat",a); prefs.putDouble("lon",b); prefs.putDouble("alt",c);
    prefs.putBool("manual",manualSite); prefs.putBool("site",true);
    orbitLoaded=false; predicting=predictionCached=false; passes.clear(); reply(200,"Sitio guardado; UTC siempre GNSS");
  });
  route("/api/calibrate", HTTP_POST, [] {
    if (!auth()) return;
    DynamicJsonDocument d(512); if (!body(d)) return; Guard guard;
    double a;
    if (!number(d["trueAz"],a) || a < 0 || a >= 360 || d["levelConfirmed"] != true) {
      reply(400,"trueAz 0..<360 y levelConfirmed true requeridos"); return;
    }
    if (!homed || busy() || mode == FAULT || std::fabs(el.position) > 1 ||
        (Board::encoders && !encoderZero)) {
      reply(409,"Homing, EL=0, reposo requeridos"); return;
    }
    north = Control::wrap(a - az.position / Control::stepsPerDegree);
    level = calibrated = true; prefs.putDouble("north", north);
    reply(200,"Norte verdadero y nivel confirmados para esta sesion");
  });
  route("/api/tle", HTTP_GET, [] {
    if (!auth()) return; Guard guard;     DynamicJsonDocument d(48000);
    JsonArray list=d.createNestedArray("satellites");
    for (size_t i=0;i<satellites.size();++i) {
      auto &s=satellites[i]; JsonObject o=list.createNestedObject();
      o["id"]=i; o["name"]=s.name; o["epoch"]=s.epoch;
      o["fresh"]=validUTC() && Control::fresh(nowUTC(),s.epoch);
      o["line1"]=s.one; o["line2"]=s.two;
    }
    json(d);
  });
  route("/api/tle", HTTP_POST, [] {
    if (!auth()) return;
    DynamicJsonDocument d(52000); if (!body(d)) return; Guard guard;
    if (busy()) { reply(409,"Detenga antes de importar"); return; }
    if (!d["text"].is<const char *>() || !cacheTles(d["text"].as<String>())) {
      reply(400,"TLE invalido, >100 satelites o fallo almacenamiento; cache anterior conservada"); return;
    }
    reply(200,"TLE validado y guardado");
  });
  route("/api/select", HTTP_POST, [] {
    if (!auth()) return;
    DynamicJsonDocument d(256); if (!body(d)) return; Guard guard;
    if (busy()) { reply(409,"Detenga primero"); return; }
    if (!d["id"].is<int>() || !loadOrbit(d["id"])) { reply(400,"Satelite/SGP4 invalido"); return; }
    passes.clear(); predicting=predictionCached=false; reply(200,"Satelite seleccionado");
  });
  route("/api/track", HTTP_POST, [] {
    if (!auth()) return; Guard guard;
    String reason=trackingBlocker();
    if (reason.length() || busy() || !orbitLoaded) { reply(409,reason.length()?reason:"Ocupado/seleccione de nuevo"); return; }
    if (!propagate(nowUTC()) || orbit.satEl < 0 || orbit.satEl >= 89) {
      reply(409,"Satelite bajo horizonte/cenit >=89 grados/error SGP4"); return;
    }
    double initialAz=orbit.satAz, initialEl=orbit.satEl, mechanical;
    Control::mechanicalAz(initialAz,north,mechanical);
    double allowedRate=Control::maxRate/Control::stepsPerDegree;
    if (!propagate(nowUTC()+1) ||
        std::fabs(Control::difference(orbit.satAz,initialAz))>allowedRate ||
        std::fabs(orbit.satEl-initialEl)>allowedRate) {
      reply(409,"Velocidad angular satelite excede limite motor/error SGP4"); return;
    }
    if (std::fabs(mechanical-az.position/Control::stepsPerDegree)>15 ||
        std::fabs(initialEl-el.position/Control::stepsPerDegree)>15) {
      reply(409,"Adquisicion >15 grados/cruce cable: apunte primero"); return;
    }
    trackStamp=millis(); mode=TRACKING; enable(true); reply(202,"Seguimiento iniciado");
  });
  route("/api/passes", HTTP_GET, [] {
    if (!auth()) return; Guard guard;
    if (busy()) { reply(409,"Prediccion solo con motores detenidos"); return; }
    if (!validUTC() || !validSite() || !orbitLoaded || selected < 0 ||
        !Control::fresh(nowUTC(),satellites[selected].epoch)) { reply(409,"UTC/sitio/TLE/seleccion invalidos"); return; }
    if (!predicting && (!predictionCached || uint32_t(millis()-predictionAt)>60000)) {
      passes.clear(); predictionCached=true; predictionAt=millis();
      predictionTime=nowUTC(); predictionEnd=predictionTime+86400;
      above=false; predicting=true; orbit.site(latitude,longitude,altitude);
    }
    DynamicJsonDocument d(4096); d["calculating"]=predicting; d["stepSeconds"]=10;
    JsonArray list=d.createNestedArray("passes");
    for (auto &p:passes) {
      JsonObject o=list.createNestedObject(); o["aos"]=p.aos; o["los"]=p.los;
      o["peak"]=p.peak; o["maxEl"]=p.maxEl; o["partial"]=p.partial;
    }
    json(d);
  });
  route("/api/update", HTTP_POST, [] {
    if (!auth()) return;
    if (transport == BLE_CONTROL) { reply(409,"HTTPS solo por HTTP en reposo; importe TLE manual"); return; }
    DynamicJsonDocument d(256); if (!body(d)) return;
    String provider=d["provider"] | "";
    String url;
    if(provider=="celestrak") url="https://celestrak.org/NORAD/elements/gp.php?GROUP=amateur&FORMAT=tle";
    else if(provider=="amsat") url="https://www.amsat.org/tle/current/dailytle.txt";
    else if(provider=="pe0sat") url="https://tle.pe0sat.nl/kepler/mykepler.txt";
    else { reply(400,"Proveedor desconocido"); return; }
    {
      Guard guard;
      if(busy() || mode==FAULT || !validUTC() || WiFi.status()!=WL_CONNECTED ||
          !strlen(Board::tlsRoots)) {
        downloadStatus="Descarga rechazada: reposo, UTC GNSS, STA y CA PEM requeridos";
        reply(409,downloadStatus); return;
      }
      timeval tv{static_cast<time_t>(nowUTC()),0}; settimeofday(&tv,nullptr);
    }
    WiFiClientSecure client; client.setCACert(Board::tlsRoots); client.setTimeout(8);
    HTTPClient http; http.setTimeout(8000); http.setConnectTimeout(5000);
    http.setFollowRedirects(HTTPC_DISABLE_FOLLOW_REDIRECTS);
    int code=-1; String text;
    if(http.begin(client,url)) {
      code=http.GET();
      // Require bounded Content-Length. Refuse unbounded/chunked downloads safely.
      if(code==200 && http.getSize()>0 && http.getSize()<=48000) text=http.getString();
      http.end();
    }
    Guard guard;
    if(code!=200 || text.isEmpty() || !cacheTles(text)) {
      downloadStatus="Fallo descarga/TLS/formato/tamano HTTP "+String(code)+"; cache anterior conservada";
      reply(502,downloadStatus); return;
    }
    downloadStatus="Actualizado desde "+provider; reply(200,downloadStatus);
  });
  server.on("/", HTTP_GET, [] {
    File f=LittleFS.open("/index.html","r");
    if(!f) { server.send(503,"text/plain","Suba LittleFS: pio run -t uploadfs"); return; }
    server.sendHeader("Content-Security-Policy",
      "default-src 'self'; script-src 'unsafe-inline'; style-src 'unsafe-inline'; connect-src 'self'; frame-ancestors 'none'");
    server.streamFile(f,"text/html"); f.close();
  });
  server.onNotFound([] { reply(404,"Ruta no encontrada"); });
}
bool checkPins() {
  int outputs[]={Board::azStep,Board::azDir,Board::elStep,Board::elDir,Board::enable,
    Board::gpsRx,Board::gpsTx};
  int inputs[]={Board::estop,Board::azMin,Board::azMax,Board::elMin,Board::elMax};
  std::vector<int> all;
  auto add=[&](int pin,bool output) {
    if(pin<0 || pin>39 || (pin>=6 && pin<=11) || pin==20 || pin==24 ||
       (pin>=28 && pin<=31) || (output && pin>=34)) return false;
    // Avoid boot-strapping, serial-console, and flash/PSRAM pins by default.
    if(pin==0 || pin==1 || pin==2 || pin==3 || pin==5 || pin==12 ||
       pin==15) return false;
    for(int p:all) if(p==pin) return false;
    all.push_back(pin); return true;
  };
  for(int p:outputs) if(!add(p,true)) return false;
  for(int p:inputs) if(!add(p,false)) return false;
  if(Board::encoders) for(int p:{Board::azSda,Board::azScl,Board::elSda,Board::elScl})
    if(!add(p,true)) return false;
  return true;
}
class BleServerCallbacks : public NimBLEServerCallbacks {
  void onConnect(NimBLEServer *, ble_gap_conn_desc *desc) override {
    Guard guard; bleConnected = true; bleSecure = false;
    bleHandle = desc->conn_handle; bleLastId = 0;
    blePending = bleOutput = ""; bleAssembly.reset();
  }
  void onDisconnect(NimBLEServer *) override {
    {
      Guard guard; bleConnected = bleSecure = false;
      bleHandle = BLE_HS_CONN_HANDLE_NONE;
      blePending = bleOutput = ""; bleAssembly.reset(); bleProtocolError = 0;
      if (tleUploadOwner == BLE_CONTROL) abortUpload();
    }
    if (!provisioning) NimBLEDevice::startAdvertising();
  }
  uint32_t onPassKeyRequest() override { return blePasskey; }
  void onAuthenticationComplete(ble_gap_conn_desc *desc) override {
    bool secure = desc->sec_state.encrypted && desc->sec_state.authenticated &&
                  desc->sec_state.bonded;
    { Guard guard; bleSecure = secure; }
    if (!secure) bleServer->disconnect(desc->conn_handle);
  }
};
class BleRxCallbacks : public NimBLECharacteristicCallbacks {
  void onWrite(NimBLECharacteristic *characteristic, ble_gap_conn_desc *desc) override {
    if (!desc->sec_state.encrypted || !desc->sec_state.authenticated ||
        !desc->sec_state.bonded) return;
    auto value = characteristic->getValue();
    Guard guard;
    if (provisioning || !bleSecure) return;
    int result = bleAssembly.feed(value.data(), value.length()); bleFragmentAt = millis();
    if (result < 0) bleProtocolError = 400;
    else if (result == 1) {
      if (blePending.length()) bleProtocolError = 429;
      else blePending = bleAssembly.data;
      bleAssembly.reset();
    }
  }
};
void setupBLE() {
  if (!bleConfigured || !ControlBLE::validPasskey(blePasskey) ||
      !Control::validCredentials(apSsid.c_str(),apPassword.c_str(),apiToken.c_str())) return;
  NimBLEDevice::init("PortableSatStation");
  NimBLEDevice::setSecurityIOCap(BLE_HS_IO_DISPLAY_ONLY);
  NimBLEDevice::setSecurityAuth(true, true, true); // bonding, MITM, Secure Connections
  NimBLEDevice::setSecurityPasskey(blePasskey);
  if (prefs.getBool("bleReset",false)) {
    NimBLEDevice::deleteAllBonds(); prefs.putBool("bleReset",false);
  }
  NimBLEDevice::setMTU(23);
  bleServer = NimBLEDevice::createServer(); bleServer->setCallbacks(new BleServerCallbacks());
  auto service = bleServer->createService("c8200001-4e53-4253-9000-000000000001");
  auto rx = service->createCharacteristic("c8200002-4e53-4253-9000-000000000001",
    NIMBLE_PROPERTY::WRITE | NIMBLE_PROPERTY::WRITE_ENC | NIMBLE_PROPERTY::WRITE_AUTHEN, 20);
  rx->setCallbacks(new BleRxCallbacks());
  bleTx = service->createCharacteristic("c8200003-4e53-4253-9000-000000000001",
    NIMBLE_PROPERTY::NOTIFY | NIMBLE_PROPERTY::READ_ENC | NIMBLE_PROPERTY::READ_AUTHEN, 20);
  service->start();
  auto advertising = NimBLEDevice::getAdvertising();
  advertising->addServiceUUID(service->getUUID()); advertising->setScanResponse(true);
  advertising->start();
}
void bleResult(uint32_t id, int code, const String &data) {
  DynamicJsonDocument d(18000); d["v"] = 1; d["id"] = id; d["code"] = code;
  DynamicJsonDocument payload(16000);
  if (data.length() > 8192 || deserializeJson(payload,data)) {
    d["code"] = 413; d["data"]["error"] = "Respuesta demasiado grande; use HTTP";
  } else d["data"] = payload.as<JsonVariant>();
  String result; serializeJson(d,result);
  if (result.length() > 8192) {
    result = "{\"v\":1,\"id\":" + String(id) +
      ",\"code\":413,\"data\":{\"error\":\"Respuesta demasiado grande; use HTTP\"}}";
  }
  Guard guard; bleOutput = result; bleOutputOffset = bleOutputSequence = 0;
}
void serviceBLE() {
  if (!bleServer) return;
  if (provisioning) {
    NimBLEDevice::stopAdvertising();
    if (bleConnected) bleServer->disconnect(bleHandle);
    return;
  }
  String pending; int protocolError = 0;
  {
    Guard guard;
    if (bleAssembly.active && uint32_t(millis()-bleFragmentAt)>3000) {
      bleAssembly.reset(); bleProtocolError = 408;
    }
    pending = blePending; blePending = ""; protocolError = bleProtocolError; bleProtocolError = 0;
  }
  if (pending.length()) {
    DynamicJsonDocument d(5000);
    if (deserializeJson(d,pending) || d["v"] != 1 || !d["id"].is<uint32_t>() ||
        d["id"].as<uint32_t>() == 0 || d["id"].as<uint32_t>() <= bleLastId ||
        !d["path"].is<const char *>() || !d["method"].is<const char *>() ||
        !d["token"].is<const char *>() || !d["body"].is<JsonObject>()) {
      bleResult(0,400,"{\"error\":\"Esquema v1/id creciente/metodo/ruta/token/body requerido\"}");
    } else {
      uint32_t id = d["id"]; bleLastId = id;
      String method = d["method"].as<String>(), path = d["path"].as<String>();
      bool transmitting;
      { Guard guard; transmitting = bleOutput.length(); }
      if (transmitting && path != "/api/stop") {
        // Stop has priority; other commands must await the previous response END.
        bleResult(id,429,"{\"error\":\"Espere END de respuesta anterior\"}");
      } else {
        transport = BLE_CONTROL; requestPath = path; requestToken = d["token"].as<String>();
        requestBody = ""; serializeJson(d["body"],requestBody);
        bleResponseCode = 404; bleResponse = "{\"error\":\"Ruta/metodo no disponible\"}";
        for (auto &r : apiRoutes) {
          if (r.path == path && ((method=="GET" && r.method==HTTP_GET) ||
                                (method=="POST" && r.method==HTTP_POST))) { r.handler(); break; }
        }
        bleResult(id,bleResponseCode,bleResponse);
        requestToken = requestBody = ""; transport = HTTP_CONTROL;
      }
    }
  } else if (protocolError) bleResult(0,protocolError,"{\"error\":\"Trama/cola/timeout BLE invalido\"}");
  uint8_t frame[20]; size_t count = 0;
  {
    Guard guard;
    if (bleSecure && bleConnected && bleOutput.length() &&
        uint32_t(millis()-bleSendAt)>=10 && bleTx->getSubscribedCount()) {
      bleSendAt = millis();
      size_t available = bleOutput.length() - bleOutputOffset;
      size_t payload = std::min(size_t(16), available);
      frame[0] = ControlBLE::magic; frame[1] = bleOutputOffset == 0 ? 1 : 0;
      if (payload == available) frame[1] |= 2;
      frame[2] = bleOutputSequence & 255; frame[3] = bleOutputSequence >> 8;
      memcpy(frame+4,bleOutput.c_str()+bleOutputOffset,payload); count = payload + 4;
      bleOutputOffset += payload; ++bleOutputSequence;
      if (bleOutputOffset == bleOutput.length()) bleOutput = "";
    }
  }
  if (count) bleTx->notify(frame,count);
}
void serialProvisioning() {
  while (Serial.available()) {
    char c = Serial.read();
    if (c == '\r') continue;
    if (c != '\n') {
      if (serialLine.length() < 768 && !serialOverflow) serialLine += c;
      else { serialOverflow = true; serialLine = ""; }
      continue;
    }
    if (serialOverflow) {
      serialOverflow = false; serialLine = ""; Serial.println("ERROR linea >768 bytes"); continue;
    }
    DynamicJsonDocument d(1536);
    auto error = deserializeJson(d, serialLine); serialLine = "";
    if (error || !d["cmd"].is<const char *>()) { Serial.println("ERROR JSON"); continue; }
    String command = d["cmd"].as<String>();
    Guard guard;
    if (command == "setup") {
      halt(true, "Provisionamiento USB"); provisioning = true;
      abortUpload();
      WiFi.disconnect(true); WiFi.softAPdisconnect(true);
      Serial.println("SETUP: motores OFF; homing/calibracion invalidados; credenciales no se muestran");
    } else if (!provisioning) Serial.println("ERROR requiere cmd setup");
    else if (command == "config") {
      if (!d["ssid"].is<const char *>() || !d["password"].is<const char *>() ||
          !d["token"].is<const char *>() ||
          !Control::validCredentials(d["ssid"], d["password"], d["token"])) {
        Serial.println("ERROR ssid1..32/password12..63/token24..128 ASCII"); continue;
      }
      String ss = d["staSsid"] | "", sp = d["staPassword"] | "";
      if (ss.length() > 32 || sp.length() > 63 || (ss.length() && sp.length() < 8)) {
        Serial.println("ERROR STA"); continue;
      }
      bool ok = prefs.putString("apSsid", d["ssid"].as<String>()) > 0 &&
        prefs.putString("apPass", d["password"].as<String>()) > 0 &&
        prefs.putString("token", d["token"].as<String>()) > 0;
      prefs.putString("staSsid", ss); prefs.putString("staPass", sp);
      Serial.println(ok ? "CONFIG guardada; cmd reboot para aplicar" : "ERROR NVS");
    } else if (command == "carrier") {
      if (!d["verified"].is<bool>()) { Serial.println("ERROR verified boolean"); continue; }
      prefs.putBool("carrier", d["verified"].as<bool>());
      Serial.println("Verificacion carrier guardada; no habilita motores en SETUP");
    } else if (command == "ble") {
      if (!d["enabled"].is<bool>() ||
          (d["enabled"] == true && (!d["passkey"].is<uint32_t>() ||
           !ControlBLE::validPasskey(d["passkey"].as<uint32_t>())))) {
        Serial.println("ERROR enabled boolean y passkey local 100000..999999"); continue;
      }
      prefs.putBool("ble",d["enabled"].as<bool>()); prefs.putBool("bleReset",true);
      if (d["enabled"] == true) prefs.putUInt("bleKey",d["passkey"].as<uint32_t>());
      Serial.println("BLE guardado; no muestra passkey; reboot requerido");
    } else if (command == "reboot") {
      Serial.println("REBOOT DISARMED"); Serial.flush(); ESP.restart();
    } else Serial.println("ERROR comando");
  }
}
void setup() {
  Serial.begin(115200); mutex=xSemaphoreCreateMutex();
  // Disable valid configured enable even if another pin is invalid.
  if(Board::enable>=0 && Board::enable<34) {
    digitalWrite(Board::enable,HIGH); pinMode(Board::enable,OUTPUT);
  }
  prefs.begin("station",false);
  carrierChecked=prefs.getBool("carrier",Board::carrierVerified);
  hardware=carrierChecked && checkPins();
  if(hardware) {
    for(int p:{Board::azStep,Board::azDir,Board::elStep,Board::elDir}) {
      digitalWrite(p,LOW); pinMode(p,OUTPUT);
    }
    for(int p:{Board::estop,Board::azMin,Board::azMax,Board::elMin,Board::elMax})
      pinMode(p,INPUT_PULLUP); // GPIO34..39 need external pull-ups
    gnss.begin(Board::gpsBaud,SERIAL_8N1,Board::gpsRx,Board::gpsTx);
    if(Board::encoders) {
      azBus.begin(Board::azSda,Board::azScl,100000);
      elBus.begin(Board::elSda,Board::elScl,100000);
      azBus.setTimeOut(5); elBus.setTimeOut(5);
    }
  }
  fsOK=LittleFS.begin(false); // Never format on mount failure.
  apSsid=prefs.getString("apSsid",Board::apSsid);
  apPassword=prefs.getString("apPass",Board::apPassword);
  apiToken=prefs.getString("token",Board::apiToken);
  staSsid=prefs.getString("staSsid",Board::staSsid);
  staPassword=prefs.getString("staPass",Board::staPassword);
  bleConfigured=prefs.getBool("ble",false); blePasskey=prefs.getUInt("bleKey",0);
  latitude=prefs.getDouble("lat",0); longitude=prefs.getDouble("lon",0);
  altitude=prefs.getDouble("alt",0); north=prefs.getDouble("north",0);
  manualSite=prefs.getBool("manual",false); siteValid=manualSite && prefs.getBool("site",false);
  if(fsOK) {
    File f=LittleFS.open("/tle.txt","r");
    if(f && f.size()<=48000) {
      String text=f.readString(); std::vector<Satellite> candidate;
      if(parseTles(text,candidate)) satellites.swap(candidate);
    }
    f.close();
  }
  WiFi.mode(WIFI_AP_STA);
  if(Control::validCredentials(apSsid.c_str(),apPassword.c_str(),apiToken.c_str()))
    WiFi.softAP(apSsid.c_str(),apPassword.c_str());
  else Serial.println("AP desactivado: configure password >=12 y token >=24");
  if(staSsid.length()) WiFi.begin(staSsid.c_str(),staPassword.c_str());
  const char *headers[]={"X-Control-Token"}; server.collectHeaders(headers,1);
  routes(); server.begin();
  setupBLE();
  xTaskCreatePinnedToCore(motorTask,"motion",4096,nullptr,3,nullptr,0);
  Serial.println("DISARMED; nunca se restaura homing/calibracion desde NVS");
  Serial.println("USB setup: {\"cmd\":\"setup\"}; configure JSON privado, nunca envie credenciales a nube");
}
void loop() {
  serialProvisioning();
  serviceBLE();
  if(hardware) while(gnss.available()) gps.encode(gnss.read());
  {
    Guard guard;
    if(tleUploadOwner!=NONE && uint32_t(millis()-tleUploadAt)>60000) abortUpload();
    if(gps.date.isValid() && gps.time.isValid() && gps.date.age()<2000 &&
        gps.time.age()<2000 && gps.time.isUpdated()) {
      int64_t t=Control::utc(gps.date.year(),gps.date.month(),gps.date.day(),
        gps.time.hour(),gps.time.minute(),gps.time.second());
      if(t) {
        if(validUTC() && std::llabs(t-nowUTC())>2 && busy()) halt(true,"Salto UTC GNSS");
        unixTime=t; timeStamp=millis();
      }
    }
    if(!manualSite && gps.location.isValid() && gps.location.age()<2000 &&
        gps.altitude.isValid() && gps.altitude.age()<2000) {
      latitude=gps.location.lat(); longitude=gps.location.lng(); altitude=gps.altitude.meters();
      siteValid=true; fixStamp=millis()-gps.location.age();
    }
    static uint32_t trackingAt=0;
    if(mode==TRACKING && uint32_t(millis()-trackingAt)>=200) {
      trackingAt=millis(); String block=trackingBlocker();
      orbit.site(latitude,longitude,altitude);
      if(block.length() || !propagate(nowUTC())) halt(true,block.length()?block:"Error SGP4");
      else if(orbit.satEl<0) halt(false);
      else if(orbit.satEl>=89) halt(true,"Zona cenit >=89 grados no admisible");
      else {
        skyAz=orbit.satAz; skyEl=orbit.satEl; rangeKm=orbit.satDist;
        double nextRange=rangeKm, desired;
        bool futureOK=propagate(nowUTC()+1);
        if(futureOK) nextRange=orbit.satDist;
        rangeRate=nextRange-rangeKm;
        Control::mechanicalAz(skyAz,north,desired);
        double current=az.position/Control::stepsPerDegree;
        double allowedRate=Control::maxRate/Control::stepsPerDegree;
        if(!futureOK) halt(true,"Error SGP4 futuro");
        else if(std::fabs(Control::difference(orbit.satAz,skyAz))>allowedRate ||
            std::fabs(orbit.satEl-skyEl)>allowedRate)
          halt(true,"Velocidad angular satelite excede limite motor");
        else if(std::fabs(desired-current)>180) halt(true,"Cruce limite cable AZ: reposicionar");
        else {
          az.target=round(desired*Control::stepsPerDegree);
          el.target=round(skyEl*Control::stepsPerDegree); trackStamp=millis();
          if(std::fabs(az.target-az.position)>15*Control::stepsPerDegree ||
             std::fabs(el.target-el.position)>15*Control::stepsPerDegree)
            halt(true,"Adquisicion >15 grados: apuntar manualmente antes");
        }
      }
    }
    if(predicting && !busy()) {
      // Bounded SGP4 work per iteration; no pass calculation in motor task.
      for(int n=0;n<4 && predicting;++n) {
        if(!validUTC() || !validSite() || !propagate(predictionTime)) {
          predicting=false; passes.clear(); break;
        }
        double elevation=orbit.satEl;
        if(elevation>=0 && !above) {
          above=true; activePass={predictionTime,0,predictionTime,elevation,
            predictionTime==predictionEnd-86400};
        }
        if(above && elevation>activePass.maxEl) {
          activePass.maxEl=elevation; activePass.peak=predictionTime;
        }
        if(elevation<0 && above) {
          activePass.los=predictionTime; passes.push_back(activePass); above=false;
        }
        predictionTime+=10;
        if(predictionTime>predictionEnd) {
          if(above) { activePass.los=predictionEnd; activePass.partial=true; passes.push_back(activePass); }
          predicting=false;
        }
      }
    }
  }
  server.handleClient(); delay(1);
}
