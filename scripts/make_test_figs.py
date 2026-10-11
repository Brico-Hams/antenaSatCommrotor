"""Branded bench figures T1 (block diagram), T2 (GPIO tester table), T3 (mechanical fixture)."""
import sys, json, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from _figkit import frame, ROOT, NAVY, ORANGE, GREY
FIG = ROOT/'docs/testing/fig'; FIG.mkdir(parents=True, exist_ok=True)
SUF = {'es': '', 'en': '.en', 'hu': '.hu'}
def box(x, y, w, h, t, fill='#f4f7fa', stroke=NAVY, size=13, bold=False):
    lines = t.split('\n'); o = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{fill}" stroke="{stroke}" stroke-width="1.5"/>'
    for i, l in enumerate(lines):
        yy = y + h/2 + (i - (len(lines)-1)/2)*size*1.25 + size*0.35
        o += f'<text x="{x+w/2}" y="{yy:.1f}" font-size="{size}" text-anchor="middle" fill="#111"{" font-weight=\"bold\"" if bold else ""}>{l}</text>'
    return o
def arrow(x1, y1, x2, y2, col=NAVY, dash=False):
    return (f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{col}" stroke-width="2"{" stroke-dasharray=\"6 4\"" if dash else ""}/>'
            f'<circle cx="{x2}" cy="{y2}" r="3.5" fill="{col}"/>')
def poly(pts, col=NAVY, dash=False):
    d = ' '.join(f'{x},{y}' for x, y in pts)
    return (f'<polyline points="{d}" fill="none" stroke="{col}" stroke-width="2"' + (' stroke-dasharray="6 4"' if dash else '') + '/>'
            f'<circle cx="{pts[-1][0]}" cy="{pts[-1][1]}" r="3.5" fill="{col}"/>')
