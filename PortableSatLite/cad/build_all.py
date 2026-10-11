#!/usr/bin/env python3
"""Generates every printable part as STL + a parts table (volume, bbox, watertight, estimated mass). Units mm.
Run:  python3 cad/build_all.py   (needs numpy, trimesh, manifold3d)"""
import sys, os, json, math
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np, trimesh
import manifold3d as m3
from manifold3d import Manifold as M, CrossSection as CS
from gears import *

OUT = os.path.join(os.path.dirname(__file__), 'stl'); os.makedirs(OUT, exist_ok=True)
# ---------------- parameters (change here, rebuild) ----------------
Z_S, Z_P, Z_R, MOD, PA, BETA, W = 12, 18, 48, 1.5, 20.0, 25.0, 16.0   # gear set: ratio 1+Zr/Zs = 5 per stage
CLR = 0.30                  # tooth clearance for FDM ASA (offset total, mm) - tune with the coupon
OUTER_R = 46.0              # housing radius
POCKET_R = 39.0             # carrier plate pocket
PIN_D = 4.0                 # planet axle (steel/stainless rod) mm
PLATE_T = 4.0               # carrier plate thickness
A_CD = (Z_S + Z_P)*MOD/2    # planet orbit radius = 22.5
N_PL = 3
BEARING = (30.0, 42.0, 7.0) # 6806: d, D, B  (output bearing)
NEMA_HOLES = 31.0; NEMA_BOSS = 22.5
DENS = 1.07                 # g/cm3 ASA
FILL = {'gear': 1.0, 'body': 0.60}   # effective solid fraction (walls+infill), ESTIMATE

def cyl(r, h, n=96, z0=0.0): return M.cylinder(h, r, r, n).translate([0, 0, z0])
def box(x, y, z, cx=True, cy=True): return M.cube([x, y, z]).translate([-x/2 if cx else 0, -y/2 if cy else 0, 0])
def holes_on_circle(r, n, hr, h, z0=-1, a0=0):
    out = None
    for i in range(n):
        a = math.radians(a0 + 360*i/n); c = cyl(hr, h + 2, 24, z0).translate([r*math.cos(a), r*math.sin(a), 0])
        out = c if out is None else out + c
    return out

parts = {}
def reg(name, m, kind='body', qty=1, note=''): parts[name] = dict(m=m, kind=kind, qty=qty, note=note)

# ---------------- planetary stage ----------------
sun1 = sun_solid(Z_S, MOD, W, BETA, 5.2, clr=CLR)
reg('gear_sun_motor', sun1, 'gear', 2, 'NEMA17 5 mm shaft (use grub screw M3 on a flat); 1 per axis')
reg('gear_planet', planet_solid(Z_P, MOD, W, BETA, PIN_D + 0.2, clr=CLR), 'gear', 12, '3 per stage x 2 stages x 2 axes')
# housing: two rings + pockets, bolt circle, motor-side flange
ring = ring_solid(Z_R, MOD, W, BETA, OUTER_R, clr=CLR, hand=-1)
H_total = PLATE_T + W + 2*PLATE_T + W + PLATE_T       # pocketA1 | gears1 | (B1+A2 shared pocket 2*T) | gears2 | pocket B2
housing = cyl(OUTER_R, H_total)
cav = None
def stack(z0, mm): return mm.translate([0, 0, z0])
cav = cyl(POCKET_R, PLATE_T + 0.4).translate([0, 0, 0])                                   # pocket for A1
ring_cav1 = (cyl(OUTER_R, W) - ring).translate([0, 0, PLATE_T])                           # gear cavity stage 1
mid_pocket = cyl(POCKET_R, 2*PLATE_T + 0.4).translate([0, 0, PLATE_T + W])
ring_cav2 = (cyl(OUTER_R, W) - ring).translate([0, 0, PLATE_T + W + 2*PLATE_T])
end_pocket = cyl(POCKET_R, PLATE_T + 0.4).translate([0, 0, H_total - PLATE_T - 0.4])
housing = housing - cav - ring_cav1 - mid_pocket - ring_cav2 - end_pocket
housing = housing - holes_on_circle(OUTER_R - 3.6, 6, 1.7, H_total)                       # 6x M3 through-bolts
housing = housing - holes_on_circle(OUTER_R - 3.6, 6, 3.2, 3.0, z0=H_total - 3.0 + 1).translate([0, 0, 0])  # nut traps at top (hex approximated by round)
reg('rotor_housing', housing, 'body', 2, 'two internal herringbone rings, one piece; 6 x M3 through-bolts')
def plate(r, t, hub=None, nip=N_PL, pin_hole=PIN_D + 0.1, center_hole=None):
    p = cyl(r, t) - holes_on_circle(A_CD, nip, pin_hole/2, t)
    if center_hole: p = p - cyl(center_hole/2, t + 2).translate([0, 0, -1])
    return p
