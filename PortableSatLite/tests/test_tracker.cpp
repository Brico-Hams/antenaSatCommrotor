#include <Arduino.h>
#include "tracker.h"
int main(int argc, char **argv) {
  Tracker t; double lat = atof(argv[1]), lon = atof(argv[2]); unsigned long t0 = strtoul(argv[3], 0, 10); double minel = atof(argv[4]); double mask = 0.0;
  t.load("ISS", "1 25544U 98067A   19343.69339541  .00001764  00000-0  38792-4 0  9991", "2 25544  51.6439 211.2001 0007417  17.6667  85.6398 15.50103472202482", lat, lon, 100);
  static PassInfo ps[16]; int n = t.find_passes(t0, 36.0, mask, minel, ps, 16);
  for (int k = 0; k < n; k++) { PassInfo &p = ps[k]; Sample s; t.sample(p.tca, s);
    printf("%lu %lu %lu %.2f %.1f %.1f %.1f %.4f\n", p.aos, p.tca, p.los, p.max_el, p.az_aos, p.az_tca, p.az_los, s.range_rate_kms); }
}
