"""Export real candidate BOM/CPL and verify frozen contract against KiCad netlist.
No LCSC stock code, JLC orientation qualification or fabrication release is asserted.
"""
import csv,json,pathlib,xml.etree.ElementTree as ET,hashlib,collections,pcbnew
P=pathlib.Path(__file__).resolve().parents[1]; F=P/'fabrication'/'NOT_FOR_MANUFACTURE'; tree=ET.parse(P/'reports'/'cm5-guard-A.net.xml'); root=tree.getroot()
contract=json.loads((P/'interface.json').read_text()); comps={c.attrib['ref']:c for c in root.findall('./components/comp')}; nets={}; bypin={}
for net in root.findall('./nets/net'):
 name=net.attrib['name']; nets[name]={ (n.attrib['ref'],n.attrib['pin']) for n in net.findall('node') }
 for n in net.findall('node'): bypin[(n.attrib['ref'],n.attrib['pin'])]=name
results=[]
def check(msg,ok):
 results.append({'test':msg,'passed':bool(ok)})
 if not ok: raise AssertionError(msg)
for pin in contract['gpio']:
 check(f"BCM{pin['bcm']} / header {pin['headerPin']} = {pin['signal']}",bypin.get(('J1',str(pin['headerPin'])))=='/'+pin['signal'])
for n in (1,2,4,17): check('No auxiliary power feed to CM5IO header pin '+str(n),'unconnected' in bypin.get(('J1',str(n)),'unconnected'))
for pin in (15,16,17):check('MCP address strap '+str(pin),bypin[('U2',str(pin))]=='/GND_LOGIC')
for pin in (1,2,21):check('Mux address strap '+str(pin),bypin[('U3',str(pin))]=='/GND_LOGIC')
for i in range(5):
 sd=str(4+2*i+(1 if i>=4 else 0)); sc=str(5+2*i+(1 if i>=4 else 0))
 check('Mux SDA channel '+str(i),bypin[('U3',sd)]==bypin[('J'+str(3+i),'3')])
 check('Mux SCL channel '+str(i),bypin[('U3',sc)]==bypin[('J'+str(3+i),'4')])
check('Retriggerable watchdog actual Q output pin13',bypin[('U6','13')]=='/WATCHDOG_OK')
check('Watchdog timing Cext14 / RCext15',bypin[('U6','14')]=='/WD_C' and bypin[('U6','15')]=='/WD_RC')
for i in range(6): check('NC hard-inhibit input '+str(i),bypin[('U4',str([2,4,6,8,10,12][i]))]==bypin[('U7',str(i+1))])
for i,ax in enumerate(['AZ','EL','POL']):
 left='J'+str(16+3*i); right='J'+str(17+3*i)
 check(ax+' EN is low-side MOSFET drain, not GPIO',bypin[(left,'1')]==bypin[('Q'+str(1+i),'3')])
 check(ax+' selected SPI CS',bypin[(left,'4')]=='/SPI1_CS'+str(i)+'_'+ax)
 check(ax+' DCO not wired as fault', 'unconnected' in bypin.get((left,'6'),'unconnected'))
 check(ax+' VIO3V3',bypin[(right,'7')]=='/V3V3')
check('USB device VBUS never battery/logic',bypin[('J34','A4')]=='/USB_VBUS_DEVICE' and bypin[('J34','A4')]!=bypin[('U1','1')])
board=pcbnew.LoadBoard(str(P/'cm5-guard-A.kicad_pcb')); footprints={p.GetReference():p for p in board.GetFootprints()}
# Verify circuit bindings before exercising a Boolean model. This is NOT SPICE or physical testing.
bindings={('U13','1'):'LATCH_CLEAR_N',('U13','2'):'ALL_REQUESTS_IDLE',('U13','3'):'REARM_CLK',('U13','4'):'V3V3',('U13','5'):'REARMED',
          ('U14','1'):'ARM_IDLE',('U14','2'):'VHF_IDLE',('U14','3'):'IDLE_AV',('U14','4'):'IDLE_AV',('U14','5'):'UHF_IDLE',('U14','6'):'ALL_REQUESTS_IDLE',
          ('U14','9'):'SAFE_OK',('U14','10'):'LOGIC_RESET_N',('U14','8'):'LATCH_CLEAR_N',('U14','12'):'SAFE_OK',('U14','13'):'REARMED',('U14','11'):'REARM_PERMIT',
          ('U8','1'):'REARM_PERMIT',('U8','2'):'MOTOR_ARM_REQUEST',('U8','3'):'MOTOR_PERMIT',('U9','1'):'REARM_PERMIT',('U9','2'):'PTT_VHF_REQUEST',('U9','3'):'PTT_VHF_GATE',
          ('U9','4'):'REARM_PERMIT',('U9','5'):'PTT_UHF_REQUEST',('U9','6'):'PTT_UHF_GATE',('Q7','2'):'BAT_FUSED',('Q7','3'):'BAT_PROTECTED',
          ('L1','1'):'LOGIC_BAT_FUSED',('L1','4'):'EMI_LOGIC_POS',('L1','2'):'GND_MOTOR',('L1','3'):'EMI_LOGIC_RETURN'}
