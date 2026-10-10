/* Original carrier geometry and deterministic two-layer maze router.
 * No downloaded design is used. All electrical connections are explicit.
 */
const fs = require('fs'), path = require('path'), crypto = require('crypto');
const root = __dirname, uuid = () => crypto.randomUUID();
const nets = ['GND','RAW12','PROTECTED12','FUSED12','STOP_SEND','VMOT','BUCK12','BUCK5','FUSED5','ESP5','3V3',
  'AZ_STEP','AZ_DIR','EL_STEP','EL_DIR','ENABLE_N','STOP_N','AZ_MIN_N','AZ_MAX_N','EL_MIN_N','EL_MAX_N',
  'GNSS_TX','GNSS_RX','AZ_SDA','AZ_SCL','EL_SDA','EL_SCL','AZ_M2B','AZ_M2A','AZ_M1A','AZ_M1B',
  'EL_M2B','EL_M2A','EL_M1A','EL_M1B'];
const nid = n => n ? nets.indexOf(n)+1 : 0;
let parts=[];
function part(ref,value,x,y,pins,opts={}) {
  const p={ref,value,x,y,pins:pins.map((n,i)=>({num:i+1,net:n,x:opts.positions?opts.positions[i][0]:0,
    y:opts.positions?opts.positions[i][1]:i*(opts.pitch||2.54)})),...opts,id:uuid()};
  parts.push(p); return p;
}
const rows=(count,spacing,pitch=2.54)=>Array.from({length:count*2},(_,i)=>[i<count?0:spacing,(i%count)*pitch]);
part('J1','DC_IN_12V',12,18,['RAW12','GND'],{pitch:5.08,pad:3.2,drill:1.3,mpn:'Phoenix 1715721 MKDS 1,5/2-5.08',kind:'terminal'});
part('D1','SB560_REVERSE_BLOCK',22,18,['RAW12','PROTECTED12'],{positions:[[0,0],[15.24,0]],pad:2.8,drill:1.3,mpn:'onsemi SB560',kind:'diode'});
part('D2','SMBJ15A_TVS',44,18,['GND','FUSED12'],{positions:[[0,0],[4.3,0]],smd:true,pad:2.4,mpn:'Littelfuse SMBJ15A',kind:'tvs'});
part('F1','T3.15A_MAIN',12,33,['PROTECTED12','FUSED12'],{positions:[[0,0],[22.5,0]],pad:3.4,drill:1.4,mpn:'Schurter 0031.8201 + SPT 0001.2509',kind:'fuse'});
part('F2','T2.5A_MOTOR',12,48,['FUSED12','STOP_SEND'],{positions:[[0,0],[22.5,0]],pad:3.4,drill:1.4,mpn:'Schurter 0031.8201 + SPT 0001.2508',kind:'fuse'});
part('J2','LATCHED_STOP_POWER_OUT_RETURN',12,62,['STOP_SEND','VMOT'],{pitch:5.08,pad:3.2,drill:1.3,mpn:'Phoenix 1715721 MKDS 1,5/2-5.08',kind:'terminal'});
part('F4','T1A_BUCK_INPUT',42,34,['FUSED12','BUCK12'],{positions:[[0,0],[22.5,0]],pad:3.4,drill:1.4,mpn:'Schurter 0031.8201 + SPT 0001.2504',kind:'fuse'});
part('J4','EXTERNAL_BUCK_INPUT',45,48,['BUCK12','GND'],{pitch:5.08,pad:3.2,drill:1.3,mpn:'Phoenix 1715721 MKDS 1,5/2-5.08',kind:'terminal'});
part('J5','EXTERNAL_BUCK_5V_RETURN',45,62,['BUCK5','GND'],{pitch:5.08,pad:3.2,drill:1.3,mpn:'Phoenix 1715721 MKDS 1,5/2-5.08',kind:'terminal'});
part('F3','T1A_LOGIC_5V',12,77,['BUCK5','FUSED5'],{positions:[[0,0],[22.5,0]],pad:3.4,drill:1.4,mpn:'Schurter 0031.8201 + SPT 0001.2504',kind:'fuse'});
part('JP1','REMOVE_FOR_USB',43,76,['FUSED5','ESP5'],{mpn:'Samtec TSW-102-07-G-S + shunt',kind:'header'});
const left=['3V3',null,null,null,'STOP_N','AZ_MIN_N','EL_MAX_N',null,'ENABLE_N','AZ_STEP','AZ_DIR','EL_STEP',null,'GND','EL_DIR',null,null,null,'ESP5'];
const right=['GND',null,'AZ_SCL',null,null,'AZ_SDA','GND','EL_SCL','EL_SDA',null,'GNSS_RX','GNSS_TX',null,null,null,null,null,null,null];
part('U1','ESP32_DEVKITC_V4_38_WROOM32E',77,20,[...left,...right],{positions:rows(19,25.4),mpn:'Espressif ESP32-DevKitC-32E',kind:'module'});
for(const [ref,x,prefix] of [['U2',45,'AZ'],['U3',80,'EL']]) {
  part(ref,'WATTEROTT_TMC2209_V2',x,94,['ENABLE_N','3V3','3V3','GND',null,null,prefix+'_STEP',prefix+'_DIR',
    'VMOT','GND',prefix+'_M2B',prefix+'_M2A',prefix+'_M1A',prefix+'_M1B','3V3','GND'],
    {positions:rows(8,15.24),mpn:'Watterott SilentStepStick TMC2209 v2.x',kind:'driver'});
  part(ref==='U2'?'C1':'C2','220u_35V_LOW_ESR',x+18,84,['VMOT','GND'],{positions:[[0,0],[5,0]],pad:2.5,drill:1,mpn:'Panasonic EEU-FR1V221',kind:'capacitor'});
  part(ref==='U2'?'JM1':'JM2',prefix+'_MOTOR',x+5,120,[prefix+'_M2B',prefix+'_M2A',prefix+'_M1A',prefix+'_M1B'],
    {positions:[[0,0],[5.08,0],[10.16,0],[15.24,0]],pad:3.2,drill:1.3,mpn:'Phoenix 1715747 MKDS 1,5/4-5.08',kind:'terminal'});
}
part('J6','GNSS_3V3_UART',157,20,['3V3','GND','GNSS_TX','GNSS_RX'],{mpn:'JST B4B-XH-A',kind:'xh'});
part('J7','AZ_AS5600_I2C0',157,38,['3V3','GND','AZ_SDA','AZ_SCL'],{pitch:2.5,mpn:'JST B4B-XH-A',kind:'xh'});
part('J8','EL_AS5600_I2C1',157,56,['3V3','GND','EL_SDA','EL_SCL'],{pitch:2.5,mpn:'JST B4B-XH-A',kind:'xh'});
part('J9','OPTIONAL_IMU_MAG_I2C0',157,74,['3V3','GND','AZ_SDA','AZ_SCL'],{pitch:2.5,mpn:'JST B4B-XH-A',kind:'xh'});
for (const [i,n,y] of [[3,'STOP_N',92],[10,'AZ_MIN_N',103],[11,'AZ_MAX_N',114],[12,'EL_MIN_N',92],[13,'EL_MAX_N',103]]) {
  part('J'+i,n+'_NC_AUX_ONLY',i<12?157:137,y,[n,'GND'],{pitch:2.5,mpn:'JST B2B-XH-A',kind:'xh'});
}
// Input-only GPIO36 and GPIO39 are brought out explicitly in the left header.
parts.find(p=>p.ref==='U1').pins[2].net='AZ_MAX_N';
parts.find(p=>p.ref==='U1').pins[3].net='EL_MIN_N';
const pull=['ENABLE_N','STOP_N','AZ_MIN_N','AZ_MAX_N','EL_MIN_N','EL_MAX_N','AZ_SDA','AZ_SCL','EL_SDA','EL_SCL'];
pull.forEach((n,i)=>part('R'+(i+1),i<6?'10k':'4k7',119+(i%2)*12,25+Math.floor(i/2)*10,['3V3',n],
 {positions:[[0,0],[0,5.08]],pad:2,drill:.8,mpn:i<6?'Yageo CFR-25JB-52-10K':'Yageo CFR-25JB-52-4K7',kind:'resistor'}));
