const fs=require('node:fs'),path=require('node:path'),validate=require('./mechanical-stl.cjs');
const root=path.join(__dirname,'..');
const shared={output_flange:2,saddle20:1,radio_cradle:1,
 diplexor_box:1,diplexor_lid:1,antenna_hub:4,band_bridge:1,arm_socket:16,
 limit_bracket:4,magnet_holder:2};
const fresh={base:1,cup608:4,cup6000:4,encoder_support:2};
let volume=0;
for(const [name,count] of Object.entries(shared))volume+=validate(path.join(root,'cad','stl',name+'.stl')).volume*count;
for(const [name,count] of Object.entries(fresh))volume+=validate(path.join(root,'cad','belt-stl',name+'.stl')).volume*count;
for(const [name,count] of Object.entries({base:1,lid:1,port40:2,port30:2}))
 volume+=validate(path.join(root,'cad','carrier-stl',name+'.stl')).volume*count;
const ancillary={
 motors:[.24,.36],eightMetalPulleys:[.16,.24],fourBelts:[.020,.035],
 eightBearings:[.130,.150],steelShafts:[.169,.169],
 fourMetalPlatesAndElSupportTray:[.680,.780],standoffsFastenersKeysUbolts:[.150,.250],
 stationaryCarrierMetalTray:[.254,.254],
 antennaMetalFiberglassCoaxRf:[.360,.580],controllerAndPortablePower:[.350,.580]
};
const range=[0,0];for(const r of Object.values(ancillary)){range[0]+=r[0];range[1]+=r[1];}
const asaSolid=volume/1e6*1.07;
console.log(JSON.stringify({variant:'BASE belt 25:1',solidEquivalentAsaKg:asaSolid,
 illustrative75percentMaterialFractionAsaKg:asaSolid*.75,
 ancillaryPlanningKg:ancillary,totalSolidPlanningKg:range.map(v=>v+asaSolid),
 totalIllustrative75percentKg:range.map(v=>v+asaSolid*.75),
 measured:false,procurementDrawingsValidated:false,includesBattery:true,excludesRadioTripod:true},null,2));
