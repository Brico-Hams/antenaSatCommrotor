"""Add BricoHams logo header-strip + authors footer to the legacy diagrams (idempotent)."""
import re, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from _figkit import logo_uri, AUTHORS, SITE, NAVY, ORANGE, GREY, ROOT
MARK = '<!-- bricohams-brand -->'
FILES = ['docs/diagrams/*.svg', 'docs/system-overview.svg', 'docs/hu/diagrams/system-overview.svg']
for pat in FILES:
    for f in sorted(ROOT.glob(pat)):
        s = f.read_text(encoding='utf-8')
        if MARK in s: continue
        m = re.search(r'viewBox="([\d.\s-]+)"', s)
        x0, y0, w, h = map(float, m.group(1).split())
        uri, lw = logo_uri(40)
        top, bot = 56, 40
        s = s.replace(m.group(0), f'viewBox="{x0:g} {y0:g} {w:g} {h+top+bot:g}"', 1)
        s = re.sub(r'(<svg[^>]*?)\sheight="[\d.]+"', lambda k: k.group(1)+f' height="{h+top+bot:g}"', s, 1)
        if 'xmlns:xlink' not in s.split('>')[0]:
            s = s.replace('<svg', '<svg xmlns:xlink="http://www.w3.org/1999/xlink"', 1)
        head = f'{MARK}<rect x="{x0}" y="{y0}" width="{w}" height="{top}" fill="#f4f7fa"/><rect x="{x0}" y="{y0+top-3}" width="{w}" height="3" fill="{ORANGE}"/><image x="{x0+12}" y="{y0+8}" width="{lw}" height="40" xlink:href="{uri}"/>'
        foot = (f'<rect x="{x0}" y="{y0+top+h}" width="{w}" height="{bot}" fill="#f4f7fa"/><rect x="{x0}" y="{y0+top+h}" width="{w}" height="2" fill="{ORANGE}"/>'
                f'<text x="{x0+12}" y="{y0+top+h+25}" font-size="14" font-family="DejaVu Sans, Arial, sans-serif" font-weight="bold" fill="{NAVY}">BricoHams · {AUTHORS} · {SITE}</text>')
        s = re.sub(r'(<svg[^>]*>)', lambda k: k.group(1)+head+f'<g transform="translate(0,{top})">', s, 1)
        s = s[:s.rfind('</svg>')]+'</g>'+foot+'</svg>'
        f.write_text(s, encoding='utf-8'); print('branded', f.relative_to(ROOT))