part('C3','100n_50V',147,18,['3V3','GND'],{positions:[[0,0],[0,5.08]],pad:2,drill:.8,mpn:'KEMET C315C104M5U5TA',kind:'capacitor'});
part('C4','100n_50V',147,38,['3V3','GND'],{positions:[[0,0],[0,5.08]],pad:2,drill:.8,mpn:'KEMET C315C104M5U5TA',kind:'capacitor'});
part('C5','100n_50V',147,56,['3V3','GND'],{positions:[[0,0],[0,5.08]],pad:2,drill:.8,mpn:'KEMET C315C104M5U5TA',kind:'capacitor'});
// J6 also uses XH's 2.50 mm pitch (not the 2.54 mm generic header).
parts.find(p=>p.ref==='J6').pins.forEach((p,i)=>p.y=i*2.5);
const esc=s=>s.replace(/\\/g,'\\\\').replace(/"/g,'\\"');
const num=x=>Number(x.toFixed(4));
const fpName=p=>'PortableSatCarrier:'+p.ref+'_'+p.kind;
const ncName=(p,q)=>`unconnected-(${p.ref}-NC-Pad${q.num})`;
for(const p of parts)for(const q of p.pins)if(!q.net)nets.push(ncName(p,q));
function footprint(p,standalone=false) {
  const pad=p.pad||1.8, dr=p.drill||1, xmax=Math.max(...p.pins.map(q=>q.x)),ymax=Math.max(...p.pins.map(q=>q.y));
  const bodyY=p.kind==='fuse'?4.8:p.kind==='capacitor'&&p.value.startsWith('220u')?5:
    p.kind==='terminal'&&ymax===0?4.8:p.kind==='xh'?2.5:1.8;
  const bodyX=(p.kind==='terminal'&&ymax>0)?4.8:p.kind==='xh'?4.5:1.8;
  return `(footprint "${fpName(p)}" (layer "F.Cu") ${standalone?'':`(at ${p.x} ${p.y}) (uuid "${p.id}")`}
    (property "Reference" "${p.ref}" (at ${num(xmax/2)} -3) (layer "F.SilkS") (effects (font (size 1 1)(thickness .15))))
    (property "Value" "${esc(p.value)}" (at 0 -5) (layer "F.Fab") (effects (font (size 1 1)(thickness .15))))
    (attr ${p.smd?'smd':'through_hole'})
    (fp_rect (start ${-bodyX} ${-bodyY}) (end ${num(xmax+bodyX)} ${num(ymax+bodyY)}) (stroke (width .15)(type default)) (layer "F.Fab"))
    (fp_rect (start ${-bodyX-.5} ${-bodyY-.5}) (end ${num(xmax+bodyX+.5)} ${num(ymax+bodyY+.5)}) (stroke (width .05)(type default)) (layer "F.CrtYd"))
    (fp_text user "1" (at -3.1 0) (layer "F.SilkS") (effects(font(size 1 1)(thickness .15))))
    ${p.pins.map(q=>`(pad "${q.num}" ${p.smd?'smd':'thru_hole'} ${q.num===1?'rect':'circle'} (at ${q.x} ${q.y}) (size ${pad} ${pad}) ${p.smd?'':`(drill ${dr})`} (layers ${p.smd?'"F.Cu" "F.Paste" "F.Mask"':'"*.Cu" "*.Mask"'}) ${!standalone?`(net ${nid(q.net||ncName(p,q))} "${q.net||ncName(p,q)}")`:''})`).join('\n')}
    ${p.kind==='fuse'?'(pad "" np_thru_hole circle (at 11.25 0) (size 2.7 2.7) (drill 2.7) (layers "*.Cu" "*.Mask"))':''}
    ${p.kind==='diode'||p.kind==='tvs'?`(fp_text user "K" (at ${xmax} -3) (layer "F.SilkS") (effects(font(size 1 1)(thickness .15))))`:''}
  )`;
}
// Conservative original deterministic router; all THT pads participate on both layers.
const step=.25, nx=721,ny=521,N=nx*ny,occ=[new Int16Array(N),new Int16Array(N)];
const allPads=parts.flatMap(p=>p.pins.map(q=>({...q,ref:p.ref,ax:p.x+q.x,ay:p.y+q.y,
  r:(p.pad||1.8)/2*(q.num===1?Math.SQRT2:1),drill:p.drill||1,smd:!!p.smd})));
for(const p of parts)if(p.kind==='fuse')allPads.push({ref:p.ref,num:0,net:null,ax:p.x+11.25,ay:p.y,r:1.35,drill:2.7,smd:false});
const idx=(x,y)=>y*nx+x, xy=k=>[k%nx,Math.floor(k/nx)];
function markCircle(layer,x,y,r,owner) {
  let a=Math.ceil(r/step);
  for(let dy=-a;dy<=a;dy++) for(let dx=-a;dx<=a;dx++) {
    let xx=Math.round(x/step)+dx, yy=Math.round(y/step)+dy;
    if(xx<0||yy<0||xx>=nx||yy>=ny)continue;
    if(Math.hypot(xx*step-x,yy*step-y)<=r+.01) {
      const k=idx(xx,yy); if(!occ[layer][k]||occ[layer][k]===owner)occ[layer][k]=owner; else occ[layer][k]=-1;
    }
  }
}
for(let l=0;l<2;l++)for(let y=0;y<ny;y++)for(let x=0;x<nx;x++)
  if(x*step<2||x*step>178||y*step<2||y*step>128||(x*step>72&&x*step<106&&y*step<19)||
    (x*step>80&&x*step<100&&y*step<27))occ[l][idx(x,y)]=-1;
for(const [x,y] of [[5,5],[175,5],[5,125],[175,125]])for(let l=0;l<2;l++)markCircle(l,x,y,3,-1);
for(const p of allPads)for(let l=0;l<(p.smd?1:2);l++)markCircle(l,p.ax,p.ay,p.r+.35,p.net?nid(p.net):-1);
const holeBlocked=new Uint8Array(N);
for(const p of allPads)if(!p.smd) {
  const r=p.drill/2+.2+.25;
  for(let y=Math.floor((p.ay-r)/step);y<=Math.ceil((p.ay+r)/step);y++)
    for(let x=Math.floor((p.ax-r)/step);x<=Math.ceil((p.ax+r)/step);x++)
      if(x>=0&&y>=0&&x<nx&&y<ny&&Math.hypot(x*step-p.ax,y*step-p.ay)<=r)holeBlocked[idx(x,y)]=1;
}
let segments=[],vias=[],failures=[];
class Heap {
  constructor(){this.a=[];}
  push(v){let a=this.a,i=a.length;a.push(v);while(i){let p=(i-1)>>1;if(a[p][0]<=v[0])break;a[i]=a[p];i=p;}a[i]=v;}
  pop(){let a=this.a,top=a[0],v=a.pop();if(a.length){let i=0;while(i*2+1<a.length){let c=i*2+1;if(c+1<a.length&&a[c+1][0]<a[c][0])c++;if(a[c][0]>=v[0])break;a[i]=a[c];i=c;}a[i]=v;}return top;}
}
function clear(l,x,y,r,owner) {
  const a=Math.ceil(r/step);
  for(let dy=-a;dy<=a;dy++)for(let dx=-a;dx<=a;dx++)if(dx*dx+dy*dy<=(r/step+.3)**2){
    let xx=x+dx,yy=y+dy;if(xx<0||yy<0||xx>=nx||yy>=ny)return false;
    let v=occ[l][idx(xx,yy)];if(v&&v!==owner)return false;
  }return true;
}
function route(net,pads,width) {
  const owner=nid(net),tree=new Set(), reached=new Set();
  const keypad=p=>idx(Math.round(p.ax/step),Math.round(p.ay/step));
  for(let l=0;l<(pads[0].smd?1:2);l++)tree.add(keypad(pads[0])+l*N);
  reached.add(pads[0]);
  for(const pad of pads.slice(1)) {
    const target=keypad(pad), [tx,ty]=xy(target),dist=new Float64Array(N*2);dist.fill(Infinity);
    const prev=new Int32Array(N*2);prev.fill(-1);const heap=new Heap();
    for(let l=0;l<(pad.smd?1:2);l++){let k=target+l*N;dist[k]=0;heap.push([0,k]);}
    let end=-1,limit=0;
    while(heap.a.length&&limit++<N*4) {
      let [cost,k]=heap.pop();if(cost!==dist[k])continue;
      if(tree.has(k)){end=k;break;}
      let l=k>=N?1:0,[x,y]=xy(k%N);
      for(const [dx,dy] of [[1,0],[-1,0],[0,1],[0,-1]]) {
        let xx=x+dx,yy=y+dy;if(!clear(l,xx,yy,width/2+.25,owner))continue;
        let kk=idx(xx,yy)+l*N,nd=cost+1;
        if(nd<dist[kk]){dist[kk]=nd;prev[kk]=k;heap.push([nd,kk]);}
      }
      let other=1-l,kk=k%N+other*N,nd=cost+12;
      const holeClear=!holeBlocked[k%N];
      if(holeClear&&clear(l,x,y,.7,owner)&&clear(other,x,y,.7,owner)&&nd<dist[kk]){dist[kk]=nd;prev[kk]=k;heap.push([nd,kk]);}
    }
    if(end<0){failures.push(`${net}: ${pad.ref}.${pad.num}`);continue;}
    let routeKeys=[],k=end;while(k>=0){routeKeys.push(k);tree.add(k);k=prev[k];}
    const pts=routeKeys.map(k=>({l:k>=N?1:0,x:(k%N%nx)*step,y:Math.floor(k%N/nx)*step}));
    for(let i=1;i<pts.length;i++) {
      const a=pts[i-1],b=pts[i];
      if(a.l!==b.l){vias.push({x:a.x,y:a.y,net});for(let l=0;l<2;l++)markCircle(l,a.x,a.y,.7,owner);}
      else {segments.push({...a,x2:b.x,y2:b.y,width,net});markCircle(a.l,(a.x+b.x)/2,(a.y+b.y)/2,width/2+.25,owner);}
    }
    const start=pts[pts.length-1];
    if(start.x!==pad.ax||start.y!==pad.ay)segments.push({...start,x2:pad.ax,y2:pad.ay,width,net});
    // The first tree seed must also terminate on the exact original pad coordinate.
    if(reached.size===1) {
      const p=pads[0],a=pts[0];if(a.x!==p.ax||a.y!==p.ay)segments.push({...a,x2:p.ax,y2:p.ay,width,net});
    }
    reached.add(pad);
  }
}
const priority=n=>isPower(n)?0:n==='GND'?1:n==='3V3'?2:3;
const order=[...nets].sort((a,b)=>priority(a)-priority(b));
function isPower(n){return /12|VMOT|STOP_SEND|_M[12][AB]/.test(n);}
for(const n of order){
  let pads=allPads.filter(p=>p.net===n);
  if(pads.length>1)route(n,pads,isPower(n)?1.5:n==='GND'?1:.3);
}
if(failures.length)console.error('UNROUTED:',failures.join(', '));
let pcb=`(kicad_pcb (version 20240108) (generator "portable_sat_original")
  (general (thickness 1.6)) (paper "A4")
  (layers (0 "F.Cu" signal) (31 "B.Cu" signal) (35 "F.Paste" user) (36 "B.SilkS" user "b.silkscreen") (37 "F.SilkS" user "f.silkscreen") (38 "B.Mask" user) (39 "F.Mask" user) (44 "Edge.Cuts" user) (46 "B.CrtYd" user) (47 "F.CrtYd" user) (48 "B.Fab" user) (49 "F.Fab" user))
  (setup
    (stackup
      (layer "F.SilkS" (type "Top Silk Screen") (color "White"))
      (layer "F.Paste" (type "Top Solder Paste"))
      (layer "F.Mask" (type "Top Solder Mask") (color "Green") (thickness .01))
      (layer "F.Cu" (type "copper") (thickness .07))
      (layer "dielectric 1" (type "core") (thickness 1.44) (material "FR4") (epsilon_r 4.5) (loss_tangent .02))
      (layer "B.Cu" (type "copper") (thickness .07))
      (layer "B.Mask" (type "Bottom Solder Mask") (color "Green") (thickness .01))
      (layer "B.SilkS" (type "Bottom Silk Screen") (color "White"))
      (copper_finish "HASL lead-free")
      (dielectric_constraints no))
    (pad_to_mask_clearance .05) (allow_soldermask_bridges_in_footprints no))
  (net 0 "") ${nets.map((n,i)=>`(net ${i+1} "${n}")`).join('\n')}
  ${parts.map(p=>footprint(p)).join('\n')}
  ${segments.map(s=>`(segment (start ${num(s.x)} ${num(s.y)}) (end ${num(s.x2)} ${num(s.y2)}) (width ${s.width}) (layer "${s.l?'B.Cu':'F.Cu'}") (net ${nid(s.net)}) (uuid "${uuid()}"))`).join('\n')}
  ${vias.map(v=>`(via (at ${v.x} ${v.y}) (size .9) (drill .4) (layers "F.Cu" "B.Cu") (net ${nid(v.net)}) (uuid "${uuid()}"))`).join('\n')}
  (gr_rect (start 0 0) (end 180 130) (stroke (width .05)(type default)) (fill none) (layer "Edge.Cuts") (uuid "${uuid()}"))
  ${[[5,5],[175,5],[5,125],[175,125]].map(([x,y],i)=>`(footprint "PortableSatCarrier:MountingHole_3.2" (layer "F.Cu") (at ${x} ${y}) (uuid "${uuid()}") (property "Reference" "H${i+1}" (at 0 4) (layer "F.SilkS") (effects(font(size 1 1)(thickness .15)))) (property "Value" "M3_NPTH" (at 0 -4) (layer "F.Fab") (effects(font(size 1 1)(thickness .15)))) (attr board_only exclude_from_pos_files exclude_from_bom) (pad "" np_thru_hole circle (at 0 0) (size 3.2 3.2) (drill 3.2) (layers "*.Cu" "*.Mask")))`).join('\n')}
  (gr_text "PortableSat CARRIER REV A / 12V ONLY / PROTOTYPE" (at 90 8) (layer "F.SilkS") (effects(font(size 1.2 1.2)(thickness .18))))
  (gr_text "NO COPPER IN ESP ANTENNA REGION - NO METAL ABOVE" (at 88 14) (layer "F.SilkS") (effects(font(size .8 .8)(thickness .12))))
  (gr_text "J2: EXTERNAL LATCHED DC STOP IN SERIES / NOT A SIGNAL" (at 86 80) (layer "F.SilkS") (effects(font(size .85 .85)(thickness .12))))
)`;
fs.writeFileSync(path.join(root,'PortableSatCarrier.kicad_pcb'),pcb);
// Schematic: exact named wires, manufacturer module pad numbers, explicit NC.
let libs=[],symbols=[],wires=[],labels=[],nc=[];
for(let j=0;j<parts.length;j++) {
  const p=parts[j],name='Carrier_'+p.ref, count=p.pins.length, height=(count+1)*2.54;
  libs.push(`(symbol "PortableSatCarrier:${name}" (pin_names (offset 1.0)) (in_bom yes)(on_board yes)
    (property "Reference" "${p.ref}" (at 0 2.54 0)(effects(font(size 1.27 1.27))))
    (property "Value" "${p.value}" (at 0 0 0)(effects(font(size 1.27 1.27))))
    (property "Footprint" "${fpName(p)}" (at 0 0 0)(effects(font(size 1.27 1.27))(hide yes)))
    (symbol "${name}_0_1" (rectangle(start 0 0)(end 20.32 ${-height})(stroke(width .254)(type default))(fill(type background))))
    (symbol "${name}_1_1" ${p.pins.map((q,i)=>`(pin passive line (at -5.08 ${-(i+1)*2.54} 0)(length 5.08)
      (name "${q.net||'NC'}" (effects(font(size 1 1)))) (number "${q.num}" (effects(font(size 1 1)))))`).join('\n')}))`);
  const sx=num(25.4+(j%5)*88.9),sy=num(25.4+Math.floor(j/5)*106.68), sid=uuid();
  symbols.push(`(symbol (lib_id "PortableSatCarrier:${name}") (at ${sx} ${sy} 0) (unit 1)(in_bom yes)(on_board yes)(dnp no)(uuid "${sid}")
    (property "Reference" "${p.ref}" (at ${sx+10} ${sy-5} 0)(effects(font(size 1.27 1.27))))
    (property "Value" "${p.value}" (at ${sx+10} ${sy-2} 0)(effects(font(size 1 1))))
    (property "Footprint" "${fpName(p)}" (at ${sx} ${sy} 0)(effects(font(size 1 1))(hide yes)))
    ${p.pins.map(q=>`(pin "${q.num}" (uuid "${uuid()}"))`).join('\n')}
    (instances(project "PortableSatCarrier" (path "/ROOT_UUID" (reference "${p.ref}")(unit 1)))))`);
  for(const q of p.pins) {
    const x=num(sx-5.08),y=num(sy+q.num*2.54);
    if(!q.net)nc.push(`(no_connect (at ${x} ${y}) (uuid "${uuid()}"))`);
    else {
      wires.push(`(wire (pts(xy ${x-7.62} ${y})(xy ${x} ${y}))(stroke(width 0)(type default))(uuid "${uuid()}"))`);
      labels.push(`(global_label "${q.net}" (shape input)(at ${x-7.62} ${y} 0)(effects(font(size .9 .9))(justify left))(uuid "${uuid()}")
        (property "Intersheetrefs" "\${INTERSHEET_REFS}" (at ${x-7.62} ${y} 0)(effects(font(size .9 .9))(hide yes))))`);
    }
  }
}
const schid=uuid();
fs.writeFileSync(path.join(root,'PortableSatCarrier.kicad_sch'),`(kicad_sch(version 20231120)(generator "eeschema")(uuid "${schid}")(paper "User" 500 900)
 (lib_symbols ${libs.join('\n')}) ${wires.join('\n')} ${labels.join('\n')} ${nc.join('\n')}
 ${symbols.join('\n').replaceAll('ROOT_UUID',schid)}
 (sheet_instances(path "/"(page "1"))))`);
const pro={board:{design_settings:{rules:{min_clearance:.25,min_track_width:.3,min_via_diameter:.9,min_via_drill:.4,min_through_hole_diameter:.4,min_hole_to_hole:.25,min_copper_edge_clearance:.5}}},
 net_settings:{classes:[{name:'Default',clearance:.25,track_width:.3,via_diameter:.9,via_drill:.4,description:'2 oz original carrier, signal 3.3V'}]},
 meta:{filename:'PortableSatCarrier.kicad_pro',version:1}};
fs.writeFileSync(path.join(root,'PortableSatCarrier.kicad_pro'),JSON.stringify(pro,null,2));
const powerConditions=nets.filter(isPower).map(n=>`A.NetName == '${n}'`).join(' || ');
fs.writeFileSync(path.join(root,'PortableSatCarrier.kicad_dru'),`(version 1)
(rule "Power_and_motor_minimum_width"
  (condition "A.Type == 'Track' && (${powerConditions})")
  (constraint track_width (min 1.5)))
(rule "Ground_minimum_width"
  (condition "A.Type == 'Track' && A.NetName == 'GND'")
  (constraint track_width (min 1.0)))
`);
fs.writeFileSync(path.join(root,'connectivity.json'),JSON.stringify({board_mm:[180,130],holes_mm:[[5,5],[175,5],[5,125],[175,125]],nets,
 parts:parts.map(p=>({...p,footprint:fpName(p)})),router:{grid_mm:step,segments:segments.length,vias:vias.length,unrouted:failures}},null,2));
fs.mkdirSync(path.join(root,'PortableSatCarrier.pretty'),{recursive:true});
for(const p of parts)fs.writeFileSync(path.join(root,'PortableSatCarrier.pretty',p.ref+'_'+p.kind+'.kicad_mod'),footprint(p,true));
const mount=pcb.match(/\(footprint "PortableSatCarrier:MountingHole_3\.2"[\s\S]*?\(layers "\*\.Cu" "\*\.Mask"\)\)\)/)[0]
 .replace(/\(at 5 5\) \(uuid "[^"]+"\)/,'');
fs.writeFileSync(path.join(root,'PortableSatCarrier.pretty','MountingHole_3.2.kicad_mod'),mount);
fs.writeFileSync(path.join(root,'PortableSatCarrier.kicad_sym'),`(kicad_symbol_lib(version 20231120)(generator "kicad_symbol_editor")
${libs.map(s=>s.replace('(symbol "PortableSatCarrier:','(symbol "')).join('\n')})`);
fs.writeFileSync(path.join(root,'sym-lib-table'),`(sym_lib_table
  (version 7)
  (lib (name "PortableSatCarrier") (type "KiCad") (uri "\${KIPRJMOD}/PortableSatCarrier.kicad_sym") (options "") (descr "Original carrier module and passive pin symbols"))
)
`);
fs.writeFileSync(path.join(root,'fp-lib-table'),`(fp_lib_table (version 7) (lib (name "PortableSatCarrier")(type "KiCad")(uri "\${KIPRJMOD}/PortableSatCarrier.pretty")(options "")(descr "Original carrier footprints; verify physical module and connector dimensions")))`);
fs.writeFileSync(path.join(root,'..','bom','pcb.csv'),'Reference,Quantity,Manufacturer_part,Value,Footprint,Estimated_EUR_each,Notes\n'+
parts.map(p=>[p.ref,1,p.mpn,p.value,fpName(p),p.kind==='module'?12:p.kind==='driver'?10:p.kind==='terminal'?1.2:p.kind==='fuse'?2.5:p.kind==='xh'?.6:p.kind==='tvs'?.6:p.kind==='diode'?.7:.15,'Estimate only; not a vendor quote'].map(v=>`"${String(v).replaceAll('"','""')}"`).join(',')).join('\n')+
'\n"PCB",1,"Custom FR4","180x130mm 2layer 2oz 1.6mm","Original",15,"Small batch estimate; manufacturing HOLD until release checks"\n"STOP",1,"External DC-rated maintained latching two-contact stop","12V >=5A DC power NC + isolated NC auxiliary","Off-board",15,"RELEASE BLOCKER exact part not selected; do not substitute AC-only rating"\n"BUCK",1,"Pololu D24V22F5","5V 2.2A regulated","Off-board wired module",15,"Only header connections; mount separately; 12V input"\n"U1_SOCKET",2,"Samtec SSW-119-01-G-S","1x19 2.54mm female socket","U1 module footprint rows",2.5,"Check actual tail/header engagement; separate from ESP module"\n"U2_U3_SOCKET",4,"Samtec SSW-108-01-G-S","1x8 2.54mm female socket","U2 U3 module footprint rows",1.5,"Separate from Watterott modules"\n"GNSS",1,"Adafruit 746 Ultimate GPS breakout","External 3.3V UART GPS","Off-board",25,"Confirm current revision VIN3.3V and UART levels"\n"ENCODER",2,"ams AS5600-ASOM","External AS5600 on qualified 3.3V breakout","Off-board",4,"Chip part number only; breakout and magnet selection/measurement remain required"\n');
console.log(JSON.stringify({parts:parts.length,nets:nets.length,segments:segments.length,vias:vias.length,unrouted:failures},null,2));
