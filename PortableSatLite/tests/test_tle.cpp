#include "tle.h"
#include <stdio.h>
int main() {
  const char *al[] = {"ISS;ZARYA", "SO-50;SAUDISAT 1C", "AO-91;FOX-1B"};
  const char *txt =
    "ISS (ZARYA)\r\n1 25544U 98067A   19343.69339541  .00001764  00000-0  38792-4 0  9991\r\n2 25544  51.6439 211.2001 0007417  17.6667  85.6398 15.50103472202482\r\n"
    "RANDOM SAT\r\n1 25544U 98067A   19343.69339541  .00001764  00000-0  38792-4 0  9991\r\n2 25544  51.6439 211.2001 0007417  17.6667  85.6398 15.50103472202482\r\n"
    "ISS (ZARYA)\r\n1 25544U 98067A   19343.69339541  .00001764  00000-0  38792-4 0  9990\r\n2 25544  51.6439 211.2001 0007417  17.6667  85.6398 15.50103472202482\r\n";   // bad checksum -> rejected
  TleEntry out[8]; int count = 0; int n = tle::parse(txt, al, 3, out, 8, count);
  printf("%d %d %s %lu\n", n, count, out[0].name, out[0].epoch_unix);
}
