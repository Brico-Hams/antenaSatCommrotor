// POL third axis concept; mm. Imported BASE interfaces/helpers are unmodified.
include <parameters.scad>
use <mechanical.scad>
use <belt_station.scad>

// Share the BASE purchased-pulley and open-belt envelopes.
belt_pitch = 2;
small_teeth = 20;
large_teeth = 100;
belt_length = 252;
small_r = small_teeth * belt_pitch / (2 * PI);
large_r = large_teeth * belt_pitch / (2 * PI);
C = solve_center(large_r - small_r + 0.1, belt_length);

// Select with -D pol_part=N: 0 assembly, 1 frame, 2 carrier, 3 retainer,
// 4 limit cam, 5 limit bracket, 6 BASE saddle, 7 motor DXF, 8 cheek DXF,
// 9 SMA/coax interface DXF, 10 generic power-harness strain-relief plate.
pol_part = 0;
pol_frame_thickness = 8;
pol_bearing_span = 48;
pol_bearing_x = pol_bearing_span / 2;
pol_bearing_clearance = 0.25;
pol_axis_y = 35;
pol_axis_z = 24;
pol_clamp_x = 64;
pol_clamp_y = 0;
pol_clamp_z = 0;
pol_mount_pattern = 15.55635; // Existing saddle/output-flange square half-pitch.
pol_sma_panel_hole_diameter = 6.5;
pol_sma_panel_thickness = 3;
pol_coax_strain_hole_diameter = 3.4;
pol_coax_strain_hole_spacing = 10;
pol_coax_plate_width = 30;
pol_coax_plate_height = 22;
pol_coax_mount_hole_spacing = 24;
pol_coax_interface_y = 38;
assert(abs(pol_clamp_y+35-pol_axis_y)<0.001,
       "Original 20 mm BASE saddle bore must align with POL shaft on Y");
assert(abs(pol_clamp_z+24-pol_axis_z)<0.001,
       "Original 20 mm BASE saddle bore must align with POL shaft on Z");

module pol_slot_2d(diameter,travel=3) {
    hull()
        for (x=[-travel/2,travel/2])
            translate([x,0]) circle(d=diameter);
}

module pol_cheek_profile() {
    difference() {
        polygon([[-10,8],[80,8],[80,62],[70,72],[0,72],[-10,62]]);
        translate([pol_axis_y,pol_axis_z])
            circle(d=22+pol_bearing_clearance);
        for (u=[pol_axis_y-12,pol_axis_y+12],v=[pol_axis_z-12,pol_axis_z+12])
            translate([u,v]) circle(d=3.4);
        for (u=[0,70],v=[14,64])
            translate([u,v]) circle(d=4.5);
        for (u=[-1,71])
            translate([u,pol_axis_z]) circle(d=4.2);
        for (u=[10,60],v=[12,30])
            translate([u,v]) circle(d=4.5);
    }
}

module pol_cheek(x0) {
    translate([x0,0,0])
        rotate([90,0,90])
            linear_extrude(height=pol_frame_thickness) pol_cheek_profile();
}

module pol_frame() {
    difference() {
        union() {
            translate([-35,-25,0]) cube([70,85,8]);
            pol_cheek(-28);
            pol_cheek(20);
        }
        translate([0,0,-1]) cylinder(d=22,h=10);
        for (x=[-pol_mount_pattern,pol_mount_pattern],
             y=[-pol_mount_pattern,pol_mount_pattern])
            translate([x,y,-1]) cylinder(d=4.5,h=10);
        for (x=[-pol_coax_mount_hole_spacing/2,pol_coax_mount_hole_spacing/2])
            translate([x,pol_coax_interface_y,-1]) cylinder(d=3.4,h=10);
        for (u=[-1,71])
            translate([-31,u,pol_axis_z])
                rotate([0,90,0]) cylinder(d=4.2,h=62,$fn=24);
    }
}

