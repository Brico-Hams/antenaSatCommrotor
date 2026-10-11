#!/usr/bin/env python3
"""Crossed-Yagi V/U model in NEC2 (PyNEC), free space, non-conductive boom (not modelled).
Boom along +X (forward). Horizontal elements along Y, vertical along Z (offset 10 mm in X so wires do not intersect).
Ideal 90-degree hybrid is modelled as two voltage sources in quadrature.
Reported: realised gain (dBi, total), axial ratio (dB), F/B (dB), driven-element R+jX per port (with the other port driven)."""
import math, sys, json
import PyNEC
import numpy as np
def F0(x): return float(np.asarray(x).flatten()[0])
def Z0(x):
    a=np.asarray(x).flatten(); return complex(a[0])
C = 299.792458
SEGS = 21
ROD_R = 0.0015      # 3 mm aluminium welding rod
XOFF = 0.010        # vertical plane offset along boom (m) -> 10 mm, modelled 

def build(f, elements, extra=(), cross=True, phase=-90.0):
    nec = PyNEC.nec_context(); g = nec.get_geometry(); tag = 0; drv = {}
    for k, (grp, off) in enumerate([(elements, 0.0), (extra, 0.0)]):
        for i, (x, L) in enumerate(grp):
            planes = [('y', 0.0)] + ([('z', XOFF)] if cross else [])
            for ax, dx in planes:
                tag += 1; h = L / 2
                a = (x+dx, -h, 0) if ax == 'y' else (x+dx, 0, -h)
                b = (x+dx, h, 0) if ax == 'y' else (x+dx, 0, h)
                g.wire(tag, SEGS, *a, *b, ROD_R, 1, 1)
                if k == 0 and i == 1: drv[ax] = tag
    nec.geometry_complete(0); nec.ld_card(5, 0, 0, 0, 3.77e7, 0, 0); nec.fr_card(0, 1, f, 0)
    nec.ex_card(0, drv['y'], (SEGS+1)//2, 0, 1.0, 0.0, 0, 0, 0, 0)
    if cross:
        p = math.radians(phase)
        nec.ex_card(0, drv['z'], (SEGS+1)//2, 0, math.cos(p), math.sin(p), 0, 0, 0, 0)
    return nec

def metrics(f, elements, extra=(), cross=True):
    n = build(f, elements, extra, cross)
    n.rp_card(0, 1, 2, 0, 0, 0, 0, 90, 0, 0, 180, 0, 0)   # phi = 0 (forward) and 180 (back)
    r = n.get_radiation_pattern(0)
    gt = np.asarray(r.get_gain_tot()).flatten(); ar = np.asarray(r.get_pol_axial_ratio()).flatten()
    z = np.asarray(build(f, elements, extra, cross).get_input_parameters(0).get_impedance()).flatten() if False else None
    n2 = build(f, elements, extra, cross); n2.rp_card(0, 1, 1, 0, 0, 0, 0, 90, 0, 0, 0, 0, 0)
    z = np.asarray(n2.get_input_parameters(0).get_impedance()).flatten()
    arv = float(ar[0]); ar_db = -20*math.log10(arv) if arv <= 1 else 20*math.log10(arv)
    return dict(gain_dbi=float(gt[0]), ar_db=ar_db, fb_db=float(gt[0]-gt[1]),
                sense=int(F0(r.get_pol_sense_index())), z_feed=[(round(complex(c).real, 1), round(complex(c).imag, 1)) for c in z])

def set_driven_resonance(f, els, cross=True, extra=()):
    """Tune driven length (index 1) by bisection on X of the driven feed (port 1)."""
    lo, hi = els[1][1]*0.90, els[1][1]*1.10
    for _ in range(18):
        mid = (lo+hi)/2; e = list(els); e[1] = (e[1][0], mid)
        n = build(f, e, extra, cross); n.rp_card(0,1,1,0,0,0,0,90,0,0,0,0,0)
        z = n.get_input_parameters(0).get_impedance()
        z = Z0(z)
        if z.imag > 0: hi = mid
        else: lo = mid
    e = list(els); e[1] = (e[1][0], (lo+hi)/2); return e

IN = 0.0254
# Start dimensions: KX4Z / WA5VJB 144 MHz 3-el (positions & lengths in inches, 3/16" rods) scaled to design f.
def vhf_start(f):
    s = 144.1/f
    return [(0, 41.8*IN*s), (8.5*IN*s, 38.3*IN*s), (19.25*IN*s, 37.3*IN*s)]
def uhf_start(f):
    s = 432.1/f
    return [(0, 13.3*IN*s), (2.5*IN*s, 12.8*IN*s), (5.5*IN*s, 12.3*IN*s), (11.25*IN*s, 11.8*IN*s)]

def report(title, f, els, extra=()):
    m = metrics(f, els, extra)
    print(f"{title:44s} f={f:7.2f} gain={m['gain_dbi']:5.2f} dBi  AR={m['ar_db']:5.2f} dB  F/B={m['fb_db']:5.1f} dB  Zfeed={m['z_feed']}")
    return m

if __name__ == '__main__':
    F_V, F_U = 145.9, 436.5
    res = {}
    v0 = vhf_start(F_V); u0 = uhf_start(F_U)
    print("== Start dimensions (scaled from KX4Z tables) ==")
    report('VHF 3el cross (start)', F_V, v0); report('UHF 4el cross (start)', F_U, u0)
    v1 = set_driven_resonance(F_V, v0); u1 = set_driven_resonance(F_U, u0)
    print("== Driven element tuned to X=0 ==")
    mv = report('VHF 3el cross (tuned)', F_V, v1); mu = report('UHF 4el cross (tuned)', F_U, u1)
    # Combined on one boom: UHF section in front of VHF section (offset), both bands present
    gap = 0.06
    xoff = v1[-1][0] + gap
    u_shift = [(x+xoff, L) for x, L in u1]
    print("== Both sections on the same boom (mutual coupling included) ==")
    # VHF with UHF elements present (as passive, crossed) and UHF with VHF elements present
    def with_extra(f, els, extra):
        n = None
        m = metrics(f, els, extra); print(f"  f={f:7.2f} gain={m['gain_dbi']:5.2f} AR={m['ar_db']:5.2f} F/B={m['fb_db']:5.1f} Z={m['z_feed']}"); return m
    cv = with_extra(F_V, v1, u_shift)
    # for UHF case: make UHF the 'driven group' and VHF passive 'extra'; driven index 1 is within the first group
    cu = with_extra(F_U, u_shift, v1)
    json.dump(dict(vhf=[(round(x,4), round(L,4)) for x,L in v1], uhf=[(round(x,4), round(L,4)) for x,L in u_shift],
                   vhf_alone=mv, uhf_alone=mu, vhf_combined=cv, uhf_combined=cu, boom_len_m=u_shift[-1][0]), open('calc/antenna_result.json','w'), indent=1)

    # band sweep with both sections on the boom
    sweep = {}
    for f, els, ex in [(144.0, v1, u_shift), (145.9, v1, u_shift), (146.0, v1, u_shift), (435.0, u_shift, v1), (436.5, u_shift, v1), (438.0, u_shift, v1)]:
        m = metrics(f, els, ex); sweep[f] = m
        r_, x_ = m['z_feed'][0]; zt = 37.5; zin = complex(zt**2) / complex(r_, x_)   # 2x75 ohm lambda/4 in parallel (37.5 ohm)
        g = abs((zin-50)/(zin+50)); sweep[f]['swr_with_37.5ohm_qwt'] = round((1+g)/(1-g), 2)
        print(f"  sweep f={f:6.1f} gain={m['gain_dbi']:5.2f} AR={m['ar_db']:4.2f} F/B={m['fb_db']:5.1f} SWR(qwt 37.5R)={sweep[f]['swr_with_37.5ohm_qwt']}")
    d = json.load(open('calc/antenna_result.json')); d['sweep'] = {str(k): v for k, v in sweep.items()}
    json.dump(d, open('calc/antenna_result.json', 'w'), indent=1)
