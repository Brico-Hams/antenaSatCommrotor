"""Local-only Specctra interchange and protected RF feed-through routes.
Freerouting must be invoked with -da (no analytics); it receives no cloud service.
"""
import argparse,pathlib,pcbnew,json
p=pathlib.Path(__file__).resolve().parents[1];a=argparse.ArgumentParser();a.add_argument('mode',choices=['prepare','import']);args=a.parse_args()
b=pcbnew.LoadBoard(str(p/'cm5-guard-A.kicad_pcb' if args.mode=='prepare' else p/'design'/'routing'/'placed-prerouted.kicad_pcb'))
def v(x,y):return pcbnew.VECTOR2I(pcbnew.FromMM(x),pcbnew.FromMM(y))
def track(a,z,net,w,layer):
 t=pcbnew.PCB_TRACK(b);t.SetStart(a);t.SetEnd(z);t.SetNet(net);t.SetWidth(pcbnew.FromMM(w));t.SetLayer(layer);b.Add(t)
if args.mode=='prepare':
 # Protected RF launches; geometry alone does NOT validate impedance or matching.
 fps={f.GetReference():f for f in b.GetFootprints()}
 for band,l,r in [('VHF','J36','J37'),('UHF','J38','J39')]:
  p1=next(x for x in fps[l].Pads() if x.GetNumber()=='1');p2=next(x for x in fps[r].Pads() if x.GetNumber()=='1')
  x1=pcbnew.ToMM(p1.GetPosition().x);x2=pcbnew.ToMM(p2.GetPosition().x);yy=pcbnew.ToMM(p1.GetPosition().y)
  track(p1.GetPosition(),v(x1+5,yy),p1.GetNet(),1,pcbnew.F_Cu)
  track(v(x1+5,yy),v(x2-5,yy),p1.GetNet(),2.9,pcbnew.F_Cu)
  track(v(x2-5,yy),p2.GetPosition(),p1.GetNet(),1,pcbnew.F_Cu)
  # Tie the four physical coax shield pins on B.Cu for each feed-through pair, with a reserved return area.
  shields=[x for ref in (l,r) for x in fps[ref].Pads() if x.GetNumber()=='2']; pts=sorted(shields,key=lambda x:(x.GetPosition().x,x.GetPosition().y))
  y=pcbnew.ToMM(p1.GetPosition().y)
  for pad in shields:
   x=pcbnew.ToMM(pad.GetPosition().x); pos=pad.GetPosition();bridge=v(x,y+7)
   track(pos,bridge,pad.GetNet(),1,pcbnew.B_Cu)
  track(v(pcbnew.ToMM(pts[0].GetPosition().x),y+7),v(pcbnew.ToMM(pts[-1].GetPosition().x),y+7),shields[0].GetNet(),1,pcbnew.B_Cu)
 # Force the difficult SPI1 MOSI link above the two module envelopes; other nets route around it.
 pp=next(x for x in fps['J19'].Pads() if x.GetNumber()=='2')
 path=[v(25,27.54),v(23.2,27.54),v(23.2,18),v(73.2,18),v(73.2,27.54),v(75,27.54),v(73.2,27.54),v(73.2,18),v(123.2,18),v(123.2,27.54),v(125,27.54)]
 for aa,zz in zip(path,path[1:]):track(aa,zz,pp.GetNet(),.2,pcbnew.F_Cu)
 pcbnew.SaveBoard(str(p/'design'/'routing'/'placed-prerouted.kicad_pcb'),b)
 if not pcbnew.ExportSpecctraDSN(b,str(p/'design'/'routing'/'guard.dsn')):raise RuntimeError('DSN export failed')
 # Assign routing rules explicitly in DSN (independent of project GUI netclass loading).
 import re
 dfile=p/'design'/'routing'/'guard.dsn';dsn=dfile.read_text(encoding='utf-8')
 dsn=dsn.replace('(clearance 45 (type smd_smd))','(clearance 180 (type smd_smd))')
 powers=['/BAT_POS','/BAT_FUSED','/BAT_PROTECTED','/CM5IO_BRANCH_FUSED','/VHF_BRANCH_FUSED','/UHF_BRANCH_FUSED','/MOTOR_BRANCH_FUSED']
 motors=['/VMOT_ESTOP','/GND_MOTOR']+[f'/{ax}_{coil}' for ax in ['AZ','EL','POL'] for coil in ['M1A','M1B','M2A','M2B']]
 logicpower=['/V3V3','/GND_LOGIC','/AUX_5V_ISOLATED','/LOGIC_BAT_FUSED','/EMI_LOGIC_POS','/EMI_LOGIC_RETURN']
 # Remove only net names from default class, never the actual network pin definitions.
 cs=dsn.index('(class kicad_default'); ce=dsn.index('\n  (wiring',cs);block=dsn[cs:ce]
 for net in powers+motors+logicpower:block=re.sub(re.escape(net)+r'(?=\s)', '',block)
 extra=''
 for name,netnames,width,clear in [('Power',powers,2000,350),('Motor',motors,1000,250),('Supply',logicpower,400,180)]:
  extra+='\n    (class '+name+' '+' '.join(netnames)+' (circuit (use_via "Via[0-1]_600:300_um")) (rule (width '+str(width)+') (clearance '+str(clear)+')))'
 # Insert classes before network closing parenthesis.
 end=block.rfind('\n  )');block=block[:end]+extra+block[end:];dsn=dsn[:cs]+block+dsn[ce:]
 # Net-tie copper is not a pad in Specctra. Keep its tiny bridge away from unrelated traces.
 st=dsn.index('    (via ');dsn=dsn[:st]+'    (keepout NT1_COPPER (rect F.Cu 174000 -71000 176000 -69000))\n'+dsn[st:]
 dfile.write_text(dsn,encoding='utf-8')
 print('Local Specctra export completed: explicit power/motor/supply widths, net-tie keepout')
