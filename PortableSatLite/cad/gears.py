"""Parametric herringbone planetary gear set (sun / planet / ring) -> manifold3d solids.
Involute profile generated from first principles; helical twist via extrude(twist). Units: mm."""
import math
import numpy as np
import manifold3d as m3
from manifold3d import Manifold, CrossSection

def inv(a): return math.tan(a) - a

def gear_profile(z, mod, pa_deg=20.0, add=1.0, ded=1.25, pts=7):
    """External involute gear 2D profile (list of (x,y)). add/ded in module units. One tooth centred on +X axis."""
    pa = math.radians(pa_deg); rp = z*mod/2; rb = rp*math.cos(pa); ra = rp + add*mod; rr = rp - ded*mod
    start = max(rb, rr)
    rs = np.linspace(start, ra, pts)
    def psi(r): return math.pi/(2*z) + inv(pa) - inv(math.acos(min(rb/r, 1.0)))
    out = []
    for k in range(z):
        a0 = 2*math.pi*k/z
        # right flank going out, then tip, then left flank coming back
        if rr < rb:
            out.append((rr*math.cos(a0 - psi(rb)), rr*math.sin(a0 - psi(rb))))
        out += [(r*math.cos(a0 - psi(r)), r*math.sin(a0 - psi(r))) for r in rs]
        out += [(r*math.cos(a0 + psi(r)), r*math.sin(a0 + psi(r))) for r in rs[::-1]]
        if rr < rb:
            out.append((rr*math.cos(a0 + psi(rb)), rr*math.sin(a0 + psi(rb))))
    return out

def herringbone(profile_pts, width, helix_deg, rp, hand=+1, ndiv=10, offset=0.0, holes=()):
    """Extrude profile with +/- twist halves (V shape). width = total face width. offset: 2D offset (mm) for clearance."""
    cs = CrossSection([np.array(profile_pts)], fillrule=m3.FillRule.NonZero if hasattr(m3,'FillRule') else None) if False else CrossSection([np.array(profile_pts)])
    if offset: cs = cs.offset(offset, m3.JoinType.Miter, 2.0, 4) if hasattr(m3, 'JoinType') else cs
    for h in holes: cs = cs - h
    half = width/2
    tw = math.degrees(half*math.tan(math.radians(helix_deg))/rp)   # twist (deg) accumulated over half width at pitch radius
    lo = Manifold.extrude(cs, half, ndiv, hand*tw)
    hi = lo.mirror([0, 0, 1]).translate([0, 0, width])            # mirrored: opposite twist, mirrors back to V-apex at mid-plane
    return (lo + hi)

def circle(r, n=96): return CrossSection.circle(r, n)
def ring_solid(zr, mod, width, helix_deg, outer_r, pa=20.0, clr=0.0, hand=+1, ndiv=10):
    rp = zr*mod/2
    cav = gear_profile(zr, mod, pa, add=1.25, ded=1.0)   # cavity: ring gaps behave like an external gear with swapped add/ded
    cavity = herringbone(cav, width, helix_deg, rp, hand, ndiv, offset=+clr/2)
    body = Manifold.extrude(circle(outer_r), width)
    return body - cavity

def sun_solid(zs, mod, width, helix_deg, bore_d, pa=20.0, clr=0.0, hand=+1, ndiv=10, d_flat=4.5):
    rp = zs*mod/2
    bore = CrossSection.circle(bore_d/2, 48)
    if d_flat: bore = bore - CrossSection.square([bore_d, bore_d]).translate([d_flat - bore_d/2 + bore_d/2 - 0 + (-bore_d/2) + bore_d/2, -bore_d/2]) if False else bore
    g = herringbone(gear_profile(zs, mod, pa), width, helix_deg, rp, hand, ndiv, offset=-clr/2)
    return g - Manifold.extrude(bore, width + 2).translate([0, 0, -1])

def planet_solid(zp, mod, width, helix_deg, bore_d, pa=20.0, clr=0.0, hand=-1, ndiv=10):
    rp = zp*mod/2
    g = herringbone(gear_profile(zp, mod, pa), width, helix_deg, rp, hand, ndiv, offset=-clr/2)
    return g - Manifold.extrude(CrossSection.circle(bore_d/2, 32), width + 2).translate([0, 0, -1])
