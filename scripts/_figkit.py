"""Branded SVG frame for assembly figures (logo, title block, steps, legend, authors)."""
import base64, io, pathlib
from html import escape
from PIL import Image
ROOT = pathlib.Path(__file__).resolve().parents[1]
AUTHORS = 'Anatol EA5KAO · Diego EA5JEF · Pedro Roca Molina'
SITE = 'bricohams.org'
STATUS = {'es': 'Prototipo digital: no validado fisicamente', 'en': 'Digital prototype: not physically validated',
          'hu': 'Digitális prototípus: fizikailag nem validált'}
LBL = {'es': ('Pasos', 'Leyenda', 'ver LICENSES/'), 'en': ('Steps', 'Legend', 'see LICENSES/'), 'hu': ('Lépések', 'Jelmagyarázat', 'lásd LICENSES/')}
NAVY, ORANGE, GREY = '#12263f', '#e8871e', '#5b6b7b'
W = 1600

def b64(img, fmt='PNG', **kw):
    b = io.BytesIO(); img.save(b, fmt, **kw)
    return base64.b64encode(b.getvalue()).decode()

def logo_uri(h=64):
    im = Image.open(ROOT/'branding/bricohams_horizontal.png').convert('RGB')
    im = im.resize((int(im.width*h/im.height), h), Image.LANCZOS)
    return 'data:image/png;base64,'+b64(im), im.width

def img_uri(path, maxw):
    im = Image.open(path).convert('RGB')
    if im.width > maxw: im = im.resize((maxw, int(im.height*maxw/im.width)), Image.LANCZOS)
    return 'data:image/jpeg;base64,'+b64(im, 'JPEG', quality=88, optimize=True), im.size

def _wrap(t, n):
    out, line = [], ''
    for w in t.split():
        if len(line)+len(w)+1 > n: out.append(line); line = w
        else: line = (line+' '+w).strip()
    return out+[line] if line else out

def frame(code, title, subtitle, body_svg, body_h, steps=(), legend=(), body_w=None, lang='es'):
    """body_svg is drawn in a box of (body_w or 900) x body_h at x=40; steps panel on the right."""
    bw = body_w or 940
    lg, lw = logo_uri(64)
    top = 104
    sx, sw = 40+bw+30, W-40-(40+bw+30)
    srows = []
    y = 0
    for i, s in enumerate(steps, 1):
        lines = _wrap(s, 44)
        srows.append((i, lines, y)); y += 26*len(lines)+20
    leg_h = 34 if legend else 0
    H = top+max(body_h, y+60)+leg_h+70+24
    o = [f'<svg lang="{lang}" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="DejaVu Sans, Arial, sans-serif">',
         f'<title>{escape(code)} {escape(title)} - BricoHams</title>',
         f'<desc>{escape(subtitle)}. {AUTHORS}. {SITE}</desc>',
         f'<rect width="{W}" height="{H}" fill="#fff"/><rect x="6" y="6" width="{W-12}" height="{H-12}" fill="none" stroke="{NAVY}" stroke-width="2"/>',
         f'<rect x="6" y="6" width="{W-12}" height="86" fill="#f4f7fa"/><rect x="6" y="90" width="{W-12}" height="4" fill="{ORANGE}"/>',
         f'<image x="24" y="14" width="{lw}" height="64" xlink:href="{lg}"/>',
         f'<text x="{lw+50}" y="44" font-size="26" font-weight="bold" fill="{NAVY}">{escape(title)}</text>',
         f'<text x="{lw+50}" y="72" font-size="15" fill="{GREY}">{escape(subtitle)}</text>',
         f'<rect x="{W-170}" y="22" width="140" height="48" rx="6" fill="{NAVY}"/><text x="{W-100}" y="54" font-size="26" font-weight="bold" fill="#fff" text-anchor="middle">{escape(code)}</text>',
         f'<g transform="translate(40,{top})">{body_svg}</g>']
    if steps:
        o.append(f'<g transform="translate({sx},{top+4})"><text font-size="18" font-weight="bold" fill="{NAVY}" y="16">{LBL[lang][0]}</text>')
        for i, lines, yy in srows:
            yy += 44
            o.append(f'<circle cx="14" cy="{yy-6}" r="14" fill="{ORANGE}"/><text x="14" y="{yy}" font-size="15" font-weight="bold" fill="#fff" text-anchor="middle">{i}</text>')
            for k, l in enumerate(lines):
                o.append(f'<text x="38" y="{yy+k*26-1}" font-size="15" fill="#222">{escape(l)}</text>')
        o.append('</g>')
    ly = top+max(body_h, y+60)+6
    if legend:
        x = 40
        o.append(f'<text x="40" y="{ly+14}" font-size="13" font-weight="bold" fill="{NAVY}">{LBL[lang][1]}:</text>'); x = 200
        for col, txt in legend:
            o.append(f'<rect x="{x}" y="{ly+3}" width="14" height="14" fill="{col}" stroke="#333"/><text x="{x+20}" y="{ly+15}" font-size="13" fill="#222">{escape(txt)}</text>')
            x += 40+len(txt)*7.4
    fy = H-60
    o += [f'<rect x="6" y="{fy-8}" width="{W-12}" height="2" fill="{ORANGE}"/>',
          f'<text x="24" y="{fy+14}" font-size="14" font-weight="bold" fill="{NAVY}">BricoHams · {escape(AUTHORS)} · {SITE}</text>',
          f'<text x="24" y="{fy+34}" font-size="12" fill="{GREY}">{escape(STATUS[lang])} · CERN-OHL-S-2.0 (hardware) / MIT (software) - {LBL[lang][2]}</text>',
          f'<text x="{W-24}" y="{fy+14}" font-size="12" fill="{GREY}" text-anchor="end">{escape(code)} · {escape(title)}</text></svg>']
    return '\n'.join(o), W, H
