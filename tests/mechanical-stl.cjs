/* Validate actual ASCII or binary rendered triangles, not file-name existence. */
const fs = require('node:fs');
const assert = require('node:assert/strict');
function validate(file) {
const b = fs.readFileSync(file);
let faces = [];
if (b.length >= 84 && 84 + 50 * b.readUInt32LE(80) === b.length) {
  for (let p = 84; p < b.length; p += 50) {
    faces.push([0, 1, 2].map(i => [0, 1, 2].map(k => b.readFloatLE(p + 12 + i * 12 + k * 4))));
  }
} else {
  const verts = [...b.toString().matchAll(/vertex\s+([-+\deE.]+)\s+([-+\deE.]+)\s+([-+\deE.]+)/g)]
    .map(m => m.slice(1).map(Number));
  assert(verts.length % 3 === 0 && verts.length > 0, 'Invalid STL vertex count');
  for (let i = 0; i < verts.length; i += 3) faces.push(verts.slice(i, i + 3));
}
const key = p => p.map(n => Math.round(n * 10000)).join(',');
const edges = new Map();
const vertexParent=new Map();
function find(x) {
  if(!vertexParent.has(x))vertexParent.set(x,x);
  let root=x;while(vertexParent.get(root)!==root)root=vertexParent.get(root);
  while(vertexParent.get(x)!==x){const next=vertexParent.get(x);vertexParent.set(x,root);x=next;}
  return root;
}
function join(a,b){const x=find(a),y=find(b);if(x!==y)vertexParent.set(x,y);}
let volume = 0;
for (const [a, c, d] of faces) {
  assert([...a, ...c, ...d].every(Number.isFinite));
  const u = c.map((n,i) => n-a[i]), v = d.map((n,i) => n-a[i]);
  const cross = [u[1]*v[2]-u[2]*v[1],u[2]*v[0]-u[0]*v[2],u[0]*v[1]-u[1]*v[0]];
  assert(Math.hypot(...cross) > 1e-8, 'Degenerate triangle');
  volume += (a[0]*(c[1]*d[2]-c[2]*d[1])+a[1]*(c[2]*d[0]-c[0]*d[2])+a[2]*(c[0]*d[1]-c[1]*d[0]))/6;
  for (const [p,q] of [[a,c],[c,d],[d,a]]) {
    const x=key(p), y=key(q); const name=x<y?x+'|'+y:y+'|'+x;
    join(x,y);
    const item=edges.get(name)||{count:0,balance:0};
    item.count++; item.balance+=x<y?1:-1; edges.set(name,item);
  }
}
for (const item of edges.values()) assert(item.count===2 && item.balance===0,'Open/nonmanifold or inconsistently oriented edge');
assert(volume > 0, 'Nonpositive oriented solid volume');
const components=new Set([...vertexParent.keys()].map(find)).size;
return {triangles:faces.length,volume,components};
}
module.exports=validate;
if(require.main===module) {
  const result=validate(process.argv[2]);
  console.log(`${process.argv[2].split(/[\\/]/).pop()}: ${result.triangles} triangles, closed oriented edges, ${result.volume.toFixed(1)} mm3`);
}
