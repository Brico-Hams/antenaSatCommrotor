#!/usr/bin/env python3
"""3 dB beamwidth of the crossed Yagis from NEC2 (single-point pattern evaluations). Writes calc/beamwidth_result.json"""
import sys, json, os; sys.path.insert(0, os.path.dirname(__file__))
import antenna_nec as A, numpy as np
d = json.load(open(os.path.join(os.path.dirname(__file__), 'antenna_result.json')))
v = [tuple(x) for x in d['vhf']]; u = [tuple(x) for x in d['uhf']]
def gain(f, els, ex, th, ph):
    n = A.build(f, els, ex); n.rp_card(0, 1, 1, 0, 0, 0, 0, float(th), float(ph), 0.0, 0.0, 0.0, 0)
    return float(np.asarray(n.get_radiation_pattern(0).get_gain_tot()).flatten()[0])
def half_angle(f, els, ex, plane):
    g0 = gain(f, els, ex, 90, 0)
    for a in np.arange(2, 90, 2):
        g = gain(f, els, ex, 90, a) if plane == 'XY' else gain(f, els, ex, 90 - a, 0)
        if g < g0 - 3: 
            g_prev = gain(f, els, ex, 90, a-2) if plane == 'XY' else gain(f, els, ex, 90 - (a-2), 0)
            return a - 2 + 2*(g_prev - (g0-3))/(g_prev - g)
    return 90.0
res = {}
for name, f, els, ex in (('VHF', 145.9, v, u), ('UHF', 436.5, u, v)):
    w1 = 2*half_angle(f, els, ex, 'XY'); w2 = 2*half_angle(f, els, ex, 'XZ'); res[name] = dict(plane_XY_deg=round(w1, 1), plane_XZ_deg=round(w2, 1))
    print(name, 'full 3 dB beamwidth: horizontal-plane cut %.0f deg, vertical-plane cut %.0f deg' % (w1, w2))
json.dump(res, open(os.path.join(os.path.dirname(__file__), 'beamwidth_result.json'), 'w'), indent=1)
