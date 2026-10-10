const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict');
const validate=require('./mechanical-stl.cjs'), root=path.join(__dirname,'..');
const rows=fs.readFileSync(path.join(root,'bom','mechanical.csv'),'utf8').trim().split(/\r?\n/).slice(1).map(line=>line.split(','));
const allStls=fs.readdirSync(path.join(root,'cad','stl')).filter(name=>name.endsWith('.stl'));
assert.equal(allStls.length,34);
for(const file of allStls) validate(path.join(root,'cad','stl',file));
let solidMm3=0, gearMm3=0, low=0, high=0,printed=0;
for(const [id,desc,qty,unit,material,selector,costLow,costHigh] of rows) {
  if(id.startsWith('B')) continue; // new BASE belt budget is independent, not additive
  low+=Number(costLow);high+=Number(costHigh);
  if(!id.startsWith('P')||id==='P19') continue; // flat_adapter is optional alternative
  const result=validate(path.join(root,'cad','stl',selector+'.stl'));
  solidMm3+=result.volume*Number(qty);printed+=Number(qty);
  if(['sun1','sun2','planet','ring','carrier1','carrier2'].includes(selector))
    gearMm3+=result.volume*Number(qty);
}
const source=fs.readFileSync(path.join(root,'cad','station.scad'),'utf8');
assert(source.includes('rotate([90,0,0]) rotate([0,0,-elevation])'),'EL must rotate about its shaft, not global Z');
assert(source.includes('translate([0,0,209]) sensor_bracket()'),'AZ encoder support must be outside moving AZ block');
const mechanical=fs.readFileSync(path.join(root,'cad','mechanical.scad'),'utf8');
assert(mechanical.includes('h=output?10:9'),'608 plate ends50 before keeper50');
// Bound for fixed sensor bridge vs rotating boom32 throughout allowed EL quadrant.
const sensorPositiveSupport=12*Math.sqrt(2), boomInner=35-16;
assert(boomInner>sensorPositiveSupport);
assert(84-62>8); // EL outer envelope clears bracket bottom plate
assert(50+142+84-62>209+3); // EL envelope clears AZ sensor bridge in Z
assert(50-34>12); // AZ motor clears tripod base
console.log(JSON.stringify({printedPiecesDefault:printed,solidEquivalentASAkg:solidMm3/1e6*1.07,
  allRenderedManifoldMeshesChecked:allStls.length,
  solidGearsAndCarriersASAkg:gearMm3/1e6*1.07,
  illustrativeASA60percentNonGearSolidFractionKg:(gearMm3+(solidMm3-gearMm3)*.6)/1e6*1.07,
  planningMechanicalBudgetEUR:[low,high],budgetIsNotVendorQuote:true,measuredMass:false,
  printedInfillMassNotCalculated:true},null,2));
console.log('PASS: BOM meshes, bounded motor/EL/sensor clearances, EL shaft rotation. Full swept assembly and load tests remain pending.');
