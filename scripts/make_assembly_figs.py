"""Build branded assembly figures into docs/assembly/fig/ (3D renders from OpenSCAD,
Gerber rasters, GPIO wiring from hardware/cm5/interface.json)."""
import sys, json, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import numpy as np
from PIL import Image
from _figkit import frame, img_uri, ROOT, NAVY, ORANGE, GREY
from _render3d import render, OUT
FIG = ROOT/'docs/assembly/fig'; FIG.mkdir(parents=True, exist_ok=True)

CAM = {  # name: (scad, scene, rot, center, dist)
 'b_parts': ('figures_belt.scad','b_parts',(60,0,30),(0,0,0),1500),
 'b_gearbox_x': ('figures_belt.scad','b_gearbox_x',(60,0,30),(0,0,0),1500),
 'b_az': ('figures_belt.scad','b_az',(60,0,30),(0,0,0),1500),
 'b_rotor': ('figures_belt.scad','b_rotor',(70,0,35),(-60,-20,110),1100),
 'b_station': ('figures_belt.scad','b_station',(70,0,35),(-60,-20,110),3200),
 'pol_x': ('figures_pol.scad','pol_x',(60,0,30),(0,0,0),1500),
 'pol_asm': ('figures_pol.scad','pol_asm',(60,0,30),(0,0,0),1500),
 'antenna_parts': ('figures.scad','antenna_parts',(60,0,30),(0,0,0),900),
 'antenna_band': ('figures.scad','antenna_band',(60,0,30),(0,0,0),2600),
 'boxes': ('figures.scad','boxes',(60,0,30),(0,0,0),900),
}
def need(n):
    if not (OUT/f'{n}.png').exists():
        s, sc, rot, c, d = CAM[n]; render(n, s, sc, rot, c, d)
    return OUT/f'{n}.png'

def photo(n, label_w=940, max_h=720):
    p = need(n); uri, (w, h) = img_uri(p, 1600)
    s = min(label_w/w, max_h/h); w2, h2 = w*s, h*s
    x = (label_w-w2)/2
    svg = (f'<rect width="{label_w}" height="{h2+16:.0f}" fill="#f8f9fb" stroke="#c8d0d8"/>'
           f'<image x="{x:.0f}" y="8" width="{w2:.0f}" height="{h2:.0f}" xlink:href="{uri}"/>')
    return svg, int(h2+16)

def write(code, name, title, sub, body, bh, steps, legend=()):
    svg, w, h = frame(code, title, sub, body, bh, steps, legend)
    (FIG/f'{name}.svg').write_text(svg, encoding='utf-8'); print(name, h)

PART = [('#c0c0c0','Placa Al 3 mm'),('#008080','Copa de rodamiento (ASA)'),('#222','Correa GT2'),('#e8871e','Pieza ASA impresa')]
def fig3d(code, name, scene, title, sub, steps, legend=PART):
    b, h = photo(scene); write(code, name, title, sub, b, h, steps, legend)

fig3d('R1','R1-rotor-piezas','b_parts','Rotor BASE: piezas del reductor','Reduccion por correa GT2 25:1 (20T:100T x2)',
 ['Comprobar: 2 placas Al 3 mm (DXF), 8 separadores Al Ø8, 2 correas GT2 252 mm.',
  'Poleas compradas: 2 x 20T y 2 x 100T; ejes acero Ø8x60 y Ø10x89.',
  'Rodamientos 608 y 6000 con sus copas ASA y retenedores.',
  'Motor NEMA14 provisional (cara 35 mm, agujeros a 26 mm).',
  'Imprimir copas y retenedores en ASA; no imprimir poleas ni correas.'])
fig3d('R2','R2-reductor-despiece','b_gearbox_x','Rotor BASE: despiece del reductor','Orden de montaje de las dos etapas',
 ['Atornillar copas de rodamiento a la placa trasera (lado interior).',
  'Insertar rodamientos 608 (eje Ø8) y 6000 (eje Ø10) en las copas.',
  'Montar polea 20T en el eje del motor y polea 100T en el eje intermedio.',
  'Colocar la primera correa; dejar 1 mm de holgura entre etapas.',
  'Montar polea 20T intermedia y 100T de salida; segunda correa.',
  'Cerrar con la placa frontal y los separadores; tensar con las ranuras ±1.5 mm.'])
