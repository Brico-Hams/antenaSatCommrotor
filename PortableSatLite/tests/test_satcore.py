#!/usr/bin/env python3
"""Cross-checks satcore.h against an independent rotation-matrix model (ZYX Euler angles + yaw offset)."""
import subprocess, numpy as np, math, os, sys
root = os.path.dirname(os.path.abspath(__file__)); os.makedirs(root + '/out', exist_ok=True)
subprocess.check_call(['g++', '-O2', '-std=c++17', '-o', root + '/out/test_satcore', root + '/test_satcore.cpp'])
rng = np.random.default_rng(7)
def Rz(a): c,s=math.cos(a),math.sin(a); return np.array([[c,-s,0],[s,c,0],[0,0,1]])
def Ry(a): c,s=math.cos(a),math.sin(a); return np.array([[c,0,s],[0,1,0],[-s,0,c]])
def Rx(a): c,s=math.cos(a),math.sin(a); return np.array([[1,0,0],[0,c,-s],[0,s,c]])
cases=[]; exp=[]
for _ in range(2000):
    yaw=rng.uniform(0,2*math.pi); pitch=rng.uniform(-0.35,0.35); roll=rng.uniform(-0.35,0.35)   # body orientation in NED (up to ~20 deg tilt)
    decl_deg=rng.uniform(-15,15); dip=math.radians(rng.uniform(40,65)); az=rng.uniform(0,360); el=rng.uniform(0,90)
    # body->NED rotation (yaw about down, pitch about y, roll about x)
    Rb = Rz(yaw) @ Ry(pitch) @ Rx(roll)               # columns: body axes in NED
    # true-north NED frame; magnetic field: horizontal part points to magnetic north = true north rotated EAST by declination
    d=math.radians(decl_deg)
    m_ned = np.array([math.cos(dip)*math.cos(d), math.cos(dip)*math.sin(d), math.sin(dip)])   # N,E,D (dip positive downwards)
    up_ned = np.array([0,0,-1.0])
    m_b = Rb.T @ m_ned; up_b = Rb.T @ up_ned
    # expected: target in NED -> body
    t_ned = np.array([math.cos(math.radians(el))*math.cos(math.radians(az)), math.cos(math.radians(el))*math.sin(math.radians(az)), -math.sin(math.radians(el))])
    t_b = Rb.T @ t_ned
    az_r = math.degrees(math.atan2(t_b[1], t_b[0])) % 360; el_r = math.degrees(math.atan2(-t_b[2], math.hypot(t_b[0], t_b[1])))
    # heading of the body x axis projected on the horizontal plane, in true terms (what the manual-north mode is told)
    fwd_ned = Rb[:, 0]; heading = math.degrees(math.atan2(fwd_ned[1], fwd_ned[0])) % 360
    cases.append(f"{up_b[0]:.12f} {up_b[1]:.12f} {up_b[2]:.12f} {m_b[0]:.12f} {m_b[1]:.12f} {m_b[2]:.12f} {decl_deg:.6f} {az:.9f} {el:.9f} {heading:.9f}")
    exp.append((az_r, el_r, az, el, heading))
out = subprocess.run([root + '/out/test_satcore'], input="\n".join(cases), capture_output=True, text=True, check=True).stdout.split("\n")
worst=0; worst_rt=0; worst_h=0
for line, (ea, ee, az, el, hd) in zip(out, exp):
    a, e, a2, e2, ah, eh = map(float, line.split())
    da = abs((a - ea + 180) % 360 - 180); de = abs(e - ee)
    if -85.0 < ee < 85.0: worst = max(worst, da, de)       # azimuth undefined near the zenith of the rotor frame
    if -85.0 < ee < 85.0: worst_h = max(worst_h, abs((ah - ea + 180) % 360 - 180), abs(eh - ee))
    worst_rt = max(worst_rt, abs((a2 - az + 180) % 360 - 180) if el < 89 else 0, abs(e2 - el))
print(f"manual-heading frame vs model: max error {worst_h:.2e} deg")
print(f"satcore vs independent rotation model: max error {worst:.2e} deg over 2000 random tilt/heading cases; round-trip {worst_rt:.2e} deg")
assert worst < 1e-5 and worst_rt < 1e-6, "pointing mismatch"
# unwrap / Doppler spot checks
sys.path.insert(0, root)