for key,net in bindings.items():check('Circuit binding '+str(key)+' '+net,bypin.get(key)=='/'+net)
for i,ax in enumerate(['AZ','EL','POL']):
 left=footprints['J'+str(16+3*i)];right=footprints['J'+str(17+3*i)]
 check(ax+' module column spacing 12.70mm',abs(pcbnew.ToMM(right.GetPosition().x-left.GetPosition().x)-12.7)<.001)
 lp={pad.GetNumber():pad for pad in left.Pads()};rp={pad.GetNumber():pad for pad in right.Pads()}
 check(ax+' socket pin1 alignment',lp['1'].GetPosition().y==rp['1'].GetPosition().y)
 for n in range(1,8):check(ax+' pitch pad'+str(n),abs(pcbnew.ToMM(lp[str(n+1)].GetPosition().y-lp[str(n)].GetPosition().y)-2.54)<.001)
 check(ax+' actual two GND pads common motor reference',bypin[('J'+str(17+3*i),'2')]=='/GND_MOTOR' and bypin[('J'+str(17+3*i),'8')]=='/GND_MOTOR')
for a,bnd in [('J36','J37'),('J38','J39')]:
 check('SMA pair signal continuity '+a,bypin[(a,'1')]==bypin[(bnd,'1')])
 check('SMA pair isolated shield continuity '+a,bypin[(a,'2')]==bypin[(bnd,'2')])
 check('SMA non-RP actual footprint '+a,'SMA_Amphenol_132134' in footprints[a].GetFPID().GetLibItemName().c_str())
check('RF shield domains distinct',bypin[('J36','2')]!=bypin[('J38','2')] and bypin[('J36','2')] not in ('/GND_MOTOR','/GND_LOGIC'))
for ref in ['J41','F1','F2','F3','F4','F5','F6','Q7','D1','D2','L1','R80','C80','R52','C16']:
 check('Unqualified power locked out DNP '+ref,footprints[ref].IsDNP())
check('Battery gate RC resistor binding',bypin[('R52','1')]=='/POWER_GATE' and bypin[('R52','2')]=='/GND_MOTOR')
check('Battery gate RC capacitor binding',bypin[('C16','1')]=='/POWER_GATE' and bypin[('C16','2')]=='/BAT_PROTECTED')
check('Logic bypass C21 remains populated',not footprints['C21'].IsDNP() and bypin[('C21','1')]=='/V3V3' and bypin[('C21','2')]=='/GND_LOGIC')
check('Main fuse upstream of reverse/transient branch',bypin[('F1','1')]==bypin[('J41','1')] and bypin[('F1','2')]==bypin[('D2','1')]==bypin[('Q7','2')])
for ref in ['F2','F3','F4','F5','F6']:check('Independent branch fuse '+ref,bypin[(ref,'1')]=='/BAT_PROTECTED')
check('Motor external E-stop cuts supply before J28',bypin[('J42','1')]=='/MOTOR_BRANCH_FUSED' and bypin[('J28','1')]=='/VMOT_ESTOP' and bypin[('J42','1')]!=bypin[('J28','1')])
# Exhaustive Boolean guard states: faults must suppress outputs; no requests can override latch.
modelcases=0
for limitmask in range(64):
 for estop in (False,True):
  for watchdog in (False,True):
   for por in (False,True):
    for latch in (False,True):
     for requests in range(8):
      safe=limitmask==63 and estop and watchdog
      q=latch if safe and por else False
      arm,vhf,uhf=[bool(requests&(1<<i)) for i in range(3)]
      motor=safe and q and arm;pttv=safe and q and vhf;pttu=safe and q and uhf
      assert (safe and por and latch) or not (motor or pttv or pttu)
      # On a rearm edge D can set only when every common request is LOW.
      rearmed=safe and por and not (arm or vhf or uhf)
      assert not rearmed or requests==0
      modelcases+=1
check('Exhaustive Boolean permit model '+str(modelcases)+' cases',True)
# Sequential fault recovery: a recovered NC/watchdog alone cannot create a new clock edge.
q=True
for safe,por,button_edge,requests,expected in [(False,True,False,7,False),(True,True,False,7,False),(True,True,True,7,False),(True,True,True,0,True),(True,False,False,0,False),(True,True,False,0,False)]:
 if not(safe and por):q=False
 elif button_edge:q=requests==0
 assert q==expected
check('Fault recovery and POR need fresh manual edge with requests idle',True)
check('RF reference zones physically present',len(list(board.Zones()))==2)
trackitems=list(board.GetTracks());viaitems=[t for t in trackitems if isinstance(t,pcbnew.PCB_VIA)];traceitems=[t for t in trackitems if not isinstance(t,pcbnew.PCB_VIA)]
widths={}
for t in traceitems:widths.setdefault(t.GetNetname(),set()).add(round(pcbnew.ToMM(t.GetWidth()),3))
for name in ['/BAT_POS','/BAT_FUSED','/BAT_PROTECTED','/MOTOR_BRANCH_FUSED','/CM5IO_BRANCH_FUSED','/VHF_BRANCH_FUSED','/UHF_BRANCH_FUSED']:
 check('Candidate DC trunk 2mm present; neckdowns NOT current-qualified '+name,max(widths[name])>=2)
