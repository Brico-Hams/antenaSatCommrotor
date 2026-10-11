"""Rasterise Gerber layers (gerbonara + cairosvg) and find free silkscreen space."""
import io, warnings, numpy as np, cairosvg
from PIL import Image
from gerbonara import LayerStack
warnings.filterwarnings('ignore')
RES = 10  # px per mm (0.1 mm)

def raster(layer, bounds, res=RES):
    (x0, y0), (x1, y1) = bounds
    tag = layer.to_svg(force_bounds=bounds, fg='#000000', bg='#ffffff', arg_unit='mm') if False else None
    svg = str(layer.to_svg(force_bounds=bounds, fg='black', bg='white'))
    w = int(round((x1 - x0) * res)); h = int(round((y1 - y0) * res))
    png = cairosvg.svg2png(bytestring=svg.encode(), output_width=w, output_height=h, background_color='white')
    return np.array(Image.open(io.BytesIO(png)).convert('L')) < 128

def analyse(gdir, side='top'):
    ls = LayerStack.open(gdir)
    (x0, y0), (x1, y1) = ls.board_bounds() if hasattr(ls, 'board_bounds') else ls.outline.bounding_box()
    pad = 1.0
    bounds = ((x0 - pad, y0 - pad), (x1 + pad, y1 + pad))
    g = ls.graphic_layers
    L = {k: raster(g[(side, k)], bounds) for k in ('copper', 'mask', 'silk')}
    L['outline'] = raster(g[('mechanical', 'outline')], bounds)
    return ls, bounds, L

import cv2

def drills(ls, bounds, res=RES):
    (x0, y0), (x1, y1) = bounds
    h = int(round((y1 - y0) * res)); w = int(round((x1 - x0) * res))
    m = np.zeros((h, w), np.uint8)
    for df in (ls.drill_pth, ls.drill_npth):
        if df is None: continue
        for o in df.objects:
            ap = getattr(o, 'aperture', None) or getattr(o, 'tool', None)
            d = getattr(ap, 'diameter', None)
            if d is None: continue
            P = lambda x, y: (int(round((x - x0) * res)), int(round((y - y0) * res)))
            if hasattr(o, 'x1'):   # routed slot
                cv2.line(m, P(o.x1, o.y1), P(o.x2, o.y2), 1, max(1, int(round(d * res))))
            else:
                cv2.circle(m, P(o.x, o.y), int(round(d / 2 * res)), 1, -1)
    return m > 0

def blocked_map(L, drill, board_margin_mm=1.5, clear_mm=0.6, res=RES):
    k = int(round(clear_mm * res))
    ker = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * k + 1, 2 * k + 1))
    obj = (L['mask'] | L['silk'] | drill).astype(np.uint8)
    bl = cv2.dilate(obj, ker) > 0
    # both boards are plain rectangles (Edge.Cuts = 4 lines): interior from the outline bounding box
    ys, xs = np.where(L['outline'])
    inside = np.zeros_like(bl)
    m = int(board_margin_mm * res)
    inside[ys.min() + m:ys.max() - m, xs.min() + m:xs.max() - m] = True
    return bl | ~inside

def find_rects(bl, w_mm, h_mm, res=RES, top_n=1, prefer=None):
    """Return top-left (px) positions of free w x h rectangles (smallest 'prefer' cost first)."""
    W = int(round(w_mm * res)); H = int(round(h_mm * res))
    ii = cv2.integral(bl.astype(np.uint8)).astype(np.int64)
    hh, ww = bl.shape
    ys = np.arange(0, hh - H, 5); xs = np.arange(0, ww - W, 5)
    Y, X = np.meshgrid(ys, xs, indexing='ij')
    s = ii[Y + H, X + W] - ii[Y, X + W] - ii[Y + H, X] + ii[Y, X]
    ok = np.argwhere(s == 0)
    if len(ok) == 0: return []
    cand = [(int(xs[j]), int(ys[i])) for i, j in ok]
    if prefer: cand.sort(key=lambda p: prefer(p[0] / res, p[1] / res))
    return cand[:top_n]