# carrier A1 (motor side): sun1 passes through the centre; pins pressed in.
reg('carrier1_plate_A', plate(POCKET_R - 0.8, PLATE_T, center_hole=14.0), 'body', 2, 'planet axles pressed (4 mm rod, 3 per plate)')
# carrier B1 + sun2 hub (hub = sun gear, same herringbone, longer)
sun2 = sun_solid(Z_S, MOD, W, BETA, 0.01, clr=CLR)  # gear body without bore
b1 = plate(POCKET_R - 0.8, PLATE_T) + sun2.translate([0, 0, PLATE_T]) - cyl(2.0, W + PLATE_T + 2).translate([0, 0, -1])  # 4 mm blind-through bore for alignment pin
reg('carrier1_plate_B_sun2', b1, 'gear', 2, 'plate with integrated 2nd-stage sun (print upright, tune clearance)')
reg('carrier2_plate_A', plate(POCKET_R - 0.8, PLATE_T, center_hole=16.0), 'body', 2, 'rides on sun2 hub, axles pressed')
# output flange (B2): 3 pin holes, hub with bearing journal, 40 mm PCD flange with 4xM4, 20 mm spigot socket
hub_len = PLATE_T + BEARING[2] + 2
flange = plate(POCKET_R - 0.8, PLATE_T) + cyl(BEARING[0]/2, BEARING[2] + 6).translate([0, 0, PLATE_T])
flange = flange + cyl(24.0, 5).translate([0, 0, PLATE_T + BEARING[2] + 6])
flange = flange - cyl(10.2, 26).translate([0, 0, PLATE_T + BEARING[2] + 6 + 5 - 24])      # 20.4 mm socket for the universal stub (24 deep)
flange = flange - holes_on_circle(20.0, 4, 2.2, 60, z0=-30)                               # M4 on 40 mm PCD
reg('output_flange', flange, 'body', 2, 'universal interface: 4xM4 on 40 mm PCD + 20 mm spigot')
endcap = cyl(OUTER_R, 10.0) - cyl(BEARING[1]/2, BEARING[2] + 0.1).translate([0, 0, 10 - BEARING[2] - 0.1]) - cyl(BEARING[0]/2 + 1.0, 12).translate([0, 0, -1])
endcap = endcap - holes_on_circle(OUTER_R - 3.6, 6, 1.7, 10)
reg('rotor_endcap', endcap, 'body', 2, '6806 bearing seat; 6 x M3 same circle as the housing')
# motor plate NEMA17
mp = cyl(OUTER_R, 6.0) - cyl(NEMA_BOSS/2 + 0.2, 8).translate([0, 0, -1]) - holes_on_circle(NEMA_HOLES*math.sqrt(2)/2, 4, 1.7, 6, a0=45) - holes_on_circle(OUTER_R - 3.6, 6, 1.7, 6)
reg('motor_plate', mp, 'body', 2, 'NEMA17 31 mm square pattern, 6xM3 to the housing')
# ---------------- universal adapters ----------------
# tripod adapter: 4xM4/40 PCD to 1/4"-20 (and 3/8" via same hole using bush)
ta = cyl(34.0, 8) - holes_on_circle(20.0, 4, 2.2, 8) - cyl(3.4, 12).translate([0, 0, -2]) - cyl(6.7, 4.5, 6).translate([0, 0, -0.5])
ta = ta + cyl(10.0, 10).translate([0, 0, 8]) - cyl(3.4, 30).translate([0, 0, -1])
reg('tripod_adapter_1-4', ta, 'body', 1, 'M4 flange side + 1/4"-20 screw (hex nut M6.35 trap underneath); 3/8" tripods: use stock reducer bush')
# stub (20 mm spigot) with flats, 80 mm long
stub = cyl(10.0, 80, 64) - cyl(5.0, 82, 48).translate([0, 0, -1])
reg('stub_spigot_20', stub, 'body', 2, 'OPTIONAL printed stub; cheaper: 20 mm aluminium/CF tube 1 mm wall (BOM)')
def boom_clamp(boom_d, name):
    L = 36.0; Wc = 40.0; H = 34.0
    body = box(Wc, L, H)                                    # block centred XY
    body = body.translate([0, 0, 0])
    ch = cyl(boom_d/2 + 0.15, L + 2).rotate([90, 0, 0]).translate([0, L/2 + 1, H/2])             # boom channel along Y
    st = cyl(10.25, H + 2).translate([0, 0, -1])                                                  # not used: stub socket perpendicular below
    sock = cyl(10.25, 20).translate([0, 0, -1])                                                   # 20 mm stub socket from below, along Z
    body = body - ch - sock
    # split plane at channel axis (z = H/2): lower and upper halves printed separately
    lower = body ^ box(Wc + 2, L + 2, H/2)
    upper = (body ^ box(Wc + 2, L + 2, H/2).translate([0, 0, H/2]))
    for sx in (-14, 14):
        bolt = cyl(2.1, H + 2, 24).translate([sx, 0, -1])
        lower = lower - bolt; upper = upper - bolt
    # slit + clamp bolt on the stub socket
    return lower, upper