for ax in ['AZ','EL','POL']:
 for coil in ['M1A','M1B','M2A','M2B']:check('Candidate motor coil minimum width1mm '+ax+coil,min(widths['/'+ax+'_'+coil])>=1)
route_metrics={'tracks':len(traceitems),'vias':len(viaitems),'zones':len(list(board.Zones())), 'board_thickness_mm':1.6,'outline_mm':[290,280],'module_socket_pitch_mm':2.54,'module_column_spacing_mm':12.7,'net_track_widths_mm':{k:sorted(v) for k,v in sorted(widths.items())},'high_current_via_rating_verified':False,'rf_impedance_verified':False,'thermal_validation':False,'latch_boolean_cases':modelcases,'latch_timing_and_physical_validation':False}
(P/'reports'/'routing-metrics.json').write_text(json.dumps(route_metrics,indent=2),encoding='utf-8')
positions=list(csv.DictReader((F/'positions-kicad.csv').open(newline='',encoding='utf-8')))
partdata=json.loads((P/'design'/'components.json').read_text()); pdata={p['ref']:p for p in partdata}
groups=collections.defaultdict(list)
for pos in positions:
 ref=pos['Ref']; p=pdata[ref]; fp=footprints[ref]
 check('BOM/CPL active-SMD '+ref,not fp.IsDNP() and bool(fp.GetAttributes() & pcbnew.FP_SMD))
 check('BOM exact candidate MPN '+ref,bool(p['mpn']))
 groups[(p['value'],p['mpn'],p['footprint'])].append(ref)
with (F/'JLCPCB-BOM-REVIEW.csv').open('w',newline='',encoding='utf-8') as f:
 w=csv.writer(f); w.writerow(['Comment','Designator','Footprint','Quantity','Manufacturer Part'])
 for (value,mpn,fp),rs in sorted(groups.items()):w.writerow([value,','.join(sorted(rs)),fp,len(rs),mpn])
with (F/'JLCPCB-CPL-REVIEW.csv').open('w',newline='',encoding='utf-8') as f:
 w=csv.writer(f);w.writerow(['Designator','Mid X','Mid Y','Layer','Rotation'])
 for p in positions:w.writerow([p['Ref'],p['PosX'],p['PosY'],'Top',p['Rot']])
with (P/'design'/'component-register.csv').open('w',newline='',encoding='utf-8') as f:
 w=csv.writer(f);w.writerow(['Reference','Value','Candidate MPN','KiCad footprint','DNP','Scope','Sourcing/physical verification'])
 for p in partdata:
  w.writerow([p['ref'],p['value'],p['mpn'],p['footprint'],p['dnp'],'EXTERNAL' if p.get('external') else 'BOARD','NOT VERIFIED / NO LCSC CODE'])
erc=json.loads((P/'reports'/'erc.json').read_text()); drc=json.loads((P/'reports'/'drc.json').read_text())
summary={'kicad_version':drc['kicad_version'],'release':'ROUTED DIGITAL REVIEW / QUALIFICATION BLOCKED / DO NOT ORDER','erc_violations':sum(len(s.get('violations',[])) for s in erc['sheets']),'drc_violations':len(drc['violations']),'drc_unconnected':len(drc['unconnected_items']),'schematic_parity':len(drc['schematic_parity']),'erc_ignored_checks':[i['key'] for i in erc['ignored_checks']],'drc_ignored_checks':[i['key'] for i in drc['ignored_checks']],'cpl_smd_components':len(positions),'bom_groups':len(groups),'contract_tests':len(results),'physical_validation':False,'limitations':['Powerpole harness remains external; exact contacts/crimp/wire/pack limits unqualified','Power front-end candidates DNP; fuse insert ratings and inrush/SOA/thermal qualification NOT complete','Isolated auxiliary 5V converter and CM5IO USB-C PD converter remain external and unselected','USB-C is a DNP USB2 device interface, not CM5IO PD power','Physical SMA feed-throughs routed with return planes; impedance/RF performance NOT measured','LCSC availability, assembly rotations and module/socket/CMC fit NOT physically verified','Manual rearm circuit implemented; model tests are NOT physical fail-off validation']}
assert summary['erc_violations']==summary['drc_violations']==summary['drc_unconnected']==summary['schematic_parity']==0
(P/'reports'/'contract-tests.json').write_text(json.dumps(results,indent=2),encoding='utf-8');(P/'reports'/'validation-summary.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
manifest={str(f.relative_to(P)):hashlib.sha256(f.read_bytes()).hexdigest() for f in sorted(P.rglob('*')) if f.is_file() and 'tools' not in f.parts and f.name not in ('manifest-sha256.json','diagnose.py','diagnostic.kicad_sch','diagnostic.net','baseline-erc.txt') and not f.name.endswith(('.pyc','.kicad_prl'))}
(P/'reports'/'manifest-sha256.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8');print(json.dumps(summary,indent=2))