fig3d('R3','R3-azimut','b_az','Rotor BASE: eje de azimut','Reductor, brida de salida e iman del encoder',
 ['Fijar la base ligera al tripode con los 4 tornillos.',
  'Montar bandeja metalica y separadores sobre la base.',
  'Colocar el reductor sobre los separadores; alinear eje de salida con el eje AZ.',
  'Montar brida de salida y portaiman; sensor sobre el soporte del encoder.'])
fig3d('R4','R4-rotor-completo','b_rotor','Rotor BASE completo (AZ + EL)','Reductor AZ, soporte EL y segundo reductor en elevacion',
 ['Montar soporte metalico EL sobre la brida AZ.',
  'Fijar segundo reductor con el eje EL horizontal.',
  'Instalar silla de antena en el eje de salida EL.',
  'Comprobar giro libre a mano y topes antes de energizar.'],
 PART+[('#4a6fa5','Base ligera')])
fig3d('R5','R5-polarizacion-despiece','pol_x','Eje POL: despiece','Etapa GT2 5:1, eje hueco, 2 rodamientos 608',
 ['Insertar los 2 rodamientos 608 en el soporte.','Pasar el eje hueco y fijar la polea de salida.',
  'Montar motor y polea pequena; colocar y tensar la correa.','Instalar topes de ±90°.'])
fig3d('R6','R6-polarizacion-montada','pol_asm','Eje POL montado','Conjunto de polarizacion sobre la silla',
 ['Verificar giro libre ±90° sin tocar cables.','Unir al brazo de antena con la abrazadera.',
  'Dejar lazo de cable para el recorrido completo.'])
fig3d('A1','A1-antena-piezas','antenna_parts','Antena: piezas impresas','Nucleo, brazos y bloques de fijacion',
 ['Imprimir en ASA las piezas del nucleo y bloques.','Retirar soportes y comprobar orificios.',
  'Presentar en seco antes de pegar o atornillar.'],[('#e8871e','Pieza ASA impresa')])
fig3d('A2','A2-antena-montada','antenna_band','Antena V/U montada','Mastil con elementos radiales',
 ['Fijar el nucleo al mastil.','Montar los elementos con la longitud de la tabla de diseno.',
  'Medir ROE en cada banda antes de conectar al sistema.'],[('#e8871e','Pieza ASA'),('#555','Mastil'),('#bbb','Elementos')])
fig3d('C1','C1-cajas','boxes','Cajas electronicas y soporte de radio','Tapas con logo BricoHams en relieve',
 ['Imprimir cajas en ASA (logo en la cara exterior de la tapa).','Insertar insertos roscados.',
  'Montar PCB sobre separadores y cerrar con la tapa.'],[('#2e8b57','Caja'),('#3a6ea5','Soporte radio')])
fig3d('I1','I1-estacion-completa','b_station','Estacion completa','Rotor + antena montados',
 ['Rotor sobre el tripode.','Antena sobre la silla EL.','Electronica fija en la base, no gira.'],
 PART+[('#555','Mastil')])

# --- PCB renders from Gerbers
sys.path.insert(0, str(ROOT/'scripts'))
from _pcb_free import analyse
def pcb(code, name, gdir, title, sub, steps=None):
    ls, b, L = analyse(str(ROOT/gdir))
    h, w = L['copper'].shape
    img = np.full((h, w, 3), 255, np.uint8)
    ys, xs = np.where(L['outline'])
    img[ys.min():ys.max()+1, xs.min():xs.max()+1] = (22, 84, 52)
    img[L['copper']] = (206, 160, 70)
    img[L['silk']] = (255, 255, 255); img[L['outline']] = (0, 0, 0)
    im = Image.fromarray(img); p = OUT/f'{name}.png'; im.save(p)
    uri, (iw, ih) = img_uri(p, 1500); s = min(940/iw, 700/ih)
    body = (f'<rect width="940" height="{ih*s+16:.0f}" fill="#f8f9fb" stroke="#c8d0d8"/>'
            f'<image x="{(940-iw*s)/2:.0f}" y="8" width="{iw*s:.0f}" height="{ih*s:.0f}" xlink:href="{uri}"/>')
    write(code, name, title, sub, body, int(ih*s+16), steps or
          ['Revisar el logo y la serigrafia sobre la placa.','Soldar primero SMD, luego conectores y pasantes.',
           'Medir continuidad y cortos antes de energizar.','Primer arranque con fuente limitada en corriente.'],
          [('#c8963c','Cobre'),('#165434','Placa / mascara'),('#fff','Serigrafia (logo BricoHams)')])
