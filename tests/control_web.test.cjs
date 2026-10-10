'use strict';
// Run using any Node 22 binary; no npm dependency or field runtime.
const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict');
const test=require('node:test');
const path=require('node:path');
const html=fs.readFileSync(path.join(__dirname,'..','web','index.html'),'utf8');
const firmware=fs.readFileSync(path.join(__dirname,'..','firmware','src','main.cpp'),'utf8');
const board=fs.readFileSync(path.join(__dirname,'..','firmware','include','board_config.h'),'utf8');
assert.match(html,/<html lang="es">/);
assert.doesNotMatch(html,/https?:\/\/.*(?:script|stylesheet)/);
const script=html.match(/<script>([\s\S]*?)<\/script>/)[1];
new vm.Script(script);
const ids=[...html.matchAll(/id="([^"]+)"/g)].map(x=>x[1]);
assert.equal(new Set(ids).size,ids.length);
const elements=new Map(ids.map(id=>[id,{value:id==='token'?'test-token':'0',checked:false,
 textContent:'',handlers:{},children:[],addEventListener(event,fn){this.handlers[event]=fn},
 replaceChildren(){this.children=[]},append(node){this.children.push(node)}}]));
let requests=[],response={message:'ok'};
const context={document:{getElementById:id=>{assert.ok(elements.has(id),id);return elements.get(id)},
 createElement:()=>({})},fetch:async(url,options)=>{
 requests.push({url,...options});return {ok:true,json:async()=>response};
},setInterval(){},console};
vm.createContext(context);vm.runInContext(script,context);
test('control web uses device API schema and authenticated actions',async()=>{
 for(const [id,endpoint] of [['stop','stop'],['clear','clear'],['home','home'],
 ['move','move'],['site','site'],['calibrate','calibrate'],['select','select'],['track','track']]){
  await elements.get(id).handlers.click();
  const request=requests.at(-1);
  assert.equal(request.url,'/api/'+endpoint);assert.equal(request.method,'POST');
  assert.equal(request.headers['X-Control-Token'],'test-token');
 }
 response={satellites:[{id:0,name:'<img src=x onerror=alert(1)>',fresh:true}]};
 await elements.get('list').handlers.click();
 assert.equal(elements.get('satellite').children[0].textContent,
 '<img src=x onerror=alert(1)> — vigente');
 assert.doesNotMatch(script,/innerHTML|localStorage|sessionStorage/);
 console.log('control_web: syntax, DOM, 8 authenticated actions, safe satellite rendering PASS');
});
test('firmware safety surfaces are guarded independently of WebServer',()=>{
 assert.match(firmware,/xTaskCreatePinnedToCore\(motorTask/);
 assert.match(firmware,/if \(hardware && !input\(Board::estop\)\) halt\(true/);
 assert.match(firmware,/if \(busy\(\)\) \{ reply\(409,"Prediccion solo con motores detenidos"/);
 assert.match(firmware,/if\(predicting && !busy\(\)\)/);
 assert.match(firmware,/if\(busy\(\) \|\| mode==FAULT \|\| !validUTC\(\)/);
 assert.match(firmware,/client\.setCACert\(Board::tlsRoots\)/);
 assert.doesNotMatch(firmware,/\.setInsecure\s*\(/);
 assert.match(firmware,/orbit\.satEl >= 89/);
 assert.match(firmware,/Velocidad angular satelite excede limite motor/);
 assert.match(firmware,/uint32_t\(millis\(\) - trackStamp\) > 1500/);
 assert.match(firmware,/ControlBLE::authorized\(provisioning/);
 assert.match(firmware,/halt\(true, "Provisionamiento USB"\); provisioning = true/);
 assert.match(firmware,/serialLine\.length\(\) < 768/);
 assert.match(firmware,/prefs\.getBool\("carrier",Board::carrierVerified\)/);
 assert.doesNotMatch(firmware,/Serial\.(?:print|println)\([^;\n]*(?:apPassword|apiToken|staPassword|serialLine)/);
 assert.match(firmware,/route\("\/api\/calibrate"/);
 assert.match(firmware,/r\.handler\(\)/);
 assert.match(firmware,/setSecurityAuth\(true, true, true\)/);
 assert.match(firmware,/sec_state\.encrypted && desc->sec_state\.authenticated/);
 assert.match(firmware,/BLE desconectado durante movimiento manual\/homing/);
 for(const path of ['begin','chunk','commit','abort'])
  assert.match(firmware,new RegExp(`route\\("/api/tle/${path}"`));
 assert.match(firmware,/mbedtls_sha256_ret/);
 assert.match(firmware,/route\("\/api\/catalog"/);
 assert.match(firmware,/millis\(\)-tleUploadAt\)>60000/);
 for(const key of ['apiVersion','protocolVersion','firmwareVersion'])
  assert.match(firmware,new RegExp(`d\\["${key}"\\] = ControlBLE::${key}`));
 const platform=fs.readFileSync(path.join(__dirname,'..','firmware','platformio.ini'),'utf8');
 assert.match(platform,/-D CONFIG_BT_NIMBLE_MAX_CONNECTIONS=1/);
});
test('controller GPIO freeze equals agreed DevKitC WROOM-32E carrier nets',()=>{
 const map={azStep:26,azDir:27,elStep:14,elDir:13,enable:25,estop:34,
 azMin:35,azMax:36,elMin:39,elMax:32,gpsRx:16,gpsTx:17,
 azSda:21,azScl:22,elSda:18,elScl:19};
 for(const [name,pin] of Object.entries(map))
  assert.match(board,new RegExp(`\\b${name}\\s*=\\s*${pin}\\b`),name);
 assert.equal(new Set(Object.values(map)).size,Object.keys(map).length);
 assert.match(board,/carrierVerified = false/);
 assert.match(board,/WROOM-32E ONLY/);
});
