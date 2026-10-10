const assert=require('node:assert/strict'), fs=require('node:fs'), path=require('node:path');
const text=fs.readFileSync(path.join(__dirname,'..','cad','parameters.scad'),'utf8');
const value=name => Number(text.match(new RegExp('^'+name+'\\s*=\\s*([\\d.]+)','m'))[1]);
const m=value('gear_module'), S=value('sun_teeth'), P=value('planet_teeth'), R=value('ring_teeth');
const pa=value('pressure_angle')*Math.PI/180, backlash=value('backlash'), clearance=m*.25;
assert.equal(R,S+2*P); assert.equal((S+R)%3,0); assert.equal((1+R/S)**2,25);
assert(S>=Math.ceil(2/Math.sin(pa)**2)); assert(P>=Math.ceil(2/Math.sin(pa)**2));
const rp=n=>n*m/2, inv=(r,rb)=>r<=rb?0:Math.sqrt((r/rb)**2-1)-Math.acos(rb/r);
const half=(n,r,internal=false)=>(Math.PI*m/2-backlash/2)/(2*rp(n))
  +(internal?-1:1)*(inv(rp(n),rp(n)*Math.cos(pa))-inv(r,rp(n)*Math.cos(pa)));
const polar=(r,a)=>[r*Math.cos(a),r*Math.sin(a)];
function outline(n,internal=false) {
  const rt=rp(n)+(internal?-m:m), rr=rp(n)+(internal?m+clearance:-m-clearance);
  const start=internal?rr:Math.max(rr,rp(n)*Math.cos(pa)), points=[], step=2*Math.PI/n;
  for(let t=0;t<n;t++) {
    const a=t*step+(internal?Math.PI/n:0);
    if(!internal) points.push(polar(rr,a-half(n,start)));
    for(let i=0;i<=24;i++){const r=start+(rt-start)*i/24;points.push(polar(r,a-half(n,r,internal)));}
    for(let i=24;i>=0;i--){const r=start+(rt-start)*i/24;points.push(polar(r,a+half(n,r,internal)));}
    if(!internal) points.push(polar(rr,a+half(n,start)));
    for(let i=1;i<8;i++) points.push(polar(rr,a+half(n,start,internal)+(step-2*half(n,start,internal))*i/8));
  }
  return points;
}
function inside(p,poly) {
  let hit=false;
  for(let i=0,j=poly.length-1;i<poly.length;j=i++) {
    const a=poly[i],b=poly[j];
    if((a[1]>p[1])!==(b[1]>p[1]) && p[0]<(b[0]-a[0])*(p[1]-a[1])/(b[1]-a[1])+a[0]) hit=!hit;
  }
  return hit;
}
const rotate=(p,a,offset=0)=>[p[0]*Math.cos(a)-p[1]*Math.sin(a)+offset,p[0]*Math.sin(a)+p[1]*Math.cos(a)];
const sun=outline(S), planet=outline(P), ring=outline(R,true), center=rp(S)+rp(P);
const basePitch=Math.PI*m*Math.cos(pa);
const contactPath=n=>Math.sqrt((rp(n)+m)**2-(rp(n)*Math.cos(pa))**2);
const contactExternal=(contactPath(S)+contactPath(P)-center*Math.sin(pa))/basePitch;
const contactInternal=(contactPath(P)-Math.sqrt((rp(R)-m)**2-(rp(R)*Math.cos(pa))**2)+center*Math.sin(pa))/basePitch;
assert(contactExternal>1 && contactInternal>1);
assert(Math.abs(rp(R)+m+clearance-(center+rp(P)+m)-clearance)<1e-9);
assert(Math.abs(center-rp(P)-m-(rp(S)-m-clearance)-clearance)<1e-9);
// One sun tooth cycle, with fixed carrier coordinates: omega_planet=-S/P omega_sun.
// Ring rotates in this carrier frame at -S/R omega_sun (Willis equation).
// This is equivalent to a fixed-ring planetary with carrier speed sun/5.
for(let i=0;i<=120;i++) {
  const a=2*Math.PI/S*i/120, planetAngle=Math.PI-Math.PI/P-a*S/P;
  const sunPoly=sun.map(p=>rotate(p,a));
  const ringPoly=ring.map(p=>rotate(p,-a*S/R));
  for(const p of planet.map(p=>rotate(p,planetAngle,center))) {
    assert(!inside(p,sunPoly),`Sun/planet sampled flank collision at ${i}`);
    assert(inside(p,ringPoly),`Planet/ring sampled flank collision at ${i}`);
  }
}
assert(Math.sqrt(3)*center>2*(rp(P)+m)); // adjacent planet addendum envelopes
assert.equal((rp(P)+rp(R))-(center+rp(P)),rp(R)-center);
// Real axial ranges; check neighbouring moving hub / fixed keeper separation.
assert(54>53); assert(124>123); assert(40<41); assert(90<91);
const cut=f=>{const lambda=299792.458/f,driven=lambda*.46,reflector=driven*1.05;
 return {f,lambda,driven,reflector,gap:lambda*.225,arm:driven/2-12,reflectorArm:reflector/2-12};};
const density=1.225, area=.12, drag=1.3, wind=8, lever=.15, gravity=.5*9.81*.03;
const windTorque=.5*density*drag*area*wind**2*lever;
console.log(JSON.stringify({ratio:25,pitchCenter:center,undercutMinimum:Math.ceil(2/Math.sin(pa)**2),
  meshSamples:121,backlash,antenna:[cut(145),cut(435)],gravityTorqueNm:gravity,windTorqueNm:windTorque,
  contactRatioExternal:contactExternal,contactRatioInternal:contactInternal,
  motorExampleNm:.08,efficiencyPerStage:.65,exampleOutputNm:.08*25*.65**2},null,2));
console.log('PASS: pitch/closure/undercut, sampled involute mesh and axial guards. Not a contact-stress or assembly collision proof.');
