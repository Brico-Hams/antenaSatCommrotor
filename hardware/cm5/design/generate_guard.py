"""Generate review-only CM5 guard using KiCad 10 libraries. Never a fabrication release.
Run with KiCad's bundled Python and --kicad-root. Inputs/outputs stay in hardware/cm5.
"""
import argparse, csv, json, re, uuid, pathlib, copy, xml.etree.ElementTree as ET
import pcbnew
P=pathlib.Path(__file__).resolve().parents[1]
a=argparse.ArgumentParser(); a.add_argument('--kicad-root',required=True); a.add_argument('--board-only',action='store_true'); args=a.parse_args()
K=pathlib.Path(args.kicad_root); LIB=K/'share'/'kicad'/'symbols'; FP=K/'share'/'kicad'/'footprints'
def uid(): return str(uuid.uuid4())
def parse(s):
    tokens=re.findall(r'"(?:\\.|[^"\\])*"|[^\s()]+|[()]',s); stack=[]; root=None
    for t in tokens:
        if t=='(':
            n=[]
            if stack: stack[-1].append(n)
            stack.append(n)
        elif t==')': root=stack.pop()
        else: stack[-1].append(t)
    return root
def q(s): return json.dumps(str(s),ensure_ascii=False)
def dump(n): return '('+' '.join(dump(v) if isinstance(v,list) else v for v in n)+')'
def child(n,key): return next((x for x in n if isinstance(x,list) and x[0]==key),None)
def children(n,key): return [x for x in n if isinstance(x,list) and x[0]==key]
def val(n): return json.loads(n) if n.startswith('"') else n
cache={}
def sym(lib,name):
    if lib=='Guard':
        root=parse((P/'Guard.kicad_sym').read_text(encoding='utf-8'))
        return next(x for x in children(root,'symbol') if val(x[1])==name)
    key=lib+':'+name
    if key in cache: return copy.deepcopy(cache[key])
    root=parse((LIB/(lib+'.kicad_sym')).read_text(encoding='utf-8'))
    node=next(x for x in children(root,'symbol') if val(x[1])==name); ext=child(node,'extends')
    if ext:
        base=sym(lib,val(ext[1])); base[1]=q(name)
        for x in children(node,'property'):
            old=next((v for v in children(base,'property') if v[1]==x[1]),None)
            if old: base.remove(old)
            base.append(copy.deepcopy(x))
        node=base
        for sub in children(node,'symbol'):
            sub[1]=q(name+re.search(r'(_\d+_\d+)$',val(sub[1])).group(1))
    cache[key]=copy.deepcopy(node); return node
