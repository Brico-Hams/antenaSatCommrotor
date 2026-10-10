const test=require('node:test'),assert=require('node:assert/strict');
const fs=require('node:fs'),path=require('node:path'),validate=require('./mechanical-stl.cjs');
const root=path.join(__dirname,'..');
const old={tripod_base:233270.3,enclosure_lid:27191.2,diplexor_lid:16691.2};
test('bounded mass optimization preserves valid impacted meshes and reduces material',()=>{
  let saved=0;
  for(const [selector,before] of Object.entries(old)) {
    const after=validate(path.join(root,'cad','stl',selector+'.stl')).volume;
    assert(after<before); saved+=before-after;
  }
  assert(saved>110000);
});
// Nominal metal geometry, not scale readings or vendor specified masses.
const cylinderKg=(d,length,rho=7.85)=>Math.PI*d*d/4*length*rho/1e6;
const shaftKg=2*cylinderKg(8,36)+2*cylinderKg(10,77);
const tieRodsKg=6*cylinderKg(3,180)+6*cylinderKg(3,130);
const shoulderKg=12*cylinderKg(4,23);
console.log(JSON.stringify({nominalSteelShaftKg:shaftKg,nominalTieRodsKg:tieRodsKg,
  nominalShoulderKg:shoulderKg,
  ancillaryMassKgPlanningRanges:{
    motors:[.24,.40],bearings:[.09,.12],steelShafts:[shaftKg,shaftKg],
    tieRods:[tieRodsKg,tieRodsKg],shoulders:[shoulderKg,shoulderKg],
    bushesPinsFastenersUboltsTripodAdapter:[.12,.22],
    aluminumRfRodsSleevesFiberglassBooms:[.25,.40],
    coaxHybridsDiplexorLiner:[.18,.30],controllerDriversWiring:[.08,.15],
    portablePower:[.25,.45]
  },measuredMass:false,includesPower:true,excludesTripodAndRadio:true},null,2));
test('nominal steel output shafts and tie rods retain truthful mass estimates',()=>{
  assert(shaftKg>.12&&shaftKg<.13);assert(tieRodsKg>.1&&tieRodsKg<.11);
  assert(fs.readFileSync(path.join(root,'cad','parameters.scad'),'utf8').includes('sun_teeth = 18'));
});