module pol_rotor_carrier() {
    difference() {
        union() {
            translate([58,pol_axis_y,pol_axis_z])
                rotate([0,90,0]) cylinder(d=26,h=10);
            for (side=[-1,1])
                translate([58,pol_axis_y+side*13,pol_axis_z])
                    rotate([0,90,0]) cylinder(d=10,h=10);
            for (sx=[-1,1],sy=[-1,1]) {
                pol_carrier_strut(
                    [63,pol_axis_y,pol_axis_z],
                    [pol_clamp_x+sx*pol_mount_pattern,
                     pol_clamp_y+sy*pol_mount_pattern,pol_clamp_z],10);
                translate([pol_clamp_x+sx*pol_mount_pattern,
                           pol_clamp_y+sy*pol_mount_pattern,pol_clamp_z-8])
                    cylinder(d=13,h=8);
            }
        }
        translate([57,pol_axis_y,pol_axis_z])
            rotate([0,90,0]) cylinder(d=8.4,h=12);
        for (sx=[-1,1],sy=[-1,1])
            translate([pol_clamp_x+sx*pol_mount_pattern,
                       pol_clamp_y+sy*pol_mount_pattern,pol_clamp_z-9])
                cylinder(d=4.5,h=10);
        translate([63,pol_axis_y+3.8,pol_axis_z])
            rotate([-90,0,0]) cylinder(d=3.4,h=14.2,$fn=24);
        translate([63,pol_axis_y-3.8,pol_axis_z])
            rotate([90,0,0]) cylinder(d=3.4,h=14.2,$fn=24);
    }
}

module pol_carrier_strut(start,end,width=10) {
    direction=end-start;
    length=norm(direction);
    axis=[-direction[1],direction[0],0];
    translate(start)
        rotate(a=acos(direction[2]/length),v=axis)
            cylinder(d=width,h=length);
}

module pol_bearing_retainer() {
    difference() {
        intersection() {
            cylinder(d=44,h=3);
            translate([-50,-15.5,-1]) cube([100,70,5]);
        }
        translate([0,0,-1]) cylinder(d=18.5,h=5);
        for (x=[-12,12],y=[-12,12])
            translate([x,y,-1]) cylinder(d=3.4,h=5);
    }
}

module pol_limit_cam() {
    difference() {
        union() {
            rotate([0,90,0]) cylinder(d=24,h=6);
            translate([0,-4,0]) cube([6,8,34]);
            translate([0,-7,-10]) cube([6,6,8]);
            translate([0,1,-10]) cube([6,6,8]);
        }
        translate([-1,0,0]) rotate([0,90,0]) cylinder(d=8.4,h=8);
        translate([-1,-1,-15]) cube([8,2,15]);
        translate([2,-9,-6]) rotate([-90,0,0]) cylinder(d=3.4,h=18,$fn=24);
    }
}

module pol_motor_plate_2d() {
    difference() {
        translate([-72,-45]) square([117,90]);
        // Clearance over the 608 retainer, centred on the POL shaft.
        translate([-C,0]) circle(d=50);
        circle(d=23); // NEMA14 pilot; confirm selected motor drawing.
        for (x=[-13,13],y=[-13,13])
            translate([x,y]) pol_slot_2d(3.4,3);
        for (x=[-48.55635,-66.55635],y=[-25,25])
            translate([x,y]) circle(d=4.5);
    }
}

module pol_motor_plate_3d() {
    translate([34,pol_axis_y,pol_axis_z-C])
        rotate([0,90,0]) linear_extrude(height=3) pol_motor_plate_2d();
}

module pol_hollow_shaft() {
    difference() {
        translate([-32,pol_axis_y,pol_axis_z])
            rotate([0,90,0]) cylinder(d=8,h=96);
        translate([-33,pol_axis_y,pol_axis_z])
            rotate([0,90,0]) cylinder(d=5,h=98);
    }
}

module pol_limit_bracket() {
    difference() {
        union() {
            translate([12,-8,36]) cube([8,86,4]);
            for (u=[1,69]) {
                translate([12,u-9,16]) cube([8,18,22]);
                translate([12,u-9,8]) cube([8,18,8]);
            }
        }
        for (u=[1,69])
            translate([11,u,pol_axis_z]) rotate([0,90,0]) cylinder(d=4.2,h=10);
        for (u=[1,69],v=[-5,5])
            translate([14,u+v,15]) cylinder(d=3.4,h=25);
    }
}

module pol_cheek_plate_2d() {
    difference() {
        translate([-10,8]) square([90,64]);
        translate([pol_axis_y,pol_axis_z]) circle(d=18.5);
        for (u=[pol_axis_y-12,pol_axis_y+12],v=[pol_axis_z-12,pol_axis_z+12])
            translate([u,v]) circle(d=3.4);
        for (u=[0,70],v=[14,64])
            translate([u,v]) circle(d=4.5);
        for (u=[1,69],dy=[-5,5])
            translate([u+dy,15]) circle(d=3.4);
        for (u=[-1,71])
            translate([u,pol_axis_z]) circle(d=4.2,$fn=24);
    }
}