parts=[]; inst=[]; graphic=[]; definitions={}; refs={}; rootid=str(uuid.uuid5(uuid.NAMESPACE_URL,'PortableSatStation-CM5-guard-A')); occupied=0
RFP='Resistor_SMD:R_0603_1608Metric'; CFP='Capacitor_SMD:C_0603_1608Metric'
def text(s,x,y,size=2): graphic.append(f'(text {q(s)} (at {x} {y} 0) (effects (font (size {size} {size})) (justify left)) (uuid {uid()}))')
def add(lib,name,ref,value,footprint,nets,x=None,y=None,mpn='',dnp=False,unit=1,external=False):
    global occupied
    node=sym(lib,name); key=lib+':'+name
    if key not in definitions:
        node[1]=q(key); definitions[key]=dump(node)
    if x is None:
        x=25.4+(occupied%12)*76.2; y=50.8+(occupied//12)*55.88; occupied+=1
    su=uid(); props=''
    for pn,pv,py in [('Reference',ref,y-13),('Value',value,y-10),('Footprint',footprint,y),('Datasheet','',y),('MPN',mpn,y)]:
        hide=' (hide yes)' if pn not in ('Reference','Value') else ''
        props+=f'(property {q(pn)} {q(pv)} (at {x} {py} 0) {hide} (effects (font (size 1.27 1.27))))'
    pins=[]
    for sub in children(node,'symbol'):
        sn=val(sub[1]); match=re.search(r'_(\d+)_(\d+)$',sn)
        if not match or int(match[1]) not in (0,unit) or int(match[2]) not in (0,1): continue
        pins+=children(sub,'pin')
    for pin in pins:
        num=val(child(pin,'number')[1]); at=child(pin,'at'); dx,dy,ang=map(float,at[1:4]); px=x+dx; py=y-dy
        net=nets.get(num)
        if net is None:
            graphic.append(f'(no_connect (at {px:g} {py:g}) (uuid {uid()}))')
        else:
            # Labels are wired away from each symbol to avoid accidental pin shorts.
            ex=px+(-5.08 if ang==0 else 5.08 if ang==180 else 0); ey=py+(5.08 if ang==90 else -5.08 if ang==270 else 0)
            graphic.append(f'(wire (pts (xy {px:g} {py:g}) (xy {ex:g} {ey:g})) (stroke (width 0) (type default)) (uuid {uid()}))')
            graphic.append(f'(label {q(net)} (at {ex:g} {ey:g} 0) (effects (font (size 0.9 0.9)) (justify left bottom)) (uuid {uid()}))')
    inst.append(f'(symbol (lib_id {q(key)}) (at {x} {y} 0) (unit {unit}) (in_bom {"no" if external or ref=="NT1" else "yes"}) (on_board {"no" if external else "yes"}) (dnp {"yes" if dnp else "no"}) (uuid {su}) {props} (instances (project "cm5-guard-A" (path "/{rootid}" (reference {q(ref)}) (unit {unit})))))')
    if ref not in refs:
        part=dict(ref=ref,value=value,footprint=footprint,nets=nets,mpn=mpn,dnp=dnp,external=external,uuid=su); parts.append(part); refs[ref]=part
    else: refs[ref]['nets'].update(nets)
    return ref
counts={'R':0,'C':0,'J':0,'Q':0,'D':0}
def passive(kind,value,n1,n2,mpn=''):
    counts[kind]+=1; ref=kind+str(counts[kind]); return add('Device',kind,ref,value,RFP if kind=='R' else CFP,{'1':n1,'2':n2},mpn=mpn)
def r(value,a,b): return passive('R',value,a,b,{'10k':'RC0603FR-0710KL','4.7k':'RC0603FR-074K7L','1k':'RC0603FR-071KL','5.1k':'RC0603FR-075K1L','1M':'RC0603FR-071ML','100k':'RC0603FR-07100KL'}.get(value,''))
def c(value,a,b): return passive('C',value,a,b,{'100n':'GRM188R71C104KA01D','1u':'GRM188R71C105KA12D','10u':'GRM21BR61A106KE19L'}.get(value,''))
def conn(ref,nets,value='',fp=None,mpn='',dnp=False):
    n=len(nets); return add('Connector_Generic',f'Conn_01x{n:02}',ref,value or f'1x{n}',fp or f'Connector_PinHeader_2.54mm:PinHeader_1x{n:02}_P2.54mm_Vertical',{str(i+1):v for i,v in enumerate(nets)},mpn=mpn,dnp=dnp)
if not args.board_only:
    cm=sym('Device','L_Coupled');cm[1]=q('WE744824622')
    for sub in children(cm,'symbol'):
        sub[1]=q('WE744824622'+re.search(r'(_\d+_\d+)$',val(sub[1])).group(1))
        for pin in children(sub,'pin'):
            pn=child(pin,'number');pn[1]=q({'1':'1','2':'4','3':'2','4':'3'}[val(pn[1])])
    for prop in children(cm,'property'):
        if val(prop[1])=='Value':prop[2]=q('WE744824622')
    (P/'Guard.kicad_sym').write_text('(kicad_symbol_lib (version 20231120) (generator "kicad_symbol_editor") '+dump(cm)+')',encoding='utf-8')
    text('CM5 GUARD A - ENGINEERING REVIEW ONLY - DO NOT FABRICATE / NO MOTOR OR TX OPERATION',20,20,3)
    text('Every net is labelled. NC contacts to GND: open wire inhibits hardware; external DC E-stop is mandatory.',20,27)
    text('Powerpole / EMI / isolated power / CM5IO PD / RF bulkhead SMA stay EXTERNAL, unresolved ratings.',20,34)
    j=json.loads((P/'interface.json').read_text()); gpio={str(i['headerPin']):i['signal'] for i in j['gpio']}
    for pin in [6,9,14,20,25,30,34,39]: gpio[str(pin)]='GND_LOGIC'
    add('Connector_Generic','Conn_02x20_Odd_Even','J1','CM5IO GPIO VIO=3V3 ONLY','Connector_IDC:IDC-Header_2x20_P2.54mm_Vertical',gpio,mpn='3020-40-0300-00')
    conn('J2',['AUX_5V_ISOLATED','GND_LOGIC'],'ISOLATED 5V external PSU','Connector_PinHeader_2.54mm:PinHeader_1x02_P2.54mm_Vertical',dnp=True)
    add('Regulator_Linear','AP2112K-3.3','U1','AP2112K-3.3TRG1','Package_TO_SOT_SMD:SOT-23-5',{'1':'AUX_5V_ISOLATED','2':'GND_LOGIC','3':'AUX_5V_ISOLATED','5':'V3V3'},mpn='AP2112K-3.3TRG1')
    c('1u','AUX_5V_ISOLATED','GND_LOGIC'); c('1u','V3V3','GND_LOGIC')
    add('Interface_Expansion','MCP23017x-x-SO','U2','MCP23017-E/SO','Package_SO:SOIC-28W_7.5x17.9mm_P1.27mm',{'9':'V3V3','10':'GND_LOGIC','12':'I2C1_SCL','13':'I2C1_SDA','15':'GND_LOGIC','16':'GND_LOGIC','17':'GND_LOGIC','18':'LOGIC_RESET_N','21':'AZ_ENABLE_REQUEST','22':'EL_ENABLE_REQUEST','23':'POL_ENABLE_REQUEST','24':'MOTOR_PERMIT_FEEDBACK_N','25':'PTT_VHF_FEEDBACK_N','26':'PTT_UHF_FEEDBACK_N','27':'PA_VHF_FAULT_N','28':'PA_UHF_FAULT_N'},mpn='MCP23017-E/SO')
    r('4.7k','V3V3','I2C1_SDA'); r('4.7k','V3V3','I2C1_SCL')
    add('Interface_Expansion','TCA9548APWR','U3','TCA9548APWR','Package_SO:TSSOP-24_4.4x7.8mm_P0.65mm',{'1':'GND_LOGIC','2':'GND_LOGIC','3':'TCA9548A_RESET_N','12':'GND_LOGIC','21':'GND_LOGIC','22':'I2C1_SCL','23':'I2C1_SDA','24':'V3V3',**{str(4+i*2+(1 if i>=4 else 0)):f'SDA_CH{i}' for i in range(5)},**{str(5+i*2+(1 if i>=4 else 0)):f'SCL_CH{i}' for i in range(5)}},mpn='TCA9548APWR')
    r('10k','V3V3','TCA9548A_RESET_N')
    for i,role in enumerate(['AZ AS5600 0x36','EL AS5600 0x36','POL AS5600 0x36','LIS3MDL','LSM6DSOX']):
        conn(f'J{3+i}',['GND_LOGIC','V3V3',f'SDA_CH{i}',f'SCL_CH{i}'],role,'Connector_JST:JST_PH_B4B-PH-K_1x04_P2.00mm_Vertical',mpn='B4B-PH-K-S(LF)(SN)')
        r('4.7k','V3V3',f'SDA_CH{i}'); r('4.7k','V3V3',f'SCL_CH{i}')
    conn('J8',['GND_LOGIC','V3V3','GNSS_UART_RX','GNSS_UART_TX','GNSS_PPS'],'GNSS PID746 custom harness',mpn='M20-9990545')
    limits=[f'{ax}_LIMIT_{end}_N' for ax in ['AZ','EL','POL'] for end in ['MIN','MAX']]
    for i,net in enumerate(limits):
        conn(f'J{9+i}',['GND_LOGIC',net],net+' NC contact',mpn='M20-9990245'); r('10k','V3V3',net); c('100n',net,'GND_LOGIC')
        inp=[1,3,5,9,11,13][i]; out=[2,4,6,8,10,12][i]
        add('74xx','74HC14','U4','SN74HC14DR','Package_SO:SOIC-14_3.9x8.7mm_P1.27mm',{str(inp):net,str(out):f'LIMIT_OK_{i}'},unit=i+1,mpn='SN74HC14DR')
    add('74xx','74HC14','U4','SN74HC14DR','Package_SO:SOIC-14_3.9x8.7mm_P1.27mm',{'14':'V3V3','7':'GND_LOGIC'},unit=7,mpn='SN74HC14DR')
    conn('J15',['GND_LOGIC','ESTOP_AUX_N'],'E-stop isolated AUX NC only',mpn='M20-9990245'); r('10k','V3V3','ESTOP_AUX_N'); c('100n','ESTOP_AUX_N','GND_LOGIC')
    # Second Schmitt IC: E-stop inversion, reset inversion, permit inversion; unused inputs grounded.
    u5=[{'1':'ESTOP_AUX_N','2':'ESTOP_OK'},{'3':'RESET_RC','4':'LOGIC_RESET'},{'5':'LOGIC_RESET','6':'LOGIC_RESET_N'},{'9':'SAFE_N','8':'SAFE_OK'},{'11':'GND_LOGIC'},{'13':'GND_LOGIC'},{'14':'V3V3','7':'GND_LOGIC'}]
    for i,n in enumerate(u5): add('74xx','74HC14','U5','SN74HC14DR','Package_SO:SOIC-14_3.9x8.7mm_P1.27mm',n,unit=i+1,mpn='SN74HC14DR')
    r('10k','V3V3','RESET_RC'); c('1u','RESET_RC','GND_LOGIC')
    add('74xx','74HC123','U6','SN74HC123DR','Package_SO:SOIC-16_3.9x9.9mm_P1.27mm',{'1':'GND_LOGIC','2':'WATCHDOG_HEARTBEAT','3':'LOGIC_RESET_N','13':'WATCHDOG_OK','14':'WD_C','15':'WD_RC'},unit=1,mpn='SN74HC123DR')
    add('74xx','74HC123','U6','SN74HC123DR','Package_SO:SOIC-16_3.9x9.9mm_P1.27mm',{'9':'GND_LOGIC','10':'GND_LOGIC','11':'GND_LOGIC'},unit=2,mpn='SN74HC123DR')
    add('74xx','74HC123','U6','SN74HC123DR','Package_SO:SOIC-16_3.9x9.9mm_P1.27mm',{'16':'V3V3','8':'GND_LOGIC'},unit=3,mpn='SN74HC123DR')
    r('1M','V3V3','WD_RC'); c('1u','WD_RC','WD_C'); r('10k','WATCHDOG_HEARTBEAT','GND_LOGIC')
    add('74xx','74LS30','U7','SN74HC30DR','Package_SO:SOIC-14_3.9x8.7mm_P1.27mm',{'1':'LIMIT_OK_0','2':'LIMIT_OK_1','3':'LIMIT_OK_2','4':'LIMIT_OK_3','5':'LIMIT_OK_4','6':'LIMIT_OK_5','11':'ESTOP_OK','12':'WATCHDOG_OK','8':'SAFE_N'},unit=1,mpn='SN74HC30DR')
    add('74xx','74LS30','U7','SN74HC30DR','Package_SO:SOIC-14_3.9x8.7mm_P1.27mm',{'14':'V3V3','7':'GND_LOGIC'},unit=2,mpn='SN74HC30DR')
    # 3 quad AND packages: common motor arm, three per-axis requests, two PTT requests.
    gateplans=[('U8',[('REARM_PERMIT','MOTOR_ARM_REQUEST','MOTOR_PERMIT'),('MOTOR_PERMIT','AZ_ENABLE_REQUEST','AZ_GATE'),('MOTOR_PERMIT','EL_ENABLE_REQUEST','EL_GATE'),('MOTOR_PERMIT','POL_ENABLE_REQUEST','POL_GATE')]),('U9',[('REARM_PERMIT','PTT_VHF_REQUEST','PTT_VHF_GATE'),('REARM_PERMIT','PTT_UHF_REQUEST','PTT_UHF_GATE'),('GND_LOGIC','GND_LOGIC',None),('GND_LOGIC','GND_LOGIC',None)])]
    for ref,plan in gateplans:
        for i,(a,b,o) in enumerate(plan):
            nums=[(1,2,3),(4,5,6),(9,10,8),(12,13,11)][i]; n={str(nums[0]):a,str(nums[1]):b}
            if o:n[str(nums[2])]=o
            add('74xx','74LS08',ref,'SN74HC08DR','Package_SO:SOIC-14_3.9x8.7mm_P1.27mm',n,unit=i+1,mpn='SN74HC08DR')
        add('74xx','74LS08',ref,'SN74HC08DR','Package_SO:SOIC-14_3.9x8.7mm_P1.27mm',{'14':'V3V3','7':'GND_LOGIC'},unit=5,mpn='SN74HC08DR')
    for net in ['MOTOR_ARM_REQUEST','AZ_ENABLE_REQUEST','EL_ENABLE_REQUEST','POL_ENABLE_REQUEST','PTT_VHF_REQUEST','PTT_UHF_REQUEST']: r('10k',net,'GND_LOGIC')
    for i,ax in enumerate(['AZ','EL','POL']):
        # Split verified top-view pin sequence into two conventional 1x8 sockets, not a guessed StepStick library.
        conn(f'J{16+i*3}',[f'{ax}_EN_N','SPI1_MOSI','SPI1_SCLK',f'SPI1_CS{[0,1,2][i]}_{ax}','SPI1_MISO',None,'GND_LOGIC','GND_LOGIC'],ax+' v1.5 LEFT top-view','Connector_PinSocket_2.54mm:PinSocket_1x08_P2.54mm_Vertical',mpn='M20-7820842')
        conn(f'J{17+i*3}',['VMOT_ESTOP','GND_MOTOR',f'{ax}_M2B',f'{ax}_M2A',f'{ax}_M1A',f'{ax}_M1B','V3V3','GND_MOTOR'],ax+' v1.5 RIGHT top-view','Connector_PinSocket_2.54mm:PinSocket_1x08_P2.54mm_Vertical',mpn='M20-7820842')
        conn(f'J{18+i*3}',[f'{ax}_M1A',f'{ax}_M1B',f'{ax}_M2A',f'{ax}_M2B'],ax+' MOTOR; rating TBD',dnp=True)
        r('10k','V3V3',f'{ax}_EN_N'); r('10k','V3V3',f'SPI1_CS{i}_{ax}'); r('10k',f'{ax}_GATE','GND_LOGIC')
        add('Transistor_FET','2N7002',f'Q{i+1}','2N7002','Package_TO_SOT_SMD:SOT-23',{'1':f'{ax}_GATE','2':'GND_LOGIC','3':f'{ax}_EN_N'},mpn='2N7002,215')
        # DCO is not a verified driver fault. BCM fault goes only to a separate isolated fault connector.
        conn(f'J{25+i}',['GND_LOGIC',f'FAULT_{ax}_N'],ax+' FAULT isolated OD only',mpn='M20-9990245'); r('10k','V3V3',f'FAULT_{ax}_N')
    add('Device','NetTie_2','NT1','MOTOR_LOGIC STAR REFERENCE','NetTie:NetTie-2_SMD_Pad2.0mm',{'1':'GND_MOTOR','2':'GND_LOGIC'})
    conn('J28',['VMOT_ESTOP','GND_MOTOR'],'External fused DC E-stop motor supply - TBD',dnp=True)
    conn('J29',['GND_LOGIC','PA_VHF_FAULT_N','PA_UHF_FAULT_N'],'Qualified isolated PA faults only',mpn='M20-9990345')
    for n in ['PA_VHF_FAULT_N','PA_UHF_FAULT_N']:r('10k','V3V3',n)
    for i,band in enumerate(['VHF','UHF']):
        r('1k','V3V3',f'PTT_{band}_LED_A')
        add('Isolator','LTV-817',f'U{10+i}','LTV-817S','Package_DIP:SMDIP-4_W7.62mm',{'1':f'PTT_{band}_LED_A','2':f'PTT_{band}_LED_K','3':f'PTT_{band}_RETURN_ISO','4':f'PTT_{band}_OUT_ISO'},mpn='LTV-817S')
        add('Transistor_FET','2N7002',f'Q{4+i}','2N7002','Package_TO_SOT_SMD:SOT-23',{'1':f'PTT_{band}_GATE','2':'GND_LOGIC','3':f'PTT_{band}_LED_K'},mpn='2N7002,215'); r('10k',f'PTT_{band}_GATE','GND_LOGIC')
        conn(f'J{30+i}',[f'PTT_{band}_OUT_ISO',f'PTT_{band}_RETURN_ISO'],band+' PTT external limits TBD',mpn='M20-9990245')
        # Feedback is external confirmation, not loopback of request.
        conn(f'J{32+i}',['GND_LOGIC',f'PTT_{band}_FEEDBACK_N'],band+' actual isolated feedback',mpn='M20-9990245'); r('10k','V3V3',f'PTT_{band}_FEEDBACK_N')
    add('Transistor_FET','2N7002','Q6','2N7002','Package_TO_SOT_SMD:SOT-23',{'1':'MOTOR_PERMIT','2':'GND_LOGIC','3':'MOTOR_PERMIT_FEEDBACK_N'},mpn='2N7002,215'); r('10k','V3V3','MOTOR_PERMIT_FEEDBACK_N')
    # Manual rearm: asynchronous fault/POR clear, edge-clocked latch, requests must all be LOW at rearm.
    conn('J40',['V3V3','REARM_BUTTON'],'LOCAL NO REARM button',mpn='M20-9990245')
    r('10k','REARM_BUTTON','GND_LOGIC'); c('100n','REARM_BUTTON','GND_LOGIC')
    rearm_inv=[{'1':'REARM_BUTTON','2':'REARM_BUTTON_N'},{'3':'REARM_BUTTON_N','4':'REARM_CLK'}, {'5':'MOTOR_ARM_REQUEST','6':'ARM_IDLE'}, {'9':'PTT_VHF_REQUEST','8':'VHF_IDLE'}, {'11':'PTT_UHF_REQUEST','10':'UHF_IDLE'}, {'13':'GND_LOGIC'}, {'14':'V3V3','7':'GND_LOGIC'}]
    for i,n in enumerate(rearm_inv): add('74xx','74HC14','U12','SN74HC14DR','Package_SO:SOIC-14_3.9x8.7mm_P1.27mm',n,unit=i+1,mpn='SN74HC14DR')
    rearm_and=[('ARM_IDLE','VHF_IDLE','IDLE_AV'),('IDLE_AV','UHF_IDLE','ALL_REQUESTS_IDLE'),('SAFE_OK','LOGIC_RESET_N','LATCH_CLEAR_N'),('SAFE_OK','REARMED','REARM_PERMIT')]
    for i,(a,b,o) in enumerate(rearm_and):
        nums=[(1,2,3),(4,5,6),(9,10,8),(12,13,11)][i]
        add('74xx','74LS08','U14','SN74HC08DR','Package_SO:SOIC-14_3.9x8.7mm_P1.27mm',{str(nums[0]):a,str(nums[1]):b,str(nums[2]):o},unit=i+1,mpn='SN74HC08DR')
    add('74xx','74LS08','U14','SN74HC08DR','Package_SO:SOIC-14_3.9x8.7mm_P1.27mm',{'14':'V3V3','7':'GND_LOGIC'},unit=5,mpn='SN74HC08DR')
    add('74xx','74HC74','U13','SN74HC74DR','Package_SO:SOIC-14_3.9x8.7mm_P1.27mm',{'1':'LATCH_CLEAR_N','2':'ALL_REQUESTS_IDLE','3':'REARM_CLK','4':'V3V3','5':'REARMED'},unit=1,mpn='SN74HC74DR')
    add('74xx','74HC74','U13','SN74HC74DR','Package_SO:SOIC-14_3.9x8.7mm_P1.27mm',{'13':'GND_LOGIC','12':'GND_LOGIC','11':'GND_LOGIC','10':'V3V3'},unit=2,mpn='SN74HC74DR')
    add('74xx','74HC74','U13','SN74HC74DR','Package_SO:SOIC-14_3.9x8.7mm_P1.27mm',{'14':'V3V3','7':'GND_LOGIC'},unit=3,mpn='SN74HC74DR')
    for i in range(3): c('100n','V3V3','GND_LOGIC')
    # Candidate DC front-end. Holders have NO fuse insert rating selected and are DNP/locked out.
    terminal='TerminalBlock_Phoenix:TerminalBlock_Phoenix_MKDS-3-2-5.08_1x02_P5.08mm_Horizontal'
    conn('J41',['BAT_POS','GND_MOTOR'],'Powerpole pigtail AFTER pack fuse and disconnect',terminal,mpn='1711725',dnp=True)
    add('Device','Fuse','F1','MAIN INSERT TBD - EMPTY','Fuse:FuseHolder_Blade_ATO_Littelfuse_FLR_178.6165',{'1':'BAT_POS','2':'BAT_FUSED'},mpn='178.6165.0001',dnp=True)
    # Reverse battery PMOS candidate: body diode initially charges source; gate-source zener clamps stress.
    add('Transistor_FET','Q_PMOS_GDS','Q7','AOD4185 -40V candidate','Package_TO_SOT_SMD:TO-252-2',{'1':'POWER_GATE','2':'BAT_FUSED','3':'BAT_PROTECTED'},mpn='AOD4185',dnp=True)
    add('Device','D_Zener','D1','BZT52C12 12V','Diode_SMD:D_SOD-123',{'1':'BAT_PROTECTED','2':'POWER_GATE'},mpn='BZT52C12-7-F',dnp=True)
    add('Device','D_TVS','D2','SMBJ18A candidate','Diode_SMD:D_SMB',{'1':'BAT_FUSED','2':'GND_MOTOR'},mpn='SMBJ18A',dnp=True)
    power_rc_refs=[r('100k','POWER_GATE','GND_MOTOR'),c('100n','POWER_GATE','BAT_PROTECTED')]
    # Independent branches. Fuse inserts must protect wires/contacts/traces, selected after measured loads.
    for ref,out in [('F2','LOGIC_BAT_FUSED'),('F3','MOTOR_BRANCH_FUSED'),('F4','CM5IO_BRANCH_FUSED'),('F5','VHF_BRANCH_FUSED'),('F6','UHF_BRANCH_FUSED')]:
        add('Device','Fuse',ref,'BRANCH INSERT TBD - EMPTY','Fuse:FuseHolder_Blade_ATO_Littelfuse_FLR_178.6165',{'1':'BAT_PROTECTED','2':out},mpn='178.6165.0001',dnp=True)
    for ref,net,role in [('J42','MOTOR_BRANCH_FUSED','DC-RATED EXTERNAL ESTOP OUT'),('J43','CM5IO_BRANCH_FUSED','EXTERNAL QUALIFIED USB-C PD CONVERTER'),('J44','VHF_BRANCH_FUSED','VHF PA external'),('J45','UHF_BRANCH_FUSED','UHF PA external')]:
        conn(ref,[net,'GND_MOTOR'],role,terminal,mpn='1711725',dnp=True)
    # Genuine 6A common-mode candidate: BOTH DC supply and return pass through coupled windings.
    add('Guard','WE744824622','L1','WE-CMB 744824622 2.2mH 6A candidate','Guard:WE744824622',{'1':'LOGIC_BAT_FUSED','4':'EMI_LOGIC_POS','2':'GND_MOTOR','3':'EMI_LOGIC_RETURN'},mpn='744824622',dnp=True)
    conn('J46',['EMI_LOGIC_POS','EMI_LOGIC_RETURN'],'EXTERNAL ISOLATED 5V converter primary',terminal,mpn='1711725',dnp=True)
    # Input damping candidate on logic branch only, not an undamped differential LC.
    add('Device','R','R80','1R 2W DAMPING candidate','Resistor_SMD:R_2512_6332Metric',{'1':'EMI_LOGIC_POS','2':'DAMP_CAP_POS'},mpn='CRCW25121R00FKEGHP',dnp=True)
    add('Device','C_Polarized','C80','47u 50V candidate','Capacitor_THT:CP_Radial_D6.3mm_P2.50mm',{'1':'DAMP_CAP_POS','2':'EMI_LOGIC_RETURN'},mpn='EEU-FR1H470',dnp=True)
    # USB2 DEVICE pass-through, no host, no PD source, no VBUS-to-logic link.
    add('Connector','USB_C_Receptacle_USB2.0_16P','J34','USB4105-GF-A USB2 DEVICE ONLY','Connector_USB:USB_C_Receptacle_GCT_USB4105-xx-A_16P_TopMnt_Horizontal',{'A1':'USB_RETURN','A4':'USB_VBUS_DEVICE','A5':'USB_CC1','A6':'USB_DP','A7':'USB_DM','A9':'USB_VBUS_DEVICE','A12':'USB_RETURN','B1':'USB_RETURN','B4':'USB_VBUS_DEVICE','B5':'USB_CC2','B6':'USB_DP','B7':'USB_DM','B9':'USB_VBUS_DEVICE','B12':'USB_RETURN','S1':'CHASSIS_USB'},mpn='USB4105-GF-A',dnp=True)
    r('5.1k','USB_CC1','USB_RETURN'); r('5.1k','USB_CC2','USB_RETURN')
    conn('J35',['USB_VBUS_DEVICE','USB_RETURN','USB_DM','USB_DP'],'External USB2 device (no codec included)',dnp=True)
    for i in range(1,10): c('100n','V3V3','GND_LOGIC')
    for net in ['GND_LOGIC','AUX_5V_ISOLATED']:
        add('power','PWR_FLAG',f'#FLG0{len([p for p in parts if p["ref"].startswith("#")])+1}','PWR_FLAG','',{'1':net})
    # Physical SMA passive feed-through test pairs: never a TX-to-RX merge or a PA/filter network.
    for i,role in enumerate(['VHF_FEED_IN','VHF_FEED_OUT','UHF_FEED_IN','UHF_FEED_OUT']):
        band='VHF' if i<2 else 'UHF'
        add('Connector','Conn_Coaxial',f'J{36+i}',role,'Connector_Coaxial:SMA_Amphenol_132134_Vertical',{'1':f'RF_{band}_LINE','2':f'RF_{band}_GND'},mpn='132134')
    text('POWER CANDIDATES DNP: empty fuseholders, unqualified ratings; no motor/PA/battery operation authorized.',25.4,820.42)
    text('Manual rearm latch requires healthy NC/E-stop/watchdog and arm/PTT requests LOW at local button edge.',25.4,828.04)
    text('SMA pairs are passive feed-through ONLY. No PA/filter/RHCP-LHCP integration or RF validation claimed.',25.4,835.66)
    content='(kicad_sch (version 20250820) (generator "eeschema") (uuid '+rootid+') (paper "A0") (title_block (title "CM5 Guard AZ/EL/POL") (rev "A review only") (comment 1 "DO NOT FABRICATE - POWER QUALIFICATION PENDING")) (lib_symbols '+' '.join(definitions.values())+') '+' '.join(graphic+inst)+')'
    (P/'cm5-guard-A.kicad_sch').write_text(content,encoding='utf-8')
    (P/'design'/'components.json').write_text(json.dumps(parts,indent=2),encoding='utf-8')
    # The battery gate RC is a power-stage candidate, not a qualified populated logic part.
    for pref in power_rc_refs:
        part=refs[pref];part['dnp']=True
    # Preserve DNP state in both actual symbol instances and metadata.
    actual=(P/'cm5-guard-A.kicad_sch').read_text(encoding='utf-8')
    for pref in power_rc_refs:
        sid=refs[pref]['uuid'];beg=actual.index('(symbol (lib_id',actual.index('(lib_symbols'))
        target=next(t for t in inst if '(uuid '+sid+')' in t)
        actual=actual.replace(target,target.replace('(dnp no)','(dnp yes)'))
    (P/'cm5-guard-A.kicad_sch').write_text(actual,encoding='utf-8')
    (P/'design'/'components.json').write_text(json.dumps(parts,indent=2),encoding='utf-8')
    print('Schematic',len(parts),'components',len(inst),'symbol units')
else:
    parts=json.loads((P/'design'/'components.json').read_text()); tree=ET.parse(P/'reports'/'cm5-guard-A.net.xml')
    nets={}; padnets={}; board=pcbnew.BOARD(); board.SetCopperLayerCount(2)
    for n in tree.findall('./nets/net'):
        name=n.attrib['name']; ni=pcbnew.NETINFO_ITEM(board,name,len(nets)+1); board.Add(ni); nets[name]=ni
        for p in n.findall('node'): padnets[(p.attrib['ref'],p.attrib['pin'])]=ni
    # Module geometry from pinned Watterott v1.5: 12.70mm between column centerlines, 2.54mm pitch.
    fixed={'J1':(208,24),'U2':(160,45),'U3':(180,45),'J34':(220,255),'J35':(235,265),
           'L1':(252,185),'J41':(278,20),'F1':(240,25),'Q7':(257,43),'D1':(242,48),'D2':(222,40),
           'F2':(240,75),'F3':(240,95),'F4':(240,115),'F5':(240,135),'F6':(240,155),
           'J42':(275,95),'J43':(275,115),'J44':(275,135),'J45':(275,155),'J46':(252,205),'R80':(230,200),'C80':(235,217),
           'J36':(30,260),'J37':(50,260),'J38':(90,260),'J39':(110,260),'NT1':(175,70)}
    for i in range(3):
        x=25+50*i
        fixed['J'+str(16+3*i)]=(x,25);fixed['J'+str(17+3*i)]=(x+12.7,25)
        fixed['J'+str(18+3*i)]=(x+10,58)
    i=0; mounted=[]; pretty=P/'Guard.pretty';pretty.mkdir(exist_ok=True)
    def v(x,y):return pcbnew.VECTOR2I(pcbnew.FromMM(x),pcbnew.FromMM(y))
    def cm_footprint():
        fp=pcbnew.FOOTPRINT(board);fp.SetReference('L1');fp.SetFPID(pcbnew.LIB_ID('Guard','WE744824622'));fp.SetAttributes(pcbnew.FP_THROUGH_HOLE)
        for num,x,y in [('1',-5,6),('2',5,6),('3',5,-6),('4',-5,-6)]:
            pad=pcbnew.PAD(fp);pad.SetNumber(num);pad.SetAttribute(pcbnew.PAD_ATTRIB_PTH);pad.SetShape(pcbnew.PAD_SHAPE_CIRCLE);pad.SetSize(v(2.5,2.5));pad.SetDrillSize(v(1.3,1.3));pad.SetLayerSet(pad.PTHMask());pad.SetPosition(v(x,y));fp.Add(pad)
        for layer,dx,dy in [(pcbnew.F_CrtYd,14.25,9.75),(pcbnew.F_Fab,13.75,9.25)]:
            for aa,bb in [((-dx,-dy),(dx,-dy)),((dx,-dy),(dx,dy)),((dx,dy),(-dx,dy)),((-dx,dy),(-dx,-dy))]:
                line=pcbnew.PCB_SHAPE(fp);line.SetShape(pcbnew.SHAPE_T_SEGMENT);line.SetLayer(layer);line.SetWidth(pcbnew.FromMM(.05));line.SetStart(v(*aa));line.SetEnd(v(*bb));fp.Add(line)
        fp.SetLibDescription('Original hole-pattern implementation from WE744824622 rev008 drawing: 10x12mm, holes1.3mm; windings1-4 and2-3; candidate, mechanical bench verification pending')
        fb=pcbnew.BOARD(); fb.Add(fp.Duplicate(False)); pcbnew.SaveBoard(str(P/'design'/'routing'/'cmc-footprint.kicad_pcb'),fb)
        saved=parse((P/'design'/'routing'/'cmc-footprint.kicad_pcb').read_text(encoding='utf-8'))
        fs=child(saved,'footprint');fs[1]=q('WE744824622')
        for field in ['path','sheetname','sheetfile']:
            item=child(fs,field)
            if item:fs.remove(item)
        (pretty/'WE744824622.kicad_mod').write_text(dump(fs),encoding='utf-8')
        return fp
    for p in parts:
        if not p['footprint']:continue
        lib,name=p['footprint'].split(':')
        fp=cm_footprint() if lib=='Guard' else pcbnew.FootprintLoad(str(FP/(lib+'.pretty')),name)
        if fp is None:raise RuntimeError(p['footprint'])
        fp.SetReference(p['ref']);fp.SetValue(p['value']);fp.SetFPID(pcbnew.LIB_ID(lib,name));fp.SetPath(pcbnew.KIID_PATH('/'+rootid+'/'+p['uuid']))
        if p['ref'] in fixed:x,y=fixed[p['ref']]
        else:
            x=20+(i%12)*16;y=88+(i//12)*13;i+=1
        fp.SetField('MPN',p['mpn']);fp.GetField('MPN').SetVisible(False);fp.SetPosition(v(x,y))
        # Labels readable between rows; values remain on fabrication drawing rather than obscuring silk.
        fp.Reference().SetPosition(v(x,y-3));fp.Reference().SetTextSize(v(.8,.8));fp.Reference().SetTextThickness(pcbnew.FromMM(.12))
        fp.Value().SetVisible(False)
        if p['ref'] in ['U10','U11']:fp.Reference().SetPosition(v(x,y-5))
        if p['ref']=='R17':fp.Reference().SetPosition(v(x+3.5,y))
        if p['ref']=='NT1':fp.SetAttributes(fp.GetAttributes() | pcbnew.FP_EXCLUDE_FROM_POS_FILES)
        if p['ref'] in ['Q7','C80','U2','U3','L1','J36','J37','J38','J39']:fp.Reference().SetPosition(v(x,y-12))
        if p['ref'] in ['J34','J41','J42','J43','J44','J45','J46','F1','F2','F3','F4','F5','F6']:fp.Reference().SetPosition(v(x,y-10))
        if p['dnp']:fp.SetDNP(True)
        for pad in fp.Pads():
            ni=padnets.get((p['ref'],pad.GetNumber()))
            if ni:pad.SetNet(ni)
        board.Add(fp);mounted.append(p)
    width=295;height=285
    for aa,bb in [((5,5),(width,5)),((width,5),(width,height)),((width,height),(5,height)),((5,height),(5,5))]:
        seg=pcbnew.PCB_SHAPE();seg.SetShape(pcbnew.SHAPE_T_SEGMENT);seg.SetLayer(pcbnew.Edge_Cuts);seg.SetWidth(pcbnew.FromMM(.1));seg.SetStart(v(*aa));seg.SetEnd(v(*bb));board.Add(seg)
    t=pcbnew.PCB_TEXT(board);t.SetText('CM5 GUARD A / REVIEW ONLY / DO NOT FABRICATE');t.SetPosition(v(112,12));t.SetTextSize(v(1.5,1.5));t.SetLayer(pcbnew.F_SilkS);board.Add(t)
    # Explicit mechanical module outline and clearance; no parts underneath module/cooling volume.
    for i in range(3):
        x=25+50*i
        for aa,bb in [((x-1.27,23.73),(x+13.97,23.73)),((x+13.97,23.73),(x+13.97,44.05)),((x+13.97,44.05),(x-1.27,44.05)),((x-1.27,44.05),(x-1.27,23.73))]:
            line=pcbnew.PCB_SHAPE(board);line.SetShape(pcbnew.SHAPE_T_SEGMENT);line.SetLayer(pcbnew.Dwgs_User);line.SetWidth(pcbnew.FromMM(.15));line.SetStart(v(*aa));line.SetEnd(v(*bb));board.Add(line)
    pcbnew.SaveBoard(str(P/'cm5-guard-A.kicad_pcb'),board)
    print('Board',len(mounted),'footprints; fixed module/SMA/power geometry; routing pending')