TXT = {
 'T1': dict(
  es=('Banco de pruebas pre-PCB', 'Diagrama de bloques del nivel B1 (electrónica sin PCB fabricada)',
      ['Fuente de banco con límite de corriente: empiece con 0,2 A.', 'La lógica (CM5, 5 V, 3,3 V) cuelga ANTES de la seta de parada.', 'Probar la parada con VMOT en los drivers (PWR-03).', 'Conectar el comprobador GPIO a la cabecera de 40 pines (PCB-05).', 'Medir con osciloscopio/analizador en TP1…TP4.'],
      dict(psu='Fuente de banco\n12 V · límite I', fuse='Fusible +\ninterruptor', stop='Seta NC\nenclavada (DC)', vmot='Bus VMOT', drv='3 × TMC5160\n(SPI1 CS0/1/2)', mot='3 × NEMA14\nAZ · EL · POL', cm5='CM5 + CM5IO\n(lógica 5 V / 3,3 V)', tst='Comprobador GPIO\n(LED + interruptores)', mux='TCA9548A 0x70\n3 × AS5600', exp='MCP23017 0x20', lim='6 finales NC', gnss='GNSS + PPS', pc='PC / teléfono\n(SSH, app BLE)', aux='contacto aux. NC → ESTOP_AUX_N', tp='TP1 VMOT · TP2 5 V · TP3 3,3 V · TP4 STEP/SPI')),
  en=('Pre-PCB test bench', 'Block diagram of level B1 (electronics without a fabricated PCB)',
      ['Current-limited bench supply: start at 0.2 A.', 'Logic (CM5, 5 V, 3.3 V) hangs BEFORE the stop switch.', 'Test the stop with VMOT on the drivers (PWR-03).', 'Plug the GPIO tester into the 40-pin header (PCB-05).', 'Measure with scope/analyser at TP1…TP4.'],
      dict(psu='Bench supply\n12 V · I limit', fuse='Fuse +\nmain switch', stop='Latching NC\nstop (DC)', vmot='VMOT bus', drv='3 × TMC5160\n(SPI1 CS0/1/2)', mot='3 × NEMA14\nAZ · EL · POL', cm5='CM5 + CM5IO\n(logic 5 V / 3.3 V)', tst='GPIO tester\n(LEDs + switches)', mux='TCA9548A 0x70\n3 × AS5600', exp='MCP23017 0x20', lim='6 NC limits', gnss='GNSS + PPS', pc='PC / phone\n(SSH, BLE app)', aux='NC aux. contact → ESTOP_AUX_N', tp='TP1 VMOT · TP2 5 V · TP3 3.3 V · TP4 STEP/SPI')),
  hu=('Gyártás előtti tesztpad', 'A B1 szint blokkvázlata (elektronika gyártott PCB nélkül)',
      ['Áramkorlátos labortáp: kezdd 0,2 A-rel.', 'A logika (CM5, 5 V, 3,3 V) a vészleállító ELŐTT csatlakozik.', 'Próbáld a leállítást VMOT-tal a meghajtókon (PWR-03).', 'Dugd a GPIO-tesztelőt a 40 tűs tüskesorra (PCB-05).', 'Mérj oszcilloszkóppal/analizátorral a TP1…TP4 pontokon.'],
      dict(psu='Labortáp\n12 V · I-korlát', fuse='Biztosíték +\nfőkapcsoló', stop='Reteszelt NC\nleállító (DC)', vmot='VMOT sín', drv='3 × TMC5160\n(SPI1 CS0/1/2)', mot='3 × NEMA14\nAZ · EL · POL', cm5='CM5 + CM5IO\n(logika 5 V / 3,3 V)', tst='GPIO-tesztelő\n(LED + kapcsolók)', mux='TCA9548A 0x70\n3 × AS5600', exp='MCP23017 0x20', lim='6 NC végállás', gnss='GNSS + PPS', pc='PC / telefon\n(SSH, BLE app)', aux='NC segédérintkező → ESTOP_AUX_N', tp='TP1 VMOT · TP2 5 V · TP3 3,3 V · TP4 STEP/SPI'))),
 'T2': dict(
  es=('Comprobador del contrato GPIO', 'Las 26 señales de hardware/cm5/interface.json y su elemento de prueba',
      ['Enchufar a la cabecera de 40 pines de la CM5IO; solo 3,3 V.', 'Salidas: LED con 2,2 kΩ a GND; verificar el nivel seguro tras reiniciar.', 'Entradas: pull-up 10 kΩ + 330 Ω serie + interruptor a GND (cerrado = sano).', 'Buses a pines de sonda para el analizador lógico.'],
      dict(h=('BCM', 'Pin', 'Señal', 'Dir.', 'Elemento de prueba', 'Estado seguro'), out='LED + 2,2 kΩ', inp='Interruptor a GND', bus='Pin de sonda', io={'output': 'LED + 2,2 kΩ', 'input': 'Interruptor a GND', 'bidirectional': 'Pin de sonda'})),
  en=('GPIO-contract tester', 'The 26 signals of hardware/cm5/interface.json and their test element',
      ['Plug into the CM5IO 40-pin header; 3.3 V only.', 'Outputs: LED with 2.2 kΩ to GND; check the safe level after reboot.', 'Inputs: 10 kΩ pull-up + 330 Ω series + switch to GND (closed = healthy).', 'Buses break out to probe pins for the logic analyser.'],
      dict(h=('BCM', 'Pin', 'Signal', 'Dir.', 'Test element', 'Safe state'), io={'output': 'LED + 2.2 kΩ', 'input': 'Switch to GND', 'bidirectional': 'Probe pin'})),
  hu=('GPIO-szerződés tesztelő', 'A hardware/cm5/interface.json 26 jele és a hozzájuk tartozó tesztelem',
      ['Dugd a CM5IO 40 tűs tüskesorára; csak 3,3 V.', 'Kimenetek: LED 2,2 kΩ-mal a GND-re; újraindítás után ellenőrizd a biztonságos szintet.', 'Bemenetek: 10 kΩ felhúzó + 330 Ω soros + kapcsoló a GND-re (zárt = egészséges).', 'A buszok mérőtűkre vannak kivezetve a logikai analizátorhoz.'],
      dict(h=('BCM', 'Láb', 'Jel', 'Irány', 'Tesztelem', 'Biztonságos'), io={'output': 'LED + 2,2 kΩ', 'input': 'Kapcsoló a GND-re', 'bidirectional': 'Mérőtű'}))),
 'T3': dict(
  es=('Fixture mecánico del rotor', 'Medición de holgura, equilibrio, precisión y temperatura',
      ['Atornillar el rotor al tablero rígido en tres puntos.', 'Colocar la carga de 0,5 kg a distancia conocida y medir el CG (≤ 30 mm).', 'Medir holgura invirtiendo el sentido con el indicador de dial.', 'Registrar posición del encoder vs. goniómetro en 10 puntos.', 'Cámara térmica sobre motor y driver durante 30 min.'],
      dict(board='Tablero rígido 18 mm', rotor='Rotor AZ/EL\n(reductor 25:1)', arm='Brazo con carga 0,5 kg', load='0,5 kg', prot='Goniómetro', dial='Indicador de dial', cam='Cámara térmica', scale='Báscula 0,1 g')),
  en=('Rotor mechanical fixture', 'Backlash, balance, accuracy and temperature measurement',
      ['Bolt the rotor to the rigid board at three points.', 'Place the 0.5 kg load at a known distance and measure the CG (≤ 30 mm).', 'Measure backlash by reversing direction with the dial indicator.', 'Record encoder position vs. protractor at 10 points.', 'Thermal camera on motor and driver for 30 min.'],
      dict(board='Rigid 18 mm board', rotor='AZ/EL rotor\n(25:1 gearbox)', arm='Arm with 0.5 kg load', load='0.5 kg', prot='Protractor', dial='Dial indicator', cam='Thermal camera', scale='0.1 g scale')),
  hu=('A forgató mechanikai rögzítője', 'Holtjáték-, egyensúly-, pontosság- és hőmérsékletmérés',
      ['Csavarozd a forgatót a merev lapra három ponton.', 'Helyezd a 0,5 kg-os terhelést ismert távolságra és mérd a súlypontot (≤ 30 mm).', 'Mérd a holtjátékot irányváltással a mérőórával.', 'Jegyezd az enkóderpozíciót a szögmérőhöz képest 10 pontban.', 'Hőkamera a motoron és a meghajtón 30 percig.'],
      dict(board='Merev 18 mm-es lap', rotor='AZ/EL forgató\n(25:1 hajtómű)', arm='Kar 0,5 kg terheléssel', load='0,5 kg', prot='Szögmérő', dial='Mérőóra', cam='Hőkamera', scale='0,1 g-os mérleg'))),
}
def t1(lang):
    title, sub, steps, d = TXT['T1'][lang]
    b = '<rect width="940" height="560" fill="#fff" stroke="#c8d0d8"/>'
    b += box(20, 40, 130, 56, d['psu'], '#e8f1fb') + arrow(150, 68, 180, 68) + box(180, 40, 120, 56, d['fuse']) + arrow(300, 68, 330, 68)
    b += box(330, 40, 130, 56, d['stop'], '#fdecd6', ORANGE, bold=True) + arrow(460, 68, 490, 68) + box(490, 40, 100, 56, d['vmot']) + arrow(590, 68, 620, 68)
    b += box(620, 40, 140, 56, d['drv']) + arrow(760, 68, 790, 68) + box(790, 40, 130, 56, d['mot'], '#e6f4ea')
    b += f'<text x="205" y="193" font-size="12" fill="{GREY}">{d["aux"]}</text>' + poly([(395, 96), (395, 200), (190, 200), (190, 230)], ORANGE, True)
    b += box(20, 230, 190, 70, d['cm5'], '#e8f1fb', NAVY, bold=True) + arrow(115, 230, 115, 96, NAVY, True)
    b += f'<text x="122" y="165" font-size="12" fill="{GREY}">5 V / 3,3 V</text>'
    b += box(250, 330, 180, 56, d['tst'], '#fdecd6', ORANGE) + arrow(115, 300, 250, 358)
    b += box(480, 230, 150, 56, d['mux']) + arrow(210, 255, 480, 255) + box(480, 320, 150, 40, d['exp']) + arrow(210, 280, 480, 340)
    b += box(680, 230, 130, 40, d['lim']) + arrow(630, 250, 680, 250) + box(680, 290, 130, 40, d['gnss']) + arrow(210, 292, 680, 310)
    b += poly([(690, 96), (690, 216), (150, 216), (150, 230)], NAVY, False) + f'<text x="700" y="150" font-size="12" fill="{GREY}">SPI1</text>' + arrow(115, 300, 115, 440) + box(20, 440, 190, 56, d['pc'], '#f4f7fa')
    b += f'<rect x="250" y="440" width="670" height="56" rx="6" fill="#f4f7fa" stroke="{GREY}"/><text x="585" y="474" font-size="13" text-anchor="middle">{d["tp"]}</text>'
    return b, 560