for d in (16, 20, 25):
    lo, up = boom_clamp(d, d)
    reg(f'boom_clamp_{d}_lower', lo, 'body', 1, f'for {d} mm boom; bolts 2xM4 (nut traps omitted -> use nylock + washer)'); reg(f'boom_clamp_{d}_upper', up, 'body', 1)
# cross hub for the crossed yagi: boom 16 mm, two orthogonal rod sockets (Y at x=0, Z at x=+10 mm), hinge lugs
def cross_hub(boom_d=16.0):
    hub = cyl(boom_d/2 + 4.5, 18).rotate([0, 90, 0]).translate([-9, 0, 0])          # sleeve along X
    hub = hub - cyl(boom_d/2 + 0.15, 20).rotate([0, 90, 0]).translate([-10, 0, 0])
    lug_y = box(8, 14, 8).translate([-0.0, 0, 0])
    # lugs: horizontal rod hinge on +/-Y, vertical on +/-Z
    for s in (1, -1):
        hub = hub + box(10, 9, 9).translate([-4, s*(boom_d/2 + 6.5), 0]) + box(10, 9, 9).translate([6, 0, s*(boom_d/2 + 6.5)])
        hub = hub - cyl(1.65, 14).rotate([0, 90, 0]).translate([-10, s*(boom_d/2 + 6.5), 0]) if False else hub
    return hub
ch = cross_hub()
# pivot holes for M3 (axis along X for Y-rods, along Y for Z-rods)
for s in (1, -1):
    ch = ch - cyl(1.65, 30).rotate([0, 90, 0]).translate([-20, s*(8 + 6.5), 0])
    ch = ch - cyl(1.65, 30).rotate([90, 0, 0]).translate([6 , 15, s*(8 + 6.5)])