else:
 if not pcbnew.ImportSpecctraSES(b,str(p/'design'/'routing'/'guard.ses')):raise RuntimeError('SES import failed')
 # Keep a real B.Cu reference plane under each RF feed-through, isolated from motor/logic returns.
 fps={f.GetReference():f for f in b.GetFootprints()}
 for ref,x1,x2 in [('J36',22,58),('J38',82,118)]:
  shield=next(x for x in fps[ref].Pads() if x.GetNumber()=='2')
  zone=pcbnew.ZONE(b);zone.SetLayer(pcbnew.B_Cu);zone.SetNet(shield.GetNet());zone.SetLocalClearance(pcbnew.FromMM(.35));zone.SetMinThickness(pcbnew.FromMM(.25));zone.SetPadConnection(pcbnew.ZONE_CONNECTION_FULL)
  outline=zone.Outline();outline.NewOutline()
  for x,y in [(x1,250),(x2,250),(x2,270),(x1,270)]:outline.Append(v(x,y))
  b.Add(zone)
 # Drop exact duplicates if a session repeats protected pre-route segments.
 seen=set()
 for t in list(b.GetTracks()):
  endpoints=tuple(sorted([(t.GetStart().x,t.GetStart().y),(t.GetEnd().x,t.GetEnd().y)]))
  key=(type(t).__name__,t.GetNetCode(),t.GetLayer(),(t.GetWidth(pcbnew.F_Cu) if isinstance(t,pcbnew.PCB_VIA) else t.GetWidth()),endpoints)
  if key in seen:b.Remove(t)
  else:seen.add(key)
 # Freerouting cannot certify timing, isolation, RF impedance or power current capacity.
 pcbnew.SaveBoard(str(p/'cm5-guard-A.kicad_pcb'),b)
 print('Imported local routing session;',len(seen),'unique track/via items')








