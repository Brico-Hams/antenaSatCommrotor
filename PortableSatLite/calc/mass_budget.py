#!/usr/bin/env python3
"""Mass budget. 'printed' comes from the CAD model volumes (cad/parts.json, ASA 1.07 g/cm3, effective solid fraction 0.6 body / 1.0 gears => ESTIMATE).
Every purchased item is a typical catalogue value (ESTIMATE, weigh the real parts). Battery, tripod and radio are listed separately."""
import json
P = json.load(open('cad/parts.json'))
use = {  # part -> qty actually used in the default build
 'gear_sun_motor':2,'gear_planet':12,'rotor_housing':2,'carrier1_plate_A':2,'carrier1_plate_B_sun2':2,'carrier2_plate_A':2,'output_flange':2,'rotor_endcap':2,'motor_plate':2,
 'tripod_adapter_1-4':1,'boom_clamp_16_lower':1,'boom_clamp_16_upper':1,'cross_hub_16':7,'hinge_arm':28,'radio_cradle_RT3S':1,'control_box':1,'control_box_lid':1}
printed = sum(P[k]['est_mass_g']*q for k, q in use.items())
rod_g_per_m = 3.1416*(1.5e-3)**2*2700*1000
ant_rods = rod_g_per_m*(2*(1.0486+0.9909+0.9357+0.3344+0.3229+0.3093+0.2967))
items = [  # (name, grams, source)
 ('Antenna: 3 mm aluminium rods (cross VHF3 + UHF4)', ant_rods, 'computed from NEC element lengths'),
 ('Antenna: 16 mm PVC conduit boom 0.83 m (two 0.45 m sections)', 0.83*90, 'catalogue ~90 g/m (ESTIMATE)'),
 ('Antenna: coax/phasing parts (4 qwt, 2 hybrids, SMA)', 90, 'ESTIMATE'),
 ('Rotor: 2x NEMA17 34 mm body', 2*220, 'typical catalogue 200-250 g (ESTIMATE)'),
 ('Rotor: 2x 6806 bearing', 2*25, 'ESTIMATE'),
 ('Rotor: 12x 4x24 steel pins + M3/M4 hardware', 12*2.4 + 90, 'ESTIMATE'),
 ('Rotor: 2x 20 mm CF/Al stub tube 120 mm', 2*18, 'ESTIMATE'),
 ('Electronics: ESP32 + 2xTMC2209 + buck + GNSS + IMU/mag + 2xAS5600 + wiring', 10+16+10+10+5+6+120, 'ESTIMATE'),
 ('Diplexer 2m/70cm PCB + 3 bulkheads', 70, 'ESTIMATE (existing BRICOHAMS diplexer)'),
 ('Cables: 2 motor cables, 2 sensor cables, USB-C, antenna coax 2x0.5 m', 160, 'ESTIMATE'),
]
total_items = sum(g for _, g, _ in items)
print(f"printed parts (ASA, from CAD): {printed:7.0f} g")
for n, g, s in items: print(f"{n:78s} {g:6.0f} g   {s}")
station = printed + total_items
print(f"{'STATION (rotor+antenna+control box+diplexer), no radio/tripod/battery':78s} {station:6.0f} g")
for n, g in (('RT3S radio with battery', 270), ('photo tripod (typical travel carbon/alu)', 1200), ('12 V source: 3S Li-ion 6 Ah pack or USB-C PD 12 V trigger + power bank', 450)):
    print(f"   + {n:74s} {g:6.0f} g   ESTIMATE")
print(f"{'TOTAL carried (all estimates)':78s} {station+270+1200+450:6.0f} g")
json.dump(dict(printed_g=printed, station_g=station, total_carried_g=station+270+1200+450), open('calc/mass_result.json', 'w'), indent=1)