reg('cross_hub_16', ch, 'body', 7, '1 per element station (3 VHF + 4 UHF); 4 hinge lugs for M3 pivots')
arm = box(12, 5.0, 16.0).translate([0, 0, 0]) + cyl(5.0, 5).translate([0, 0, 0]) .rotate([90, 0, 0]).translate([0, 2.5, 0])
arm = arm - cyl(1.65, 20).rotate([90, 0, 0]).translate([0, 10, 0]) - cyl(1.55, 20).translate([0, 0, 0]).translate([0, 0, 0])
reg('hinge_arm', arm, 'body', 28, 'swing arm: 3.1 mm bore for the 3 mm aluminium rod (epoxy/M2 grub); folds along the boom')
# RT3S radio cradle (dimensions are PARAMETERS -- measure your radio)
RW, RT, RH = 60.0, 36.0, 118.0
cr = box(RW + 8, RT + 8, 6) + box(RW + 8, 4, 40).translate([0, (RT + 4)/2, 0]) + box(RW + 8, 4, 40).translate([0, -(RT + 4)/2, 0])
cr = cr + box(4, RT + 8, 40).translate([(RW + 4)/2, 0, 0]) + box(4, RT + 8, 40).translate([-(RW + 4)/2, 0, 0])
cr = cr - box(RW, RT, 48).translate([0, 0, 6]) - box(RW - 24, 90, 20).translate([0, 0, -1])
cr = cr - holes_on_circle(20.0, 4, 2.2, 8)
reg('radio_cradle_RT3S', cr, 'body', 1, 'open-top tray, 4xM4 on 40 mm PCD (same as every interface) + Velcro strap through the side windows; internal size is a PARAMETER')
# control box with diplexer bay
BX, BY, BZ = 112.0, 82.0, 42.0; WALL = 2.4
bx = box(BX, BY, BZ) - box(BX - 2*WALL, BY - 2*WALL, BZ).translate([0, 0, WALL])
bx = bx - cyl(5.0, 6).rotate([0, 90, 0]).translate([BX/2 - 3, -20, 16]) - cyl(5.0, 6).rotate([0, 90, 0]).translate([BX/2 - 3, 0, 16]) - cyl(5.0, 6).rotate([0, 90, 0]).translate([BX/2 - 3, 20, 16])   # BNC/SMA bulkheads J1..J3 (diplexer face)
bx = bx - cyl(6.0, 6).rotate([90, 0, 0]).translate([-30, -BY/2 + 3, 20]) - cyl(6.0, 6).rotate([90, 0, 0]).translate([0, -BY/2 + 3, 20])                    # motor cables
bx = bx - cyl(5.0, 6).rotate([90, 0, 0]).translate([30, -BY/2 + 3, 20]) - cyl(4.5, 6).rotate([0, 90, 0]).translate([-BX/2 + 3, 20, 16])                    # sensor+USB-C
bx = bx - holes_on_circle(20.0, 4, 2.2, 8)
posts = None
for px in (-BX/2 + 5, BX/2 - 5):
    for py in (-BY/2 + 5, BY/2 - 5):
        pst = cyl(4.0, BZ - 2.2).translate([px, py, WALL])
        bx = bx + pst - cyl(1.3, BZ).translate([px, py, WALL + 8])
reg('control_box', bx, 'body', 1, 'ESP32 + 2xTMC2209 + buck/PD + diplexer bay (72x40 PCB, BNC/SMA bulkheads on +X face)')
lid = box(BX, BY, 2.4) - holes_on_circle(20.0, 4, 2.2, 8)
reg('control_box_lid', lid, 'body', 1)
# element tuning coupon (test print for tooth clearance)
cp = cyl(12.0, 12.0) - cyl(2.6, 14).translate([0, 0, -1])
reg('coupon_gear_clearance', herringbone(gear_profile(Z_P, MOD, PA), 8.0, BETA, Z_P*MOD/2) - cyl(2.0, 12).translate([0, 0, -1]), 'gear', 1, 'print this first: check it slides on the 4 mm pin and meshes with a printed sun tooth coupon')

# ---------------- export + table ----------------
table = {}
for n, p in parts.items():
    m = p['m']; mesh = m.to_mesh(); tm = trimesh.Trimesh(vertices=mesh.vert_properties[:, :3], faces=mesh.tri_verts, process=True)
    tm.export(os.path.join(OUT, n + '.stl'))
    vol = m.volume()/1000.0                   # cm3
    mass = vol*DENS*FILL[p['kind']]
    bb = tm.bounds
    table[n] = dict(volume_cm3=round(vol, 2), size_mm=[round(float(x), 1) for x in (bb[1]-bb[0])], watertight=bool(tm.is_watertight), est_mass_g=round(mass, 1), qty=p['qty'], note=p['note'])
json.dump(table, open(os.path.join(os.path.dirname(__file__), 'parts.json'), 'w'), indent=1)
tot = sum(v['est_mass_g']*v['qty'] for v in table.values())
print(f"{'part':28s} {'qty':>3s} {'size mm':>22s} {'cm3':>7s} {'g(est)':>7s} watertight")
for n, v in table.items(): print(f"{n:28s} {v['qty']:3d} {str(v['size_mm']):>22s} {v['volume_cm3']:7.1f} {v['est_mass_g']:7.1f} {v['watertight']}")
print('printed mass total (qty counted, for the parts listed incl. 2 rotor axes):', round(tot), 'g')
