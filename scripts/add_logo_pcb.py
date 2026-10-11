#!/usr/bin/env python3
"""Add the BricoHams logo (single colour) to the top silkscreen of both boards.

Patches, for each board: the Gerber legend file (G36/G37 regions, LPD/LPC) and the
.kicad_pcb (gr_poly triangles on F.SilkS) so a future KiCad plot keeps the logo.
The position is the most open free area found by rasterising the Gerber layers
(clear of pads/mask openings, holes, existing silkscreen and the board edge).
Idempotent: refuses to patch a file that already carries the marker.
NOTE: KiCad is NOT available in the build environment; DRC/ERC were not re-run.
"""
import json, sys, re, pathlib, warnings
import numpy as np, cv2, mapbox_earcut as earcut
warnings.filterwarnings('ignore')
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import _pcb_free as P

ROOT = pathlib.Path(__file__).resolve().parents[1]
MARK = 'BRICOHAMS-LOGO'
polys = json.loads((ROOT/'branding/bricohams_polys.json').read_text())

BOARDS = [
    dict(name='carrier', gdir='fabrication/gerbers', silk='PortableSatCarrier-f_silkscreen.gto',
         pcb='hardware/PortableSatCarrier.kicad_pcb', pcbfmt='old'),
    dict(name='cm5-guard-A', gdir='hardware/cm5/fabrication/NOT_FOR_MANUFACTURE/gerber',
         silk='cm5-guard-A-F_Silkscreen.gto', pcb='hardware/cm5/cm5-guard-A.kicad_pcb', pcbfmt='new'),
]

def rd(p):  # keep original line endings (files are CRLF on Windows checkouts)
    return open(p, encoding='utf-8', newline='').read()

def wr(p, t):
    open(p, 'w', encoding='utf-8', newline='').write(t)

def choose(name):
    ls, b, L = P.analyse(str(ROOT/[x for x in BOARDS if x['name']==name][0]['gdir']))
    dr = P.drills(ls, b); bl = P.blocked_map(L, dr)
    free = cv2.distanceTransform((~bl).astype(np.uint8), cv2.DIST_L2, 5)
    for variant, widths in (('lockup', (50, 40, 32, 26)), ('mark', (16, 12, 10))):
        asp = (polys[variant]['bbox'][3]-polys[variant]['bbox'][1]) / (polys[variant]['bbox'][2]-polys[variant]['bbox'][0])
        for w in widths:
            c = P.find_rects(bl, w, w*asp, top_n=100000)
            if not c: continue
            H = int(round(w*asp*P.RES)); W = int(round(w*P.RES))
            best = max(c, key=lambda p: free[p[1]+H//2, p[0]+W//2])
            (bx0, by0), (bx1, by1) = b
            gx = bx0 + best[0]/P.RES; gy_top = by1 - best[1]/P.RES   # raster row 0 = top (max Y)
            return dict(variant=variant, w=w, h=w*asp, gx=gx, gy=gy_top-w*asp,
                        clearance=float(free[best[1]+H//2, best[0]+W//2]/P.RES), bounds=b, L=L, bl=bl)
    raise SystemExit(f'{name}: no free area for the logo')

def to_mm(variant, w, gx, gy):
    """contours -> list of (depth, [(X,Y) mm in Gerber coords, Y up])"""
    x0, y0, x1, y1 = polys[variant]['bbox']; s = w/(x1-x0)
    out = []
    for c in polys[variant]['contours']:
        out.append((c['depth'], [(gx+(x-x0)*s, gy+(y1-y)*s) for x, y in c['pts']]))
    return out

def gerber_regions(cont):
    f = lambda v: int(round(v*1e6))
    lines = [f'G04 {MARK} begin*']
    for dpt in range(0, 8):
        group = [p for d, p in cont if d == dpt]
        if not group: continue
        lines.append('%LPD*%' if dpt % 2 == 0 else '%LPC*%')
        for p in group:
            lines.append('G36*')
            lines.append(f'X{f(p[0][0])}Y{f(p[0][1])}D02*'); lines.append('G01*')
            for x, y in p[1:] + [p[0]]:
                lines.append(f'X{f(x)}Y{f(y)}D01*')
            lines.append('G37*')
    lines += ['%LPD*%', f'G04 {MARK} end*']
    return lines

def triangles(cont):
    """Group depth-even outer + depth-odd holes it contains, earcut -> triangles (Gerber mm)."""
    outers = [(i, p) for i, (d, p) in enumerate(cont) if d % 2 == 0]
    holes = [(i, p) for i, (d, p) in enumerate(cont) if d % 2 == 1]
    def inside(pt, poly):
        return cv2.pointPolygonTest(np.array(poly, np.float32), (float(pt[0]), float(pt[1])), False) >= 0
    tris = []
    for i, outer in outers:
        hs = [h for j, h in holes if inside(h[0], outer)
              and not any(inside(h[0], o2) and cv2.contourArea(np.array(o2, np.float32)) < cv2.contourArea(np.array(outer, np.float32)) for k, o2 in outers if k != i and inside(o2[0], outer))]
        rings = [outer] + hs
        verts = np.array([pt for r in rings for pt in r], np.float64).reshape(-1, 2)
        ends = np.cumsum([len(r) for r in rings]).astype(np.uint32)
        idx = earcut.triangulate_float64(verts, ends).reshape(-1, 3)
        for a, b_, c in idx: tris.append((verts[a], verts[b_], verts[c]))
    return tris

def patch_pcb(path, tris, fmt):
    s = rd(path)
    out = []
    for t in tris:
        pts = ' '.join(f'(xy {x:.4f} {-y:.4f})' for x, y in t)   # PCB y = -Gerber Y
        if fmt == 'old':
            out.append(f'  (gr_poly (pts {pts}) (stroke (width 0) (type solid)) (fill solid) (layer "F.SilkS"))')
        else:
            out.append(f'\t(gr_poly\n\t\t(pts {pts})\n\t\t(stroke\n\t\t\t(width 0)\n\t\t\t(type solid)\n\t\t)\n\t\t(fill yes)\n\t\t(layer "F.SilkS")\n\t\t(uuid "{__import__("uuid").uuid5(__import__("uuid").NAMESPACE_URL, MARK+pts)}")\n\t)')
    block = ''
    i = s.rstrip().rfind(')')
    nl = '\r\n' if '\r\n' in s else '\n'
    wr(path, s[:i] + (block + '\n'.join(out) + '\n').replace('\n', nl) + s[i:])

def main(apply=True):
    if apply and (ROOT/'branding/pcb_logo_placement.json').exists():
        raise SystemExit('already applied (branding/pcb_logo_placement.json exists); git checkout the boards first to redo')
    res = {}
    for B in BOARDS:
        c = choose(B['name'])
        cont = to_mm(c['variant'], c['w'], c['gx'], c['gy'])
        res[B['name']] = {k: c[k] for k in ('variant', 'w', 'h', 'gx', 'gy', 'clearance')}
        print(B['name'], res[B['name']])
        if not apply: continue
        g = ROOT/B['gdir']/B['silk']; txt = rd(g)
        assert MARK not in txt, f'{g} already patched'
        end = txt.rstrip().rfind('M02*')
        nl = '\r\n' if '\r\n' in txt else '\n'
        wr(g, txt[:end] + nl.join(gerber_regions(cont)) + nl + txt[end:])
        patch_pcb(ROOT/B['pcb'], triangles(cont), B['pcbfmt'])
    (ROOT/'branding/pcb_logo_placement.json').write_text(json.dumps(res, indent=1))
    return res

if __name__ == '__main__':
    main(apply='--dry-run' not in sys.argv)
