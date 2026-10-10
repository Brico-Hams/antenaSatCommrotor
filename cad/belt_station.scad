// ORIGINAL lightweight BASE alternative. All pulleys and belts are PURCHASED.
// Cylinders are declared procurement envelopes, NOT printable tooth profiles.
// See docs/MECHANICAL.md for metal fabrication and unverified purchase drawings.
include <parameters.scad>
include <gears.scad>
include <mechanical.scad>
include <antenna.scad>
belt_part="assembly";
belt_pitch=2;
small_teeth=20;
large_teeth=100;
belt_length=252;
small_r=small_teeth*belt_pitch/(2*PI);
large_r=large_teeth*belt_pitch/(2*PI);
// Exact open belt tangent geometry (not the approximate length formula).
function belt_path_length(c) = let(a=asin((large_r-small_r)/c))
    2*sqrt(c*c-pow(large_r-small_r,2))
    +PI*(large_r+small_r)+2*a*PI/180*(large_r-small_r);
function solve_center(lo,hi,n=45)=n==0?(lo+hi)/2:
    belt_path_length((lo+hi)/2)>belt_length?
        solve_center(lo,(lo+hi)/2,n-1):solve_center((lo+hi)/2,hi,n-1);
C=solve_center(large_r-small_r+0.1,100);
assert(small_teeth==20&&large_teeth==100);
assert(abs(belt_path_length(C)-belt_length)<0.00001);
assert(C>large_r+small_r+3,"Pulley envelopes collide");
module adjustment_slot(d,h,travel=3) {
    hull() for(x=[-travel/2,travel/2]) translate([x,0,0]) cylinder(d=d,h=h);
}
module purchased_pulley(n,bore) {
    r=n*belt_pitch/(2*PI);
    color("silver") difference() {
        union() {
            cylinder(r=r+1.5,h=1);
            translate([0,0,1]) cylinder(r=r,h=6);
            translate([0,0,7]) cylinder(r=r+1.5,h=1);
            translate([0,0,8]) cylinder(d=n==20?18:30,h=4);
        }
        translate([0,0,-1]) cylinder(d=bore,h=14);
    }
}
module purchased_belt() {
    // Two common external tangents and their circular end arcs. Convex hull
    // of pitch circles IS this exact open-belt path. 1.4 mm backing envelope.
    color("black") difference() {
        linear_extrude(height=6) hull() {
            circle(r=small_r+0.7);
            translate([C,0]) circle(r=large_r+0.7);
        }
        translate([0,0,-1]) linear_extrude(height=8) hull() {
            circle(r=small_r-0.7);
            translate([C,0]) circle(r=large_r-0.7);
        }
    }
}
module metal_plate(rear=false) {
    // 3 mm aluminum plate; pockets are milled/drilled, not ASA STL.
    difference() {
        translate([-C-21,-43,0]) cube([2*C+66,86,3]);
        translate([0,0,-1]) adjustment_slot(9,5); // paired bearing blocks slide together
        translate([C,0,-1]) cylinder(d=11,h=5);
        if(!rear) {
            translate([-C,0,-1]) adjustment_slot(23,5);
            for(x=[-1,1],y=[-1,1]) translate([-C+x*13,y*13,-1]) adjustment_slot(3.4,5);
        }
        for(x=[-C-12,C+35],y=[-35,35])
            translate([x,y,-1]) cylinder(d=4.5,h=5);
        for(x=[0,C],a=[45:90:315]) translate([x+19*cos(a),19*sin(a),-1])
            if(x==0) adjustment_slot(3.4,5); else cylinder(d=3.4,h=5);
        if(rear) for(y=[-8,8]) translate([C-25,y,-1]) cylinder(d=3.4,h=5);
        // Preserve bearing islands and continuous edge rails.
        for(x=[-C/2,C/2]) translate([x,0,-1]) cylinder(d=24,h=5);
    }
}
module aluminum_standoff(length=51) {
    color("silver") difference() {
        cylinder(d=8,h=length);
        translate([0,0,-1]) cylinder(d=4.5,h=length+2);
    }
}
module belt_keeper(output=false) {
    difference() {
        cylinder(d=48,h=3);
        translate([0,0,-1]) cylinder(d=(output?10:8)+1,h=5);
        for(a=[45:90:315]) translate([19*cos(a),19*sin(a),-1]) cylinder(d=3.4,h=5);
    }
}
module bearing_cup(output=false) {
    id=output?10:8; od=output?26:22; w=output?8:7;
    difference() {
        cylinder(d=48,h=10);
        translate([0,0,-1]) cylinder(d=id+1,h=12);
        // Installed against a metal plate; lip retains far-side outer race.
        translate([0,0,-1]) cylinder(d=od+fit,h=w+1);
        for(a=[45:90:315]) translate([19*cos(a),19*sin(a),-1]) cylinder(d=3.4,h=12);
    }
}
module belt_gearbox() {
    color("lightgray") metal_plate();
    color("lightgray") translate([0,0,54]) metal_plate(true);
    for(x=[-C-12,C+35],y=[-35,35])
        translate([x,y,3]) aluminum_standoff();
    color("black") translate([-C-17.5,-17.5,-34]) cube([35,35,34]);
    translate([-C,0,14]) purchased_pulley(20,5);
    translate([0,0,14]) purchased_pulley(100,8);
    translate([-C,0,15]) purchased_belt();
    // 1 mm gap between first-stage hub end26 and second-stage start27.
    translate([0,0,27]) purchased_pulley(20,8);
    translate([C,0,27]) purchased_pulley(100,10);
    translate([0,0,28]) purchased_belt();
    for(x=[0,C]) {
        id=x==0?8:10; od=x==0?22:26; w=x==0?7:8;
        translate([x,0,3]) bearing(id,od,w);
        translate([x,0,54-w]) bearing(id,od,w);
        color("teal") translate([x,0,3]) bearing_cup(x==C);
        color("teal") translate([x,0,54]) rotate([180,0,0]) bearing_cup(x==C);
        color("silver") translate([x,0,0]) cylinder(d=id,h=x==0?60:89);
    }
    for(y=[-8,8]) color("silver") translate([C-25,y,57])
        difference() { cylinder(d=6,h=20); translate([0,0,-1]) cylinder(d=3.4,h=22); }
}
module light_base() {
    difference() {
        translate([-55,-40,0]) cube([110,80,6]);
        translate([0,0,-1]) cylinder(d=7,h=8);
        translate([0,0,1]) cylinder(d=11.1/cos(30)+fit,h=6,$fn=6);
        for(x=[-40,40],y=[-28,28]) translate([x,y,-1]) cylinder(d=4.5,h=8);
    }
}
module light_encoder_support() {
    difference() {
        union() {
            translate([-32,-12,0]) cube([44,24,3]);
            translate([-32,-12,-18]) cube([4,24,21]);
            translate([-32,-12,-18]) cube([12,24,3]);
        }
        translate([0,0,-1]) cylinder(d=8,h=5);
        for(x=[-8,8],y=[-8,8]) translate([x,y,-1]) cylinder(d=2.4,h=5);
        for(y=[-8,8]) translate([-25,y,-19]) cylinder(d=3.4,h=5);
    }
}
module metal_el_support() {
    color("silver") difference() {
        union() {
            translate([-40,-30,0]) cube([80,60,3]);
            translate([-C*2-21,26,0]) cube([2*C+66,3,104]);
        }
        for(x=[-15.556,15.556],y=[-15.556,15.556])
            translate([x,y,-1]) cylinder(d=4.5,h=5);
        // Four housing screws, EL output center z60.
        for(x=[-2*C-12,35],z=[25,95]) translate([x,25,z])
            rotate([-90,0,0]) cylinder(d=4.5,h=6);
        translate([-2*C-19,25,41]) cube([38,6,38]); // EL motor face clearance
    }
}
module metal_tray() {
    difference() {
        translate([-2*C-21,-43,0]) cube([2*C+66,86,3]);
        for(x=[-40,40],y=[-28,28]) translate([x,y,-1]) cylinder(d=4.5,h=5);
        for(x=[-2*C-12,35],y=[-35,35]) translate([x,y,-1]) cylinder(d=4.5,h=5);
    }
}
module belt_station() {
    light_base();
    // Motor is remote from tripod center; plate overhang has METAL support tray.
    color("silver") translate([0,0,6]) metal_tray();
    for(x=[-2*C-12,35],y=[-35,35]) translate([x,y,9]) aluminum_standoff(36);
    translate([-C,0,45]) belt_gearbox();
    rotate([0,0,azimuth]) translate([0,0,105]) output_flange();
    rotate([0,0,azimuth]) translate([0,0,126]) magnet_holder();
    translate([0,0,140]) light_encoder_support();
    rotate([0,0,azimuth]) {
        translate([0,0,123]) metal_el_support();
        translate([-C,26,183]) rotate([90,0,0]) belt_gearbox();
        translate([0,-34,183]) rotate([90,0,0]) output_flange();
        translate([0,-55,183]) rotate([90,0,0]) magnet_holder();
        translate([0,-69,183]) rotate([90,0,0]) light_encoder_support();
        translate([0,-40,183]) rotate([90,0,0]) rotate([0,0,-elevation]) {
            saddle(20);
            translate([reflector_gap(vhf_mhz)/2,35,24]) rotate([0,-90,0]) antennas();
        }
    }
}
if(belt_part=="assembly") belt_station();
else if(belt_part=="gearbox") belt_gearbox();
else if(belt_part=="base") light_base();
else if(belt_part=="keeper608") belt_keeper();
else if(belt_part=="keeper6000") belt_keeper(true);
else if(belt_part=="encoder_support") light_encoder_support();
else if(belt_part=="cup608") bearing_cup();
else if(belt_part=="cup6000") bearing_cup(true);
else if(belt_part=="front_plate_dxf") projection(cut=true) translate([0,0,-1]) metal_plate();
else if(belt_part=="rear_plate_dxf") projection(cut=true) translate([0,0,-1]) metal_plate(true);
else if(belt_part=="tray_dxf") projection(cut=true) translate([0,0,-1]) metal_tray();
else assert(false,"Unknown belt_part");
