#!/usr/bin/env python3
"""Mock of the firmware HTTP API (same endpoints/JSON) so the web UI can be exercised without hardware. Uses python-sgp4 + the same satcore maths via ctypes-free python port.
Fake clock = TLE epoch + 1 h so the 2019 ISS TLE is accurate."""
import json, math, time, sys, os, threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse, parse_qs
import numpy as np
from sgp4.api import Satrec, WGS72
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'firmware', 'data')
l1 = "1 25544U 98067A   19343.69339541  .00001764  00000-0  38792-4 0  9991"; l2 = "2 25544  51.6439 211.2001 0007417  17.6667  85.6398 15.50103472202482"
sat = Satrec.twoline2rv(l1, l2, WGS72); EP = int((sat.jdsatepoch + sat.jdsatepochF - 2440587.5)*86400)
T0 = EP + 5400; WALL0 = time.time()
LAT, LON = 38.0, -1.3; lat, lon = math.radians(LAT), math.radians(LON)
def now(): return int(T0 + (time.time() - WALL0)*30)       # 30x time lapse so a pass is visible in a screenshot
def gmst(jd): T = (jd-2451545.0)/36525.0; return math.radians((280.46061837 + 360.98564736629*(jd-2451545.0) + 0.000387933*T*T) % 360)
a = 6378.137; f = 1/298.257223563; e2 = f*(2-f); N = a/math.sqrt(1-e2*math.sin(lat)**2)
site = np.array([(N+0.1)*math.cos(lat)*math.cos(lon), (N+0.1)*math.cos(lat)*math.sin(lon), (N*(1-e2)+0.1)*math.sin(lat)])
Sm = np.array([[math.sin(lat)*math.cos(lon), math.sin(lat)*math.sin(lon), -math.cos(lat)], [-math.sin(lon), math.cos(lon), 0], [math.cos(lat)*math.cos(lon), math.cos(lat)*math.sin(lon), math.sin(lat)]])
def azel(t):
    jd = t/86400 + 2440587.5; jdi = math.floor(jd-0.5)+0.5; e, r, v = sat.sgp4(jdi, jd-jdi); th = gmst(jd)
    R = np.array([[math.cos(th), math.sin(th), 0], [-math.sin(th), math.cos(th), 0], [0, 0, 1]]); s = Sm @ (R @ np.array(r) - site); rho = np.linalg.norm(s)
    return math.degrees(math.atan2(s[1], -s[0])) % 360, math.degrees(math.asin(s[2]/rho)), rho
def passes(t0):
    out = []; up = azel(t0)[1] > 0; aos = t0 if up else 0; best = (-90, 0)
    for t in range(t0, t0 + 24*3600, 30):
        el = azel(t)[1]
        if el > best[0] and up: best = (el, t)
        if el > 0 and not up: aos = t; best = (el, t)
        if el <= 0 and up and best[0] >= 10: out.append(dict(sat=0, id='ISS', aos=aos, tca=best[1], los=t, max_el=round(best[0], 1), az_aos=round(azel(aos)[0]), az_los=round(azel(t)[0])))
        if el <= 0 and up: best = (-90, 0)
        up = el > 0
    return out
PASSES = passes(T0)
state = dict(tracking=-1, az=0.0, el=0.0, decl=0.0, north=None)
class H(BaseHTTPRequestHandler):
    def log_message(self, *a): pass
    def _send(self, body, ctype='application/json', code=200):
        b = body.encode() if isinstance(body, str) else body; self.send_response(code); self.send_header('Content-Type', ctype); self.send_header('Content-Length', str(len(b))); self.end_headers(); self.wfile.write(b)
    def do_POST(self): self.do_GET()
    def do_GET(self):
        u = urlparse(self.path); q = {k: v[0] for k, v in parse_qs(u.query).items()}
        if u.path == '/': return self._send(open(ROOT + '/index.html', 'rb').read(), 'text/html')
        if u.path == '/api/state':
            t = now(); az, el, rho = azel(t); rr = (azel(t+1)[2] - azel(t-1)[2])/2
            tr = state['tracking']; tg = (0, 0)
            if tr >= 0: tg = (az, max(el, 0)); state['az'] += (tg[0]-state['az'])*0.5; state['el'] += (tg[1]-state['el'])*0.5
            j = dict(unix=t, have_time=1, gps_fix=1, sats=9, lat=LAT, lon=LON, alt=100, site_manual=0, roll=1.2, pitch=-0.8, heading=212.4, decl=state['decl'], north_manual=state['north'], frame_ok=1,
                     az=state['az'], el=state['el'], tgt_az=tg[0], tgt_el=tg[1], tracking=tr, sat_az=az, sat_el=el, rr=rr, dop_rx=145.990e6*(1-rr/299792.458), dop_tx=437.800e6*(1+rr/299792.458), cal=0, sta=0, tle_count=1,
                     catalog=[dict(i=0, id='ISS', dl=145.990, ul=437.800, have_tle=1), dict(i=1, id='SO-50', dl=436.795, ul=145.850, have_tle=0)])
            return self._send(json.dumps(j))
        if u.path == '/api/passes': return self._send(json.dumps(PASSES))
        if u.path == '/api/track': state['tracking'] = int(q.get('sat', 0)); return self._send('{"ok":1}')
        if u.path == '/api/stop': state['tracking'] = -1; return self._send('{"ok":1}')
        if u.path == '/api/tle_update': return self._send('STA not connected: set a Wi-Fi (phone hotspot) in Settings', 'text/plain')
        return self._send('{"ok":1}')
if __name__ == '__main__':
    ThreadingHTTPServer(('127.0.0.1', int(sys.argv[1]) if len(sys.argv) > 1 else 8765), H).serve_forever()