def t2(lang):
    title, sub, steps, d = TXT['T2'][lang]
    g = json.load(open(ROOT/'hardware/cm5/interface.json'))['gpio']
    hd = d['h']; xs = (8, 80, 150, 430, 540, 750)
    rows = [f'<rect width="940" height="{(len(g)+1)*24}" fill="#fff" stroke="#c8d0d8"/>']
    rows.append(f'<rect width="940" height="24" fill="{NAVY}"/>' + ''.join(f'<text x="{x}" y="17" font-size="13" font-weight="bold" fill="#fff">{h}</text>' for x, h in zip(xs, hd)))
    for i, p in enumerate(g):
        y = (i+1)*24; safe = p.get('safeLevel') or (('OK: ' + p['healthy']) if 'healthy' in p else '')
        col = ORANGE if ('LIMIT' in p['signal'] or 'ESTOP' in p['signal'] or 'FAULT' in p['signal']) else NAVY
        el = d['io'].get(p.get('direction', 'input'), '')
        if any(k in p['signal'] for k in ('I2C', 'SPI1', 'GNSS_UART')): el = d['io']['bidirectional']
        rows.append(f'<rect y="{y}" width="940" height="24" fill="{"#f4f7fa" if i%2 else "#fff"}"/>'
          f'<text x="{xs[0]}" y="{y+17}" font-size="12">{p["bcm"]}</text><text x="{xs[1]}" y="{y+17}" font-size="12">{p["headerPin"]}</text>'
          f'<text x="{xs[2]}" y="{y+17}" font-size="12" font-weight="bold" fill="{col}">{p["signal"]}</text>'
          f'<text x="{xs[3]}" y="{y+17}" font-size="12">{p.get("direction","")}</text><text x="{xs[4]}" y="{y+17}" font-size="12">{el}</text>'
          f'<text x="{xs[5]}" y="{y+17}" font-size="12">{safe}</text>')
    return ''.join(rows), (len(g)+1)*24
