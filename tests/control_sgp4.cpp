#include <cmath>
#include <cstdio>
#include <cstring>
#include "sgp4io.h"
#include "sgp4unit.h"
int main() {
  // Vallado/CelesTrak verification satellite 00005, WGS72, improved operation.
  char one[130]="1 00005U 58002B   00179.78495062  .00000023  00000-0  28098-4 0  4753";
  char two[130]="2 00005  34.2682 348.7242 1859667 331.7664  19.3264 10.82419157413667";
  elsetrec record{};
  twoline2rv(one,two,'i',wgs72,record);
  double r[3],v[3];
  if(!sgp4(wgs72,record,0,r,v) || record.error) return 1;
  const double expectedR[]={7022.46529266,-1400.08296755,0.03995155};
  const double expectedV[]={1.893841015,6.405893759,4.534807250};
  for(int i=0;i<3;++i) {
    if(std::fabs(r[i]-expectedR[i])>0.001 || std::fabs(v[i]-expectedV[i])>0.000001) {
      std::printf("SGP4 mismatch axis %d r=%.9f v=%.9f\n",i,r[i],v[i]); return 2;
    }
  }
  std::puts("control_sgp4: published Vallado epoch vector PASS");
  char blankOne[130]="1 00005U 58002B   00179.78495062  .00000023  00000 0  00000 0 0  4753";
  char blankTwo[130]="2 00005  34.2682 348.7242 1859667 331.7664  19.3264 10.82419157413667";
  elsetrec blank{};
  twoline2rv(blankOne,blankTwo,'i',wgs72,blank);
  if(blank.nddot!=0 || blank.bstar!=0 || !sgp4(wgs72,blank,0,r,v) || blank.error) return 3;
  std::puts("control_sgp4: blank positive exponent fields PASS");
}
