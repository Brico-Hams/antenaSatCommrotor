"""Render OpenSCAD scenes headlessly (xvfb) and auto-crop to content."""
import subprocess, pathlib, numpy as np
from PIL import Image
ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT = pathlib.Path('/tmp/rend')

def render(name, scad, scene, rot=(60, 0, 30), center=(0, 0, 0), dist=1200, size=(1800, 1300), defs=()):
    OUT.mkdir(exist_ok=True)
    png = OUT / f'{name}.png'
    cam = ','.join(str(v) for v in (*center, *rot, dist))
    cmd = ['xvfb-run', '-a', 'openscad', '-o', str(png), f'--imgsize={size[0]},{size[1]}', f'--camera={cam}',
           '--projection=p', '--colorscheme=Tomorrow', '-D', f'scene="{scene}"', *defs, scad]
    r = subprocess.run(cmd, cwd=ROOT/'cad', capture_output=True, text=True)
    if r.returncode or 'ERROR' in r.stderr:
        raise SystemExit(f'{name}: {r.stderr[-400:]}')
    im = Image.open(png).convert('RGB'); a = np.array(im).astype(int)
    bg = a[2, 2]
    diff = np.abs(a - bg).sum(axis=2) > 24
    ys, xs = np.where(diff)
    pad = 24
    box = (max(xs.min()-pad, 0), max(ys.min()-pad, 0), min(xs.max()+pad, a.shape[1]), min(ys.max()+pad, a.shape[0]))
    im.crop(box).save(png)
    return png, Image.open(png).size
