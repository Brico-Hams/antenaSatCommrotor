"""Build branded assembly figures into docs/assembly/fig/ (3D renders from OpenSCAD,
Gerber rasters, GPIO wiring from hardware/cm5/interface.json)."""
import sys, json, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import numpy as np
from PIL import Image
from _figkit import frame, img_uri, ROOT, NAVY, ORANGE, GREY
from _render3d import render, OUT
from _figtext import X, LEG, FLOW
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

LANGS = ('es', 'en', 'hu')
SUF = {'es': '', 'en': '.en', 'hu': '.hu'}
NAMES = {'R1': 'R1-rotor-piezas', 'R2': 'R2-reductor-despiece', 'R3': 'R3-azimut', 'R4': 'R4-rotor-completo',
         'R5': 'R5-polarizacion-despiece', 'R6': 'R6-polarizacion-montada', 'A1': 'A1-antena-piezas',
         'A2': 'A2-antena-montada', 'C1': 'C1-cajas', 'I1': 'I1-estacion-completa', 'E1': 'E1-pcb-carrier',
         'E2': 'E2-pcb-cm5-guard', 'E3': 'E3-cableado-gpio', 'I2': 'I2-integracion'}
SCENE = {'R1': 'b_parts', 'R2': 'b_gearbox_x', 'R3': 'b_az', 'R4': 'b_rotor', 'R5': 'pol_x', 'R6': 'pol_asm',
         'A1': 'antenna_parts', 'A2': 'antenna_band', 'C1': 'boxes', 'I1': 'b_station'}
C = {'al': '#c0c0c0', 'cup': '#008080', 'belt': '#222', 'asa': '#e8871e', 'base': '#4a6fa5', 'mast': '#555',
     'elem': '#bbb', 'box': '#2e8b57', 'cradle': '#3a6ea5', 'cu': '#c8963c', 'board': '#165434', 'silk': '#fff'}
LEGEND = {
 'R1': [('al', 'part'), ('cup', 'cup'), ('belt', 'belt'), ('asa', 'asa')], 'R2': [('al', 'part'), ('cup', 'cup'), ('belt', 'belt'), ('asa', 'asa')],
 'R3': [('al', 'part'), ('cup', 'cup'), ('belt', 'belt'), ('asa', 'asa')], 'R4': [('al', 'part'), ('cup', 'cup'), ('belt', 'belt'), ('asa', 'asa'), ('base', 'base')],
 'R5': [('al', 'part'), ('cup', 'cup'), ('belt', 'belt'), ('asa', 'asa')], 'R6': [('al', 'part'), ('cup', 'cup'), ('belt', 'belt'), ('asa', 'asa')],
 'A1': [('asa', 'asa')], 'A2': [('asa', 'asa'), ('mast', 'mast'), ('elem', 'elem')], 'C1': [('box', 'box'), ('cradle', 'cradle')],
 'I1': [('al', 'part'), ('cup', 'cup'), ('belt', 'belt'), ('asa', 'asa'), ('mast', 'mast')],
 'E1': [('cu', 'cu'), ('board', 'board'), ('silk', 'silk')], 'E2': [('cu', 'cu'), ('board', 'board'), ('silk', 'silk')],
 'E3': [('#e8871e', 'safety'), ('#12263f', 'other')], 'I2': [('#e8871e', 'step')]}

def write(code, lang, body, bh):
    title, sub, steps = X[code][lang]
    leg = [(C.get(c, c), LEG[k][lang]) for c, k in LEGEND[code]]
    svg, w, h = frame(code, title, sub, body, bh, steps, leg, lang=lang)
    (FIG/f'{NAMES[code]}{SUF[lang]}.svg').write_text(svg, encoding='utf-8'); print(NAMES[code], lang, h)

def pcb_body(name, gdir):
    ls, b, L = analyse(str(ROOT/gdir))
    h, w = L['copper'].shape
    img = np.full((h, w, 3), 255, np.uint8)
    ys, xs = np.where(L['outline'])
    img[ys.min():ys.max()+1, xs.min():xs.max()+1] = (22, 84, 52)
    img[L['copper']] = (206, 160, 70); img[L['silk']] = (255, 255, 255); img[L['outline']] = (0, 0, 0)
    p = OUT/f'{name}.png'; Image.fromarray(img).save(p)
    uri, (iw, ih) = img_uri(p, 1500); sc = min(940/iw, 700/ih)
    return (f'<rect width="940" height="{ih*sc+16:.0f}" fill="#f8f9fb" stroke="#c8d0d8"/>'
            f'<image x="{(940-iw*sc)/2:.0f}" y="8" width="{iw*sc:.0f}" height="{ih*sc:.0f}" xlink:href="{uri}"/>'), int(ih*sc+16)

sys.path.insert(0, str(ROOT/'scripts'))
from _pcb_free import analyse
BODY = {c: photo(n) for c, n in SCENE.items()}
BODY['E1'] = pcb_body('E1-pcb-carrier', 'fabrication/gerbers')
BODY['E2'] = pcb_body('E2-pcb-cm5-guard', 'hardware/cm5/fabrication/NOT_FOR_MANUFACTURE/gerber')

g = json.load(open(ROOT/'hardware/cm5/interface.json'))['gpio']
rows = []
for i, p in enumerate(g):
    y = i*26; col = ORANGE if 'LIMIT' in p['signal'] or 'ESTOP' in p['signal'] else NAVY
    rows.append(f'<rect x="0" y="{y}" width="940" height="24" fill="{"#f4f7fa" if i%2 else "#fff"}"/>'
        f'<text x="8" y="{y+17}" font-size="13">BCM {p["bcm"]}</text><text x="100" y="{y+17}" font-size="13">pin {p["headerPin"]}</text>'
        f'<text x="190" y="{y+17}" font-size="13" font-weight="bold" fill="{col}">{p["signal"]}</text>'
        f'<text x="470" y="{y+17}" font-size="13">{p.get("direction","")}</text>'
        f'<text x="620" y="{y+17}" font-size="13">{p.get("safeLevel", "healthy: "+p["healthy"] if "healthy" in p else "")}</text>')
BODY['E3'] = (''.join(rows), len(g)*26)

for lang in LANGS:
    b = []
    for i, st in enumerate(FLOW[lang]):
        x, y = (i%2)*470, (i//2)*86
        b.append(f'<rect x="{x}" y="{y}" width="450" height="68" rx="8" fill="#f4f7fa" stroke="{NAVY}"/>'
                 f'<circle cx="32" cy="34" r="20" fill="{ORANGE}"/><text x="32" y="41" font-size="18" font-weight="bold" fill="#fff" text-anchor="middle">{i+1}</text>'
                 f'<text x="64" y="40" font-size="15">{st}</text>')
    BODY['I2'] = (''.join(b), 5*86)
    for code in NAMES: write(code, lang, *BODY[code])
