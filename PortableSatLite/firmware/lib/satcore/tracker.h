// tracker.h - satellite sampling + pass prediction on top of Hopperpop/Sgp4-Library (MIT). Host-testable (see tests/test_tracker.*).
#pragma once
#include "Sgp4.h"
#include "satcore.h"
struct PassInfo { unsigned long aos, tca, los; float max_el, az_aos, az_tca, az_los; };
struct Sample { double az, el, range_km, range_rate_kms, lat, lon, alt_km; };
class Tracker {
 public:
  Sgp4 sat;
  bool loaded = false;
  // lat/lon in degrees (east positive), alt in metres.
  bool load(const char *name, const char *l1, const char *l2, double lat, double lon, double alt_m) {
    char a[130], b[130]; strncpy(a, l1, 129); a[129] = 0; strncpy(b, l2, 129); b[129] = 0;
    sat.site(lat, lon, alt_m);
    loaded = sat.init(name, a, b);
    return loaded;
  }
  // Position at unix time t; range rate from a symmetric +-1 s difference (km/s, positive = receding).
  bool sample(unsigned long t, Sample &s) {
    if (!loaded) return false;
    sat.findsat(t - 1); double r0 = sat.satDist;
    sat.findsat(t + 1); double r1 = sat.satDist;
    sat.findsat(t);
    s.az = sat.satAz; s.el = sat.satEl; s.range_km = sat.satDist; s.range_rate_kms = (r1 - r0) / 2.0;
    s.lat = sat.satLat; s.lon = sat.satLon; s.alt_km = sat.satAlt; return true;
  }
  // Next pass above min_el. iterations = number of orbits to search (e.g. 30 = 2 days for LEO).
  // Own pass finder (ADR-009): the library's nextpass() steps one orbit at a time and SKIPS low passes (measured: 3 of 7 missed in tests).
  // Sweep every step_s seconds over [from, from+hours], mask = horizon mask (deg) that defines AOS/LOS, keep passes whose max elevation >= min_max_el.
  int find_passes(unsigned long from, double hours, double mask, double min_max_el, PassInfo *out, int max_n, int step_s = 30) {
    if (!loaded) return 0;
    int n = 0; unsigned long end = from + (unsigned long)(hours * 3600.0);
    sat.findsat(from); bool up = sat.satEl > mask; unsigned long aos = up ? from : 0;
    for (unsigned long t = from + step_s; t <= end && n < max_n; t += step_s) {
      sat.findsat(t); bool now = sat.satEl > mask;
      if (now && !up) aos = refine(t - step_s, t, mask, true);
      if (!now && up) {
        unsigned long los = refine(t - step_s, t, mask, false), tca = aos, best_t = aos; double best = -90;
        for (unsigned long u = aos; u <= los; u += 5) { sat.findsat(u); if (sat.satEl > best) { best = sat.satEl; best_t = u; } }
        tca = best_t;
        if (best >= min_max_el && aos) {
          PassInfo p; p.aos = aos; p.los = los; p.tca = tca; p.max_el = (float)best;
          sat.findsat(aos); p.az_aos = (float)sat.satAz; sat.findsat(tca); p.az_tca = (float)sat.satAz; sat.findsat(los); p.az_los = (float)sat.satAz; out[n++] = p;
        }
      }
      up = now;
    }
    return n;
  }
 private:
  // bisection of the elevation=mask crossing between t0 (state !rising) and t1; returns the first second above (rising) / last second above (setting)
  unsigned long refine(unsigned long t0, unsigned long t1, double mask, bool rising) {
    while (t1 - t0 > 1) {
      unsigned long m = t0 + (t1 - t0) / 2; sat.findsat(m); bool above = sat.satEl > mask;
      if (above == rising) t1 = m; else t0 = m;
    }
    return rising ? t1 : t0;
  }
};
