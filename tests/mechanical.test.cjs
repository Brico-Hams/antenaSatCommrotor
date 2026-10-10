const test=require('node:test');
const assert=require('node:assert/strict');
const {spawnSync}=require('node:child_process');
const path=require('node:path');
for(const file of ['mechanical-math.cjs','mechanical-inventory.cjs','mechanical-mass.cjs']) {
  test(`mechanical validation: ${file}`,()=>{
    const result=spawnSync(process.execPath,[path.join(__dirname,file)],{encoding:'utf8'});
    assert.equal(result.status,0,result.stderr||result.stdout);
  });
}
