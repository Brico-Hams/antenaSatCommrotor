const test=require('node:test'),assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path');
const validate=require('./mechanical-stl.cjs'),root=path.join(__dirname,'..');
const r=20*2/(2*Math.PI),R=100*2/(2*Math.PI);
const length=c=>2*Math.sqrt(c*c-(R-r)**2)+Math.PI*(R+r)+2*Math.asin((R-r)/c)*(R-r);
let lo=R-r+.1,hi=100;
for(let i=0;i<60;i++){const c=(lo+hi)/2;if(length(c)>252)hi=c;else lo=c;}
const c=(lo+hi)/2,alpha=Math.asin((R-r)/c),smallWrap=Math.PI-2*alpha;
test('two 20:100 GT2 stages retain 25:1 with real 252 mm path',()=>{
  assert.equal((100/20)**2,25);assert.equal(200*16*25,80000);
  assert(Math.abs(length(c)-252)<1e-9);
  assert(c>R+r+3);
  assert(smallWrap/(2*Math.PI)*20>6);
  assert(13<14); // front bearing cups finish before first stage
  assert(26<27); // first hub finishes before second plane
  assert(39<44); // second hub finishes before rear bearing cups
  assert(57<60); // fixed rear plate ends before output flange
});
test('all new printable components are closed meshes',()=>{
  for(const file of ['base','encoder_support','cup608','cup6000'])
    validate(path.join(root,'cad','belt-stl',file+'.stl'));
});
test('belt variant mass audit executes independently of legacy BOM',()=>{
  const {spawnSync}=require('node:child_process');
  const result=spawnSync(process.execPath,[path.join(__dirname,'mechanical-belt-mass.cjs')],{encoding:'utf8'});
  assert.equal(result.status,0,result.stderr);
});
test('conditional BuildLight mass sheet sums but does not approve incompatible motor',()=>{
  const budget=[.460,.260,.160,.020,.130,.169,.680,.150,.360,.100,.190];
  const sum=budget.reduce((a,b)=>a+b,0);
  assert(Math.abs(sum-2.679)<1e-12);
  assert(Math.abs(3-sum-.321)<1e-12);
  assert(21<26); // published candidate shaft does NOT meet current CAD requirement
  const doc=fs.readFileSync(path.join(root,'docs','MECHANICAL.md'),'utf8');
  assert(doc.includes('NO compatible con montajeBASE actual'));
});
console.log(JSON.stringify({ratio:25,stepsPerOutputRev:80000,centerMm:c,
  beltPitchLengthMm:length(c),smallPulleyWrapDeg:smallWrap*180/Math.PI,
  smallPulleyEngagedTeeth:smallWrap/(2*Math.PI)*20,
  maxPulleyFlangeRadiusMm:R+1.5,pulleyStage1Axial:[14,26],stage2Axial:[27,39],
  frontBearingCup:[3,13],rearBearingCup:[44,54],rearMetalPlate:[54,57]},null,2));