pcb('E1','E1-pcb-carrier','fabrication/gerbers','PCB portadora PortableSat','Capa superior (Gerber)')
pcb('E2','E2-pcb-cm5-guard','hardware/cm5/fabrication/NOT_FOR_MANUFACTURE/gerber','PCB cm5-guard-A','Capa superior (Gerber, NO fabricar: prototipo)',
    ['Solo revision: placa en estado de diseno, no apta para fabricacion.','Comprobar el logo y la serigrafia en KiCad.','Ejecutar DRC/ERC en KiCad antes de cualquier pedido (pendiente).'])

# --- wiring from interface.json
g = json.load(open(ROOT/'hardware/cm5/interface.json'))['gpio']
rows = []
for i, p in enumerate(g):
    y = i*26; col = ORANGE if 'LIMIT' in p['signal'] or 'ESTOP' in p['signal'] else NAVY
    rows.append(f'<rect x="0" y="{y}" width="940" height="24" fill="{"#f4f7fa" if i%2 else "#fff"}"/>'
        f'<text x="8" y="{y+17}" font-size="13">BCM {p["bcm"]}</text><text x="100" y="{y+17}" font-size="13">pin {p["headerPin"]}</text>'
        f'<text x="190" y="{y+17}" font-size="13" font-weight="bold" fill="{col}">{p["signal"]}</text>'
        f'<text x="470" y="{y+17}" font-size="13">{p.get("direction","")}</text>'
        f'<text x="620" y="{y+17}" font-size="13">{p.get("safeLevel", "sano: "+p["healthy"] if "healthy" in p else "")}</text>')
hh = len(g)*26
write('E3','E3-cableado-gpio','Cableado GPIO CM5','Contrato de senales (hardware/cm5/interface.json)',
  ''.join(rows), hh,
  ['Cablear segun la tabla; no inventar pines.','Finales de carrera y paro NC: nivel sano = bajo.',
   'MOTOR_ARM_REQUEST arranca en bajo (seguro).','Pasos solo desde el controlador dedicado, nunca GPIO Linux.'],
  [(ORANGE,'Seguridad / finales'),(NAVY,'Otras senales')])

# --- integration flow
steps = ['Aceptar por separado antena, rotor y radio','Montar tripode y base fija','Acoplar antena al rotor',
 'RF SMA por banda, TX inhibido','Distribucion Powerpole/fusibles','Perfil integrated + identidades SDR',
 'Calibrar UTC, norte y ceros AZ/EL/POL','Validar pases, Doppler, audio, SSTV/APRS (sin TX)','Cualificar TX/full-duplex con carga e instrumentos','Pesar conjunto (<=5 kg) y ensayar autonomia 2 h']
b = []
for i, s in enumerate(steps):
    x, y = (i%2)*470, (i//2)*86
    b.append(f'<rect x="{x}" y="{y}" width="450" height="68" rx="8" fill="#f4f7fa" stroke="{NAVY}"/>'
             f'<circle cx="32" cy="34" r="20" fill="{ORANGE}"/><text x="32" y="41" font-size="18" font-weight="bold" fill="#fff" text-anchor="middle">{i+1}</text>'
             f'<text x="64" y="40" font-size="15">{s}</text>')
write('I2','I2-integracion','Integracion colectiva','Secuencia de MODULE-INTEGRATED.md',
  ''.join(b), 5*86, ['Cada modulo se acepta solo antes de unir.','No sumar dos CM5 ni dos sistemas de energia.',
  'No puentear interbloqueos al quitar un modulo.'], [(ORANGE,'Paso')])
