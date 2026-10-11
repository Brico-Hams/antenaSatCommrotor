#!/usr/bin/env python3
"""Firmware SGP4 library (Hopperpop/Sgp4-Library, MIT) vs python-sgp4 reference (Vallado WGS72) -- az/el/range at the station."""
import subprocess, os, math, sys, glob
import numpy as np
from sgp4.api import Satrec, jday, WGS72
root = os.path.dirname(os.path.abspath(__file__)); lib = os.environ.get('SGP4_LIB', '/home/claude/ext/Sgp4-Library/src')
srcs = [f for f in glob.glob(lib + '/*.cpp')]
subprocess.check_call(['g++', '-O1', '-std=gnu++17', '-Uunix', '-w', '-I', root + '/host_stub', '-I', lib, '-o', root + '/out/test_sgp4_lib', root + '/test_sgp4_lib.cpp'] + srcs)
l1 = "1 25544U 98067A   19343.69339541  .00001764  00000-0  38792-4 0  9991"; l2 = "2 25544  51.6439 211.2001 0007417  17.6667  85.6398 15.50103472202482"
sat = Satrec.twoline2rv(l1, l2, WGS72)
epoch_unix = (sat.jdsatepoch + sat.jdsatepochF - 2440587.5) * 86400
times = [int(epoch_unix + k*300) for k in range(0, 120)]
out = subprocess.run([root + '/out/test_sgp4_lib'] + [str(t) for t in times], capture_output=True, text=True, check=True).stdout.strip().split('\n')
lat, lon, alt = math.radians(38.0), math.radians(-1.3), 0.1
def gmst(jd):
    T = (jd - 2451545.0) / 36525.0
    g = 280.46061837 + 360.98564736629 * (jd - 2451545.0) + 0.000387933 * T*T
    return math.radians(g % 360)
def ecef_site():
    a = 6378.137; f = 1/298.257223563; e2 = f*(2-f); N = a/math.sqrt(1-e2*math.sin(lat)**2)
    return np.array([(N+alt)*math.cos(lat)*math.cos(lon), (N+alt)*math.cos(lat)*math.sin(lon), (N*(1-e2)+alt)*math.sin(lat)])
site = ecef_site(); worst_el = worst_az = worst_r = 0
for line in out:
    t, az, el, rng_, la, lo = map(float, line.split())
    jd = t/86400 + 2440587.5; jdi = math.floor(jd - 0.5) + 0.5; fr = jd - jdi
    e, r, v = sat.sgp4(jdi, fr)
    th = gmst(jd); R = np.array([[math.cos(th), math.sin(th), 0], [-math.sin(th), math.cos(th), 0], [0, 0, 1]])   # TEME->ECEF (no polar motion)
    rec = R @ np.array(r); d = rec - site
    S = np.array([[math.sin(lat)*math.cos(lon), math.sin(lat)*math.sin(lon), -math.cos(lat)], [-math.sin(lon), math.cos(lon), 0], [math.cos(lat)*math.cos(lon), math.cos(lat)*math.sin(lon), math.sin(lat)]])
    s = S @ d; rho = np.linalg.norm(s); eaz = math.degrees(math.atan2(s[1], -s[0])) % 360; eel = math.degrees(math.asin(s[2]/rho))
    if abs(eel) < 89 and abs(el) < 89: worst_az = max(worst_az, abs((az-eaz+180) % 360 - 180))
    worst_el = max(worst_el, abs(el-eel)); worst_r = max(worst_r, abs(rng_-rho))
print(f"Sgp4-Library vs python-sgp4 (120 samples, 10 h): max |d_az|={worst_az:.3f} deg, max |d_el|={worst_el:.3f} deg, max |d_range|={worst_r:.2f} km")
assert worst_el < 0.2 and worst_az < 0.2 and worst_r < 5, "library disagrees with reference"
