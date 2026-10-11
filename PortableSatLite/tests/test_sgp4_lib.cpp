// Host test of the Hopperpop Sgp4 library used by the firmware (needs Arduino.h stub). Prints az el range lat lon for given unix times.
#include <Arduino.h>
#include "Sgp4.h"
int main(int argc, char** argv) {
  char l1[130] = "1 25544U 98067A   19343.69339541  .00001764  00000-0  38792-4 0  9991";
  char l2[130] = "2 25544  51.6439 211.2001 0007417  17.6667  85.6398 15.50103472202482";
  Sgp4 sat; sat.site(38.0, -1.3, 100); sat.init("ISS", l1, l2);
  for (int i = 1; i < argc; i++) { unsigned long t = strtoul(argv[i], 0, 10); sat.findsat(t); printf("%lu %.6f %.6f %.4f %.6f %.6f\n", t, sat.satAz, sat.satEl, sat.satDist, sat.satLat, sat.satLon); }
}
