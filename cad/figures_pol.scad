// POL stage scenes. 'use' imports modules only.
include <parameters.scad>
use <mechanical.scad>
use <belt_station.scad>
use <polarization_station.scad>
belt_pitch=2; small_r=20*belt_pitch/(2*PI); large_r=100*belt_pitch/(2*PI);
C=solve_center(large_r-small_r+0.1,252);
pol_axis_y=35; pol_axis_z=24; pol_clamp_x=64; pol_clamp_y=0; pol_clamp_z=0;
scene="none";
module pol_x() {
    k=1;
    color("silver") translate([0,0,-18-50*k]) output_flange();
    color("lightgray") pol_frame();
    color("gold") translate([0,0,0]) pol_rotor_carrier();
    color("teal") translate([20+30*k,pol_axis_y,pol_axis_z]) rotate([0,90,0]) pol_bearing_retainer();
    color("teal") translate([-20-30*k,pol_axis_y,pol_axis_z]) rotate([0,-90,0]) pol_bearing_retainer();
    color("silver") pol_hollow_shaft();
    color("orange") translate([0,pol_axis_y,pol_axis_z]) pol_limit_cam();
    color("gray") translate([40*k,0,0]) pol_motor_plate_3d();
    color("black") translate([2+60*k,pol_axis_y-17.5,pol_axis_z-C-17.5]) cube([35,35,35]);
    color("orange") translate([pol_clamp_x,pol_clamp_y,pol_clamp_z+60*k]) saddle(20);
}
if(scene=="pol_asm") pol_assembly();
else if(scene=="pol_x") pol_x();
