#!/usr/bin/env python3
"""Loads the real firmware/data/index.html against the mock API in headless Chromium: no console errors, passes listed, tracking starts, mobile layout has no horizontal overflow."""
import subprocess, time, sys, os, json
from playwright.sync_api import sync_playwright
root = os.path.dirname(os.path.abspath(__file__)); os.makedirs(root + '/out', exist_ok=True)
srv = subprocess.Popen([sys.executable, root + '/mock_server.py', '8765']); time.sleep(5)   # pass table is computed at start
errs = []
try:
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=os.environ.get('CHROMIUM', '/opt/pw-browsers/chromium'), args=['--no-sandbox']) if os.path.exists('/opt/pw-browsers/chromium') else p.chromium.launch(args=['--no-sandbox'])
        pg = b.new_page(viewport={'width': 390, 'height': 900}, device_scale_factor=2); pg.on('console', lambda m: errs.append(m.text) if m.type == 'error' else None); pg.on('pageerror', lambda e: errs.append(str(e)))
        pg.goto('http://127.0.0.1:8765/'); pg.wait_for_selector('#pl tr', timeout=20000)
        rows = pg.locator('#pl tr').count(); pg.locator('#pl button').first.click(); pg.wait_for_timeout(2500)
        ov = pg.evaluate('document.documentElement.scrollWidth - document.documentElement.clientWidth'); trk = pg.inner_text('#tgt'); dop = pg.inner_text('#dr')
        pg.screenshot(path=root + '/out/ui_mobile.png', full_page=True); pg.click('#lang'); pg.wait_for_timeout(300); en = pg.inner_text('h2'); b.close()
    print(f"passes rows={rows}, horizontal overflow={ov}px, target after Track='{trk}', RX Doppler='{dop}', EN toggle h2='{en}', console errors={errs}")
    assert rows >= 1 and ov <= 0 and not errs and trk != '--'
finally: srv.terminate()
