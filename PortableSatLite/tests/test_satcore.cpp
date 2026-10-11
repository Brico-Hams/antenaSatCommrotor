// Reads cases from stdin: up(3) mag(3) decl az el  -> prints rotor az/el and round-trip az/el
#include "../firmware/lib/satcore/satcore.h"
#include <stdio.h>
using namespace satcore;
int main() {
  double ux,uy,uz,mx,my,mz,decl,az,el,hd;
  while (scanf("%lf %lf %lf %lf %lf %lf %lf %lf %lf %lf",&ux,&uy,&uz,&mx,&my,&mz,&decl,&az,&el,&hd)==10) {
    Frame f = frame_from_sensors({ux,uy,uz},{mx,my,mz},decl);
    Frame fh = frame_from_heading({ux,uy,uz}, hd);
    double ar, er, a2, e2; target_to_rotor(f, az, el, ar, er); rotor_to_target(f, ar, er, a2, e2);
    double ah, eh; target_to_rotor(fh, az, el, ah, eh); printf("%.9f %.9f %.9f %.9f %.9f %.9f\n", ar, er, a2, e2, ah, eh);
  }
}
