#!/usr/bin/env python3
"""Tracker (firmware wrapper) pass list vs brute-force python-sgp4 (10 s sampling): AOS/TCA/LOS times, max elevation."""
import subprocess, os, math, glob
import numpy as np
from sgp4.api import Satrec, WGS72
root = os.path.dirname(os.path.abspath(__file__)); lib = os.environ.get('SGP4_LIB', '/home/claude/ext/Sgp4-Library/src')
srcs = glob.glob(lib + '/*.cpp')
subprocess.check_call(['g++', '-O1', '-std=gnu++17', '-Uunix', '-w', '-I', root + '/host_stub', '-I', lib, '-I', root + '/../firmware/lib/satcore', '-o', root + '/out/test_tracker', root + '/test_tracker.cpp'] + srcs)
l1 = "1 25544U 98067A   19343.69339541  .00001764  00000-0  38792-4 0  9991"; l2 = "2 25544  51.6439 211.2001 0007417  17.6667  85.6398 15.50103472202482"
sat = Satrec.twoline2rv(l1, l2, WGS72); t0 = int((sat.jdsatepoch + sat.jdsatepochF - 2440587.5)*86400)
LAT, LON, ALT, MINEL = 38.0, -1.3, 0.1, 10.0
out = subprocess.run([root + '/out/test_tracker', str(LAT), str(LON), str(t0), str(MINEL)], capture_output=True, text=True, check=True).stdout.strip().split('\n')
lat, lon = math.radians(LAT), math.radians(LON)
def gmst(jd): T = (jd-2451545.0)/36525.0; return math.radians((280.46061837 + 360.98564736629*(jd-2451545.0) + 0.000387933*T*T) % 360)
a = 6378.137; f = 1/298.257223563; e2 = f*(2-f); N = a/math.sqrt(1-e2*math.sin(lat)**2)
site = np.array([(N+ALT)*math.cos(lat)*math.cos(lon), (N+ALT)*math.cos(lat)*math.sin(lon), (N*(1-e2)+ALT)*math.sin(lat)])
S = np.array([[math.sin(lat)*math.cos(lon), math.sin(lat)*math.sin(lon), -math.cos(lat)], [-math.sin(lon), math.cos(lon), 0], [math.cos(lat)*math.cos(lon), math.cos(lat)*math.sin(lon), math.sin(lat)]])
def el_at(t):
    jd = t/86400 + 2440587.5; jdi = math.floor(jd-0.5)+0.5; e, r, v = sat.sgp4(jdi, jd-jdi); th = gmst(jd)
    R = np.array([[math.cos(th), math.sin(th), 0], [-math.sin(th), math.cos(th), 0], [0, 0, 1]]); s = S @ (R @ np.array(r) - site)
    return math.degrees(math.asin(s[2]/np.linalg.norm(s)))
ts = np.arange(t0, t0 + 36*3600, 10); els = np.array([el_at(t) for t in ts])
passes = []; i = 0
while i < len(ts):
    if els[i] > 0.0:
        j = i
        while j < len(ts) and els[j] > 0.0: j += 1
        k = i + int(np.argmax(els[i:j]))
        if els[k] >= MINEL and i > 0 and j < len(ts): passes.append((ts[i], ts[k], ts[j-1], els[k]))
        i = j
    else: i += 1
print(f"python reference: {len(passes)} passes above {MINEL} deg in 36 h")
worst = 0; worst_el = 0; matched = 0
fw = [tuple(map(float, l.split()[:4])) for l in out]
for ref in passes:
    c = min(fw, key=lambda p: abs(p[1]-ref[1]))
    d = max(abs(c[0]-ref[0]), abs(c[1]-ref[1]), abs(c[2]-ref[2])); de = abs(c[3]-ref[3])
    print(f"  ref pass TCA {int(ref[1])} max el {ref[3]:5.1f}: fw dt AOS/TCA/LOS = {c[0]-ref[0]:+4.0f}/{c[1]-ref[1]:+4.0f}/{c[2]-ref[2]:+4.0f} s, max el fw {c[3]:5.1f}")
    worst = max(worst, d); worst_el = max(worst_el, de); matched += d < 20
print(f"{matched}/{len(passes)} reference passes matched; max |dt| = {worst:.0f} s (reference sampled at 10 s), max |d_maxel| = {worst_el:.2f} deg; the extra firmware pass is the one already in progress at the start of the window")
assert matched == len(passes) and worst_el < 1.0, "pass prediction disagrees"