module pol_coax_interface_2d() {
    difference() {
        translate([-pol_coax_plate_width/2,-pol_coax_plate_height/2])
            square([pol_coax_plate_width,pol_coax_plate_height]);
        circle(d=pol_sma_panel_hole_diameter);
        for (x=[-pol_coax_mount_hole_spacing/2,pol_coax_mount_hole_spacing/2])
            translate([x,0]) circle(d=3.4);
        for (x=[-pol_coax_strain_hole_spacing/2,pol_coax_strain_hole_spacing/2])
            translate([x,6]) circle(d=pol_coax_strain_hole_diameter);
    }
}

module pol_coax_interface_plate() {
    translate([0,pol_coax_interface_y,8])
        linear_extrude(height=pol_sma_panel_thickness)
            pol_coax_interface_2d();
}

module pol_power_harness_strain_relief_2d() {
    difference() {
        square([48,84],center=true);
        for (x=[-19,19],y=[-38,38])
            translate([x,y]) circle(d=3.4);
        for (y=[-24,-8,8,24],x=[-6,6])
            translate([x,y]) circle(d=3.4);
    }
}

module pol_power_harness_strain_relief() {
    linear_extrude(height=3)
        pol_power_harness_strain_relief_2d();
}

module pol_assembly() {
    color("silver") translate([0,0,-18]) output_flange();
    color("lightgray") pol_frame();
    // Thin metal SMA bulkhead tab: the connector part itself remains unselected.
    color("silver") pol_coax_interface_plate();
    // Metal stop pins are tangent to the 34 mm cam at the nominal +/-90 deg stops.
    color("silver") for (u=[-1,71])
        translate([-30,u,pol_axis_z]) rotate([0,90,0]) cylinder(d=4,h=60,$fn=24);
    color("silver") for (y=[0,70],z=[14,64])
        translate([-20,y,z]) rotate([0,90,0]) cylinder(d=4,h=40);
    // Metal motor-plate standoffs land on the reinforced cheek fixing holes.
    color("silver") for (y=[10,60],z=[12,30])
        translate([31,y,z]) rotate([0,90,0]) difference() {
            cylinder(d=8,h=3);
            translate([0,0,-1]) cylinder(d=3.4,h=5);
        }
    // 3 mm metal cheek reinforcements from the paired DXF template.
    color("silver") for (x=[-31,28])
        translate([x,0,0]) rotate([90,0,90]) linear_extrude(height=3)
            pol_cheek_plate_2d();
    color("teal") translate([20,pol_axis_y,pol_axis_z]) rotate([0,90,0])
        pol_bearing_retainer();
    color("teal") translate([-20,pol_axis_y,pol_axis_z]) rotate([0,-90,0])
        pol_bearing_retainer();
    color("silver") for (x=[-pol_bearing_x,pol_bearing_x])
        translate([x-3.5,pol_axis_y,pol_axis_z]) rotate([0,90,0]) bearing(8,22,7);
    color("silver") pol_hollow_shaft();
    color("orange") translate([0,pol_axis_y,pol_axis_z]) pol_limit_cam();
    color("gold") pol_rotor_carrier();
    color("silver") translate([37,pol_axis_y,pol_axis_z]) rotate([0,90,0])
        purchased_pulley(100,8);
    color("silver") translate([37,pol_axis_y,pol_axis_z-C]) rotate([0,90,0])
        purchased_pulley(20,5);
    color("black") translate([38,pol_axis_y,pol_axis_z-C])
        rotate([0,90,0]) purchased_belt();
    color("gray") pol_motor_plate_3d();
    color("black") translate([2,pol_axis_y-17.5,pol_axis_z-C-17.5])
        cube([35,35,35]); // NEMA14 procurement envelope, not a selected motor.
    color("lightgray") pol_limit_bracket();
    // Actual existing BASE clamp interface, unchanged and removable.
    color("orange") translate([pol_clamp_x,pol_clamp_y,pol_clamp_z]) saddle(20);
}

if (pol_part==0) pol_assembly();
else if (pol_part==1) pol_frame();
else if (pol_part==2) pol_rotor_carrier();
else if (pol_part==3) pol_bearing_retainer();
else if (pol_part==4) pol_limit_cam();
else if (pol_part==5) pol_limit_bracket();
else if (pol_part==6) saddle(20);
else if (pol_part==7) pol_motor_plate_2d();
else if (pol_part==8) pol_cheek_plate_2d();
else if (pol_part==9) pol_coax_interface_2d();
else if (pol_part==10) pol_power_harness_strain_relief();
else assert(false,str("Unknown pol_part: ",pol_part));
