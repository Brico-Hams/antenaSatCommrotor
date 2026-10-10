#include <unity.h>
#include "../../../firmware/include/control_logic.h"
#include "../../../firmware/include/ble_protocol.h"
using namespace Control;
void setUp() {}
void tearDown() {}
void ranges() {
  TEST_ASSERT_EQUAL_INT(80000,stepsPerRevolution);
  TEST_ASSERT_TRUE(inRange(-180,0)); TEST_ASSERT_TRUE(inRange(180,90));
  TEST_ASSERT_FALSE(inRange(180.01,45)); TEST_ASSERT_FALSE(inRange(0,-.01));
  TEST_ASSERT_FALSE(inRange(NAN,0));
  double a; TEST_ASSERT_TRUE(mechanicalAz(350,10,a)); TEST_ASSERT_EQUAL_FLOAT(-20,a);
  mechanicalAz(10,350,a); TEST_ASSERT_EQUAL_FLOAT(20,a);
  TEST_ASSERT_FALSE(mechanicalAz(NAN,0,a));
}
void credentials() {
  TEST_ASSERT_TRUE(validCredentials("station","long-password","abcdefghijklmnopqrstuvwx"));
  TEST_ASSERT_FALSE(validCredentials("station","","abcdefghijklmnopqrstuvwx"));
  TEST_ASSERT_FALSE(validCredentials("station","long-password","short"));
  TEST_ASSERT_FALSE(validCredentials("","long-password","abcdefghijklmnopqrstuvwx"));
  TEST_ASSERT_FALSE(validCredentials("station","long-password\n","abcdefghijklmnopqrstuvwx"));
}
void bleFrames() {
  ControlBLE::Assembler parser;
  uint8_t first[]={0x53,1,0,0,'{','}'};
  uint8_t end[]={0x53,2,1,0,'\n'};
  TEST_ASSERT_EQUAL_INT(0,parser.feed(first,sizeof(first)));
  TEST_ASSERT_EQUAL_INT(1,parser.feed(end,sizeof(end)));
  TEST_ASSERT_EQUAL_STRING("{}\n",parser.data);
  parser.reset(); end[2]=2;
  TEST_ASSERT_EQUAL_INT(-1,parser.feed(end,sizeof(end)));
  TEST_ASSERT_EQUAL_INT(0,parser.feed(first,sizeof(first)));
  TEST_ASSERT_EQUAL_INT(-1,parser.feed(first,sizeof(first))); // interleaved START
  uint8_t single[]={0x53,3,0,0,'{','}'};
  TEST_ASSERT_EQUAL_INT(1,parser.feed(single,sizeof(single))); parser.reset();
  single[5]=0; TEST_ASSERT_EQUAL_INT(-1,parser.feed(single,sizeof(single)));
  uint8_t frame[20]={0x53,1,0,0};
  memset(frame+4,'x',16);
  for(int n=0;n<128;++n) {
    frame[1]=n==0?1:0; frame[2]=n; frame[3]=0;
    TEST_ASSERT_EQUAL_INT(0,parser.feed(frame,20));
  }
  frame[2]=128; TEST_ASSERT_EQUAL_INT(-1,parser.feed(frame,20)); // max2048
  TEST_ASSERT_TRUE(ControlBLE::validPasskey(100000));
  TEST_ASSERT_TRUE(ControlBLE::validPasskey(999999));
  TEST_ASSERT_FALSE(ControlBLE::validPasskey(12345));
  const char *token="abcdefghijklmnopqrstuvwx";
  TEST_ASSERT_TRUE(ControlBLE::authorized(false,true,token,token));
  TEST_ASSERT_FALSE(ControlBLE::authorized(true,true,token,token));
  TEST_ASSERT_FALSE(ControlBLE::authorized(false,false,token,token));
  TEST_ASSERT_FALSE(ControlBLE::authorized(false,true,token,"abcdefghijklmnopqrstuvwy"));
  TEST_ASSERT_FALSE(ControlBLE::authorized(false,true,"",""));
}
void epochs() {
  TEST_ASSERT_EQUAL_INT64(1704067200,utc(2024,1,1,0,0,0));
  TEST_ASSERT_EQUAL_INT64(1709164800,utc(2024,2,29,0,0,0));
  TEST_ASSERT_EQUAL_INT64(0,utc(2025,2,29,0,0,0));
  TEST_ASSERT_EQUAL_INT64(0,utc(2024,1,1,24,0,0));
  TEST_ASSERT_TRUE(fresh(2000000,2000000));
  TEST_ASSERT_TRUE(fresh(2000000,2000000-maxTleAge));
  TEST_ASSERT_FALSE(fresh(2000000,2000000-maxTleAge-1));
  TEST_ASSERT_FALSE(fresh(2000000,2000000+86401));
  TEST_ASSERT_FALSE(fresh(0,100));
}
void tleValidation() {
  // Vallado published SGP4 test case 00005; checksum valid.
  const char *one="1 00005U 58002B   00179.78495062  .00000023  00000-0  28098-4 0  4753";
  const char *two="2 00005  34.2682 348.7242 1859667 331.7664  19.3264 10.82419157413667";
  TEST_ASSERT_TRUE(validTle(one,two));
  char damaged[70]; std::strcpy(damaged,two); damaged[68]='0';
  TEST_ASSERT_FALSE(validTle(one,damaged));
  TEST_ASSERT_FALSE(validTle("1 short",two));
  TEST_ASSERT_EQUAL_INT64(962131819,tleEpoch(one));
  char blankExponent[70]; std::strcpy(blankExponent,one);
  // Standard TLE blank exponent sign is positive, e.g. AMSAT zero fields.
  blankExponent[50]=' '; blankExponent[51]='0';
  blankExponent[59]=' '; blankExponent[60]='0';
  int sum=0;
  for(int i=0;i<68;++i) {
    if(blankExponent[i]>='0' && blankExponent[i]<='9')sum+=blankExponent[i]-'0';
    if(blankExponent[i]=='-')++sum;
  }
  blankExponent[68]='0'+sum%10;
  TEST_ASSERT_TRUE(validTle(blankExponent,two));
  blankExponent[50]='X';
  TEST_ASSERT_FALSE(validTle(blankExponent,two));
}
void motion() {
  Axis axis; axis.target=1000;
  double previous=0;
  for(int n=0;n<20000;++n) {
    int step=axis.tick(.001);
    TEST_ASSERT_TRUE(std::abs(step)<=1);
    TEST_ASSERT_TRUE(std::fabs(axis.speed)<=maxRate);
    TEST_ASSERT_TRUE(std::fabs(axis.speed-previous)<=acceleration*.001+.000001);
    previous=axis.speed;
  }
  TEST_ASSERT_INT_WITHIN(1,1000,axis.position);
  axis.stop(); TEST_ASSERT_EQUAL_FLOAT(0,axis.speed);
  TEST_ASSERT_EQUAL_INT(0,axis.tick(.1));
  axis.target=-1000;
  for(int n=0;n<20000;++n)axis.tick(.001);
  TEST_ASSERT_INT_WITHIN(1,-1000,axis.position);
}
int main() {
  UNITY_BEGIN(); RUN_TEST(ranges); RUN_TEST(credentials); RUN_TEST(bleFrames);
  RUN_TEST(epochs); RUN_TEST(tleValidation); RUN_TEST(motion);
  return UNITY_END();
}
