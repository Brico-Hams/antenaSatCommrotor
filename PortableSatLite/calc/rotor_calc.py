#!/usr/bin/env python3
"""Torque, gear stress, resolution and wind-load checks for the 25:1 (5:1 x 5:1) herringbone planetary rotor axis."""
import math, json
# --- inputs (ASSUMPTIONS flagged; replace with your motor datasheet / measurements) ---
MOTOR_HOLD_NM = 0.25          # NEMA17 34 mm body, holding torque (typ. 0.2-0.3 N.m, VERIFY datasheet of the motor you buy)
STAGE_EFF = 0.90              # per planetary stage (helical, plastic, dry) - assumption
Zs, Zp, Zr, MOD, FACE, BETA, PA = 12, 18, 48, 1.5, 16.0, 25.0, 20.0
N_PL = 3
SIGMA_ALLOW_MPA = 9.0         # allowable bending stress for printed ASA gear tooth (conservative; ~20% of tensile, layer-direction, creep) - assumption
STEPS_REV, MICRO = 200, 16
ratio_stage = 1 + Zr/Zs; ratio = ratio_stage**2
# Antenna loads
rods_vhf = [1.0486, 0.9909, 0.9357]; rods_uhf = [0.3344, 0.3229, 0.3093, 0.2967]; D_ROD = 0.003
A_rods = 2*(sum(rods_vhf)+sum(rods_uhf))*D_ROD; A_boom = 0.83*0.016; A = A_rods + A_boom
RHO = 1.225; CD = 1.2
def wind_torque(v, arm):   # N.m, flat-on worst case; arm = distance from axis to centre of pressure (m)
    return 0.5*RHO*v*v*CD*A*arm
# Lewis bending, helical -> use virtual teeth z' = z/cos^3(beta); Y(z') interpolated for 20 deg PA (Lewis form factor)
def lewis_Y(z):
    t = [(12,0.245),(13,0.261),(14,0.276),(15,0.289),(16,0.295),(17,0.302),(18,0.308),(20,0.320),(25,0.340),(30,0.358),(40,0.389),(50,0.408),(75,0.433),(100,0.447),(300,0.480)]
    for (z0,y0),(z1,y1) in zip(t, t[1:]):
        if z0 <= z <= z1: return y0 + (y1-y0)*(z-z0)/(z1-z0)
    return t[-1][1] if z > t[-1][0] else t[0][1]
def sun_stress(T_in):
    rp = Zs*MOD/2/1000
    Ft = T_in/rp/N_PL                                  # N per planet mesh (ideal load sharing; real: x1.3 unequal sharing factor below)
    zv = Zs/math.cos(math.radians(BETA))**3
    Y = lewis_Y(zv); b = FACE
    return 1.3*Ft/(b*MOD*Y*math.cos(math.radians(BETA))), Ft, zv, Y
out = {}
T1 = MOTOR_HOLD_NM                     # worst case: stall at holding torque (steppers can briefly exceed; keep current set to rated)
s1, Ft1, zv, Y = sun_stress(T1)
T2 = T1*ratio_stage*STAGE_EFF
s2, Ft2, _, _ = sun_stress(T2)
T_out = T1*ratio*STAGE_EFF**2
print(f"ratio per stage {ratio_stage:.1f}:1, total {ratio:.0f}:1; microsteps/rev {STEPS_REV*MICRO*ratio:.0f}; resolution {360/(STEPS_REV*MICRO*ratio):.5f} deg/microstep")
print(f"Lewis Y at virtual teeth z'={zv:.1f}: {Y:.3f}")
print(f"stage-1 sun tooth stress at stall: {s1:.2f} MPa (Ft/mesh {Ft1:.1f} N)  -> safety factor {SIGMA_ALLOW_MPA/s1:.1f}")
print(f"stage-2 sun tooth stress at stall: {s2:.2f} MPa (Ft/mesh {Ft2:.1f} N)  -> safety factor {SIGMA_ALLOW_MPA/s2:.1f}")
print(f"output holding torque at stall: {T_out:.2f} N.m")
print(f"projected area (rods+boom): {A*1e4:.0f} cm2")
for v in (5, 10, 15):
    for arm in (0.25, 0.40):
        tw = wind_torque(v, arm)
        print(f"  wind {v:2d} m/s ({v*3.6:3.0f} km/h) arm {arm:.2f} m: {tw:5.2f} N.m  margin vs output holding {T_out/tw:5.1f}x")
# pointing resolution vs beamwidth
bw = json.load(open('calc/beamwidth_result.json'))
print(f"NEC 3 dB beamwidth: VHF {bw['VHF']['plane_XY_deg']:.0f} deg, UHF {bw['UHF']['plane_XY_deg']:.0f} deg -> 0.0045 deg/microstep is ~4 orders finer than needed; 25:1 is chosen for TORQUE (wind) and backlash masking, not accuracy.")
for frac in (1.0, 0.6, 0.5):
    s2f, *_ = sun_stress(T2*frac)
    print(f"  stage-2 sun stress with motor current limited to {frac*100:.0f}% of rated holding torque: {s2f:.2f} MPa (SF {SIGMA_ALLOW_MPA/s2f:.1f}), output torque {T_out*frac:.2f} N.m")
# speed: microstep rate for X deg/s
for w in (1, 5, 20):
    sps = w/360*STEPS_REV*MICRO*ratio
    print(f"  {w:2d} deg/s needs {sps:7.0f} microsteps/s")
json.dump(dict(ratio=ratio, stress_stage1_mpa=s1, stress_stage2_mpa=s2, out_torque_nm=T_out, area_m2=A), open('calc/rotor_result.json', 'w'), indent=1)
