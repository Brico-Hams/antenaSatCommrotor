// satcore.h - hardware-independent pointing, orientation and Doppler maths (header-only, no Arduino deps).
// Conventions: angles in degrees at the API, radians internally.
// Body frame B (rotor base, fixed to the tripod head): x = rotor zero-azimuth direction ("forward"), y = right, z = down.
// Sensors: accelerometer u_b = unit vector UP expressed in B (static reading, accel measures +1 g upward).
//          magnetometer m_b = Earth field in B (any units).
// declination_deg: NOAA convention, positive when MAGNETIC north is EAST of TRUE north (e.g. +1.0 deg in Murcia area is NOT assumed; look it up).
#pragma once
#include <math.h>
namespace satcore {
struct V3 { double x, y, z; };
static inline V3 add(V3 a, V3 b) { return {a.x + b.x, a.y + b.y, a.z + b.z}; }
static inline V3 mul(V3 a, double s) { return {a.x * s, a.y * s, a.z * s}; }
static inline double dot(V3 a, V3 b) { return a.x * b.x + a.y * b.y + a.z * b.z; }
static inline V3 cross(V3 a, V3 b) { return {a.y * b.z - a.z * b.y, a.z * b.x - a.x * b.z, a.x * b.y - a.y * b.x}; }
static inline double norm(V3 a) { return sqrt(dot(a, a)); }
static inline V3 unit(V3 a) { double n = norm(a); return n > 0 ? mul(a, 1.0 / n) : a; }
static const double D2R = M_PI / 180.0, R2D = 180.0 / M_PI;

// Local frame (E,N,U axes as unit vectors in body coordinates). TRUE north.
struct Frame { V3 e, n, u; bool valid; };

// up: accelerometer unit vector; mag: magnetometer vector; declination: magnetic north is declination_deg EAST of true north.
// Magnetic field points to magnetic north (plus dip). Returns frame whose n axis points to TRUE north.
static inline Frame frame_from_sensors(V3 up, V3 mag, double declination_deg) {
  Frame f{{0,0,0},{0,0,0},{0,0,0}, false};
  V3 u = unit(up);
  V3 down = mul(u, -1.0);
  V3 east_m = cross(down, mag);                   // E = D x N  (N has the horizontal part of mag)
  if (norm(east_m) < 1e-9) return f;              // field parallel to gravity: no heading
  east_m = unit(east_m);
  V3 north_m = cross(east_m, down);               // N = E x D
  double d = declination_deg * D2R;
  // True north lies west of magnetic north by declination (if declination is east-positive: magnetic north east of true).
  // true_north = north_m*cos(d) - east_m*sin(d)
  f.n = add(mul(north_m, cos(d)), mul(east_m, -sin(d)));
  f.e = add(mul(east_m, cos(d)), mul(north_m, sin(d)));
  f.u = u; f.valid = true; return f;
}

// Frame from gravity + a known heading: true azimuth (deg, clockwise from north) of the rotor zero direction (body x projected on the horizontal).
static inline Frame frame_from_heading(V3 up, double heading_deg) {
  Frame f{{0,0,0},{0,0,0},{0,0,0}, false};
  V3 u = unit(up), x = {1, 0, 0};
  V3 fh = {x.x - dot(x, u) * u.x, x.y - dot(x, u) * u.y, x.z - dot(x, u) * u.z};
  if (norm(fh) < 1e-9) return f;                                  // forward axis vertical: heading undefined
  fh = unit(fh); V3 r = cross(mul(u, -1.0), fh); double h = heading_deg * D2R;
  f.n = add(mul(fh, cos(h)), mul(r, -sin(h))); f.e = add(mul(fh, sin(h)), mul(r, cos(h))); f.u = u; f.valid = true; return f;
}

// Target (true azimuth clockwise from north, elevation) -> rotor axis angles.
// az_r: clockwise from body x seen from above (0..360). el_r: elevation above the base plane (-90..90).
static inline void target_to_rotor(const Frame &f, double az_deg, double el_deg, double &az_r, double &el_r) {
  double az = az_deg * D2R, el = el_deg * D2R;
  double te = cos(el) * sin(az), tn = cos(el) * cos(az), tu = sin(el);
  V3 t = add(add(mul(f.e, te), mul(f.n, tn)), mul(f.u, tu));   // target direction in body frame (x fwd, y right, z down)
  double h = hypot(t.x, t.y);
  az_r = atan2(t.y, t.x) * R2D; if (az_r < 0) az_r += 360.0;
  el_r = atan2(-t.z, h) * R2D;                                 // up = -z
}

// Inverse: rotor axis angles -> true az/el (used to display where the antenna really points).
static inline void rotor_to_target(const Frame &f, double az_r, double el_r, double &az, double &el) {
  double a = az_r * D2R, e = el_r * D2R;
  V3 t = {cos(e) * cos(a), cos(e) * sin(a), -sin(e)};          // body x,y,z(down)
  double te = dot(t, f.e), tn = dot(t, f.n), tu = dot(t, f.u);
  az = atan2(te, tn) * R2D; if (az < 0) az += 360.0;
  el = atan2(tu, hypot(te, tn)) * R2D;
}

// Choose the cable-friendly AZ command in [0, az_max] (e.g. 450) closest to the current position.
static inline double unwrap_az(double want_deg, double current_deg, double az_max_deg) {
  double best = want_deg, bd = 1e9;
  for (int k = -1; k <= 2; k++) {
    double c = want_deg + 360.0 * k;
    if (c < 0 || c > az_max_deg) continue;
    double d = fabs(c - current_deg);
    if (d < bd) { bd = d; best = c; }
  }
  return best;
}
// Flip (over-the-top) for passes near the zenith: same pointing with az+180 and el = 180 - el.
static inline void flip(double az_r, double el_r, double &az_f, double &el_f) {
  az_f = fmod(az_r + 180.0, 360.0); el_f = 180.0 - el_r;
}

// Doppler. range_rate_km_s > 0 when receding. Returns the frequency received on the ground for a satellite transmitting f0.
static inline double doppler_rx(double f0_hz, double range_rate_km_s) { return f0_hz * (1.0 - range_rate_km_s / 299792.458); }
// Frequency the ground station must transmit so the satellite receives f0.
static inline double doppler_tx(double f0_hz, double range_rate_km_s) { return f0_hz * (1.0 + range_rate_km_s / 299792.458); }
}  // namespace satcore