def t3(lang):
    title, sub, steps, d = TXT['T3'][lang]
    b = '<rect width="940" height="470" fill="#fff" stroke="#c8d0d8"/>'
    b += f'<rect x="60" y="390" width="560" height="26" fill="#c9b08a" stroke="#555"/><text x="480" y="384" font-size="13" text-anchor="middle">{d["board"]}</text>'
    for x in (90, 330, 580): b += f'<rect x="{x}" y="416" width="26" height="22" fill="#777"/>'
    b += box(250, 250, 160, 140, d['rotor'], '#e8f1fb', NAVY, bold=True)
    b += f'<rect x="330" y="215" width="14" height="40" fill="#999"/><rect x="200" y="200" width="330" height="16" fill="#bbb" stroke="#555"/>'
    b += box(470, 120, 90, 56, d['load'], '#fdecd6', ORANGE, bold=True) + arrow(515, 176, 515, 200, ORANGE)
    b += f'<text x="360" y="190" font-size="12" fill="{GREY}">{d["arm"]}</text>'
    b += box(650, 60, 160, 44, d['prot']) + arrow(650, 82, 345, 232, GREY, True)
    b += box(650, 130, 160, 44, d['dial']) + arrow(650, 152, 530, 208, GREY, True)
    b += box(650, 200, 160, 44, d['cam']) + arrow(650, 222, 410, 300, GREY, True)
    b += box(650, 270, 160, 44, d['scale']) + arrow(650, 292, 620, 395, GREY, True)
    return b, 470
for code, fn, name in (('T1', t1, 'T1-banco-pruebas'), ('T2', t2, 'T2-comprobador-gpio'), ('T3', t3, 'T3-fixture-mecanico')):
    for lang in ('es', 'en', 'hu'):
        title, sub, steps = TXT[code][lang][:3]
        body, h = fn(lang)
        svg, w, hh = frame(code, title, sub, body, h, steps, [], lang=lang)
        (FIG/f'{name}{SUF[lang]}.svg').write_text(svg, encoding='utf-8')
print('figs ok')
