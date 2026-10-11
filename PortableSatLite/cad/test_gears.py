import sys, math, itertools; sys.path.insert(0, 'cad')
from gears import *
import numpy as np
Z_S, Z_P, Z_R, MOD, W, BETA, CLR = 12, 18, 48, 1.5, 16.0, 25.0, 0.30
a = (Z_S + Z_P)*MOD/2
print('center distance', a, 'ratio', 1 + Z_R/Z_S, 'assembly (Zs+Zr)/3 =', (Z_S+Z_R)/3, 'Zr = Zs+2Zp:', Z_R == Z_S + 2*Z_P)
sun = sun_solid(Z_S, MOD, W, BETA, 5.0, clr=CLR); planet = planet_solid(Z_P, MOD, W, BETA, 4.0, clr=CLR); ring = ring_solid(Z_R, MOD, W, BETA, 43.0, clr=CLR)
print('volumes mm3 sun/planet/ring', round(sun.volume()), round(planet.volume()), round(ring.volume()))
def rot(m, deg, c=(0,0)): return m.translate([-c[0], -c[1], 0]).rotate([0, 0, deg]).translate([c[0], c[1], 0])
best = None
for k in range(0, 40):
    rho = k*(360/Z_P)/40
    p = rot(planet, rho).translate([a, 0, 0])
    v = (sun ^ p).volume()
    if best is None or v < best[0]: best = (v, rho)
print('sun-planet min interference volume (mm3) and planet phase:', best)
pl = rot(planet, best[1]).translate([a, 0, 0])
bestr = None
for k in range(0, 48):
    rr = k*(360/Z_R)/48
    v = (rot(ring, rr) ^ pl).volume()
    if bestr is None or v < bestr[0]: bestr = (v, rr)
print('ring-planet min interference volume (mm3) and ring phase:', bestr)
