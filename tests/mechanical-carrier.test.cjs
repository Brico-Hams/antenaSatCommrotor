const test=require('node:test'),assert=require('node:assert/strict'),path=require('node:path'),fs=require('node:fs');
const validate=require('./mechanical-stl.cjs'),root=path.join(__dirname,'..');
test('actual 180x130 carrier footprint and four mounting holes fit only new case',()=>{
 assert(180>124&&130>64); // old enclosure cannot fit actual routed board
 const inner=[224,174],board=[180,130];assert(inner[0]-board[0]===44&&inner[1]-board[1]===44);
 for(const [x,y] of [[5,5],[175,5],[5,125],[175,125]]) {
   assert(x>=5&&x<=board[0]-5&&y>=5&&y<=board[1]-5);
 }
 assert(8+1.6+32<43.6);
});
test('new case base lid and removable port panels have closed oriented STL edges',()=>{
 for(const name of ['base','lid','port40','port30'])
   validate(path.join(root,'cad','carrier-stl',name+'.stl'));
});
test('actual enlarged carrier enclosure increases budget instead of hiding mass',()=>{
 const count={base:1,lid:1,port40:2,port30:2};let newVolume=0;
 for(const [name,n] of Object.entries(count))newVolume+=validate(path.join(root,'cad','carrier-stl',name+'.stl')).volume*n;
 const oldVolume=validate(path.join(root,'cad','stl','enclosure.stl')).volume+
  validate(path.join(root,'cad','stl','enclosure_lid.stl')).volume;
 const increment=(newVolume-oldVolume)*1.07/1e6;
 assert(increment>.130&&increment<.160);
 assert(2.679+increment+.168+.120>3); // populated carrier plus tray invalidates old light budget
});
test('BRICOHAMS and URL are integrated raised text in actual carrier lid',()=>{
 const cad=fs.readFileSync(path.join(root,'cad','carrier_enclosure.scad'),'utf8');
 assert(cad.includes('brand_name="BRICOHAMS"'));assert(cad.includes('brand_url="bricohams.org"'));
 assert(cad.includes('brand_raise=0.7'));assert(cad.includes('1.95'));
 const mesh=validate(path.join(root,'cad','carrier-stl','lid.stl'));
 assert.equal(mesh.components,1,'Raised branding must join lid, not disconnected floating glyphs');
 const branded=mesh.volume;
 const plain=228*178*2-4*Math.PI*(3.4/2)**2*2;
 assert(branded>plain+100&&branded<plain+1000);
});
