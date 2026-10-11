#!/usr/bin/env python3
"""Feed-network maths for ONE band of the crossed Yagi. Pure transmission-line maths (ABCD), numpy.
OPTION A (adopted): 90-degree hybrid coupler -> 2 outputs -> lambda/4 transformer (Zt = 37.5 ohm = 2x75 ohm coax in parallel) -> each Yagi.
   An ideal hybrid with IDENTICAL loads on both outputs presents a perfect match at its input: the reflected power goes to the isolated (dummy-load) port.
   What is lost is |Gamma|^2 of the transformer+Yagi (printed below). Quadrature phase/amplitude are set by the hybrid, not by cable lengths.
OPTION B (REJECTED, evidence printed below): lambda/4 delay line in one leg + T-junction (no hybrid).
Chain: 50-ohm port -> lambda/4 transformer (Zt 37.5 = 2x75 ohm in parallel) -> T splitting into 2 equal 50-ohm legs
       (leg Z gets an extra lambda/4 of 50-ohm coax = 90 deg) -> each leg through its own lambda/4 transformer (37.5) -> Yagi (R from NEC).
Reports return loss over the band, the quadrature error between the two Yagi feed currents, and cable lengths (velocity factor VF)."""
import numpy as np, json, math
C = 299.792458
VF50, VF75 = 0.66, 0.66      # RG-58 / RG-59 solid PE (datasheet values; VERIFY on the cable you buy -- measure with the NanoVNA)
def tl(Z0, f, L, vf):
    bl = 2*math.pi*f/(C*vf)*L; return np.array([[math.cos(bl), 1j*Z0*math.sin(bl)], [1j*Z0*math.sin(bl)/Z0**2, math.cos(bl)]])
def zin(abcd, ZL):
    A, B, Cc, D = abcd[0,0], abcd[0,1], abcd[1,0], abcd[1,1]; return (A*ZL + B)/(Cc*ZL + D)
def design(f0, yagi_R):
    L4 = C/f0/4
    return dict(lam4_free_m=L4, lam4_50_m=L4*VF50, lam4_75_m=L4*VF75)
def network(f, f0, yagi_Z, d):
    """returns (zin at port, I_ratio of the two yagi feeds)"""
    L50 = d['lam4_50_m']; L75 = d['lam4_75_m']; Zt = 37.5
    def leg(extra):
        # yagi -> qwt(37.5) -> 50 ohm coax of length (extra*L50) ; return input impedance seen at the T and the transfer
        A = tl(Zt, f, L75, 1.0) if False else tl(Zt, f, L75, VF75)
        if extra: A = A @ tl(50.0, f, L50, VF50)
        return A
    legY = leg(False); legZ = leg(True)
    ZY = zin(legY, yagi_Z); ZZ = zin(legZ, yagi_Z)
    Zt_junction = 1/(1/ZY + 1/ZZ)
    top = tl(Zt, f, L75, VF75)
    Zport = zin(top, Zt_junction)
    # junction voltage -> yagi currents
    V1 = 1.0
    def current(abcd, ZL, Vin):   # Vin at input, find IL: [Vin; Iin] = abcd [VL; IL], IL = VL/ZL
        Iin = Vin/zin(abcd, ZL); VL = (abcd[1,1]*Vin - abcd[0,1]*Iin)/(abcd[0,0]*abcd[1,1]-abcd[0,1]*abcd[1,0]); return VL/ZL
    IY = current(legY, yagi_Z, V1); IZ = current(legZ, yagi_Z, V1)
    return Zport, IZ/IY
res = json.load(open('calc/antenna_result.json')); out = {}
def optA(f, f0, Zy, d):
    top = tl(37.5, f, d['lam4_75_m'], VF75); Zl = zin(top, Zy)       # impedance each hybrid output sees
    g = abs((Zl-50)/(Zl+50)); return (1+g)/(1-g), g*g
for band, f0, sweep in (('VHF', 145.9, (144.0, 145.0, 145.9, 146.0, 147.0)), ('UHF', 436.5, (432.0, 435.0, 436.5, 438.0, 440.0))):
    key = 'vhf_combined' if band == 'VHF' else 'uhf_combined'
    R, X = res[key]['z_feed'][0]; Zy = complex(R, X)
    d = design(f0, R); out[band] = dict(design=d)
    print(f"{band}: lambda/4 free space {d['lam4_free_m']*100:.1f} cm; 50-ohm coax (VF {VF50}) {d['lam4_50_m']*100:.1f} cm; 75-ohm coax (VF {VF75}) {d['lam4_75_m']*100:.1f} cm (use 2 pieces in parallel -> 37.5 ohm); NEC Zyagi={R:.1f}{X:+.1f}j")
    rows = []
    for f in sweep:
        Zp, ratio = network(f, f0, Zy, d)
        g = abs((Zp-50)/(Zp+50)); swr = (1+g)/(1-g); ph = math.degrees(np.angle(ratio)); mag = abs(ratio)
        rows.append(dict(f=f, swr=round(swr, 2), phase_deg=round(ph, 1), amp_ratio=round(mag, 2)))
        print(f"   OPTION B(rejected) {f:6.1f} MHz  SWR at radio port {swr:4.2f}   yagi-Z vs yagi-Y current: {mag:4.2f} /{ph:7.1f} deg")
    out[band]['rows_optionB_rejected'] = rows
    rowsA = []
    for f in sweep:
        swr, g2 = optA(f, f0, Zy, d); rowsA.append(dict(f=f, swr_each_output=round(swr, 2), reflected_to_isolated_port_pct=round(100*g2, 1)))
        print(f"   OPTION A {f:6.1f} MHz  SWR at each hybrid output {swr:4.2f}  power lost to the isolated load {100*g2:4.1f} %  (input SWR ideal = 1.0)")
    out[band]['rows_optionA'] = rowsA
json.dump(out, open('calc/feed_result.json', 'w'), indent=1)
