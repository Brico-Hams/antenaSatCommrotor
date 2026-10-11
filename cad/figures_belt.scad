// BricoHams illustration scenes for the CURRENT BASE (belt station).
// 'use' imports modules only (no top-level rendering of belt_station.scad).
include <parameters.scad>
use <mechanical.scad>
use <belt_station.scad>
belt_pitch=2; small_r=20*belt_pitch/(2*PI); large_r=100*belt_pitch/(2*PI);
C=solve_center(large_r-small_r+0.1,100);
scene="none";
E_=1;
module b_parts() {
    color("lightgray") translate([0,0,0]) light_base();
    color("teal") translate([-80,-100,0]) bearing_cup();
    color("teal") translate([-20,-100,0]) bearing_cup(true);
    color("gray") translate([40,-100,0]) belt_keeper();
    color("gray") translate([100,-100,0]) belt_keeper(true);
    color("gray") translate([-60,-160,0]) light_encoder_support();
    color("sienna") translate([30,-160,0]) output_flange();
    color("orange") translate([110,-160,0]) magnet_holder();
    color("orange") translate([-60,60,0]) saddle(20);
}
module b_gearbox_x() {
    k=E_;
    color("lightgray") translate([0,0,-40*k]) metal_plate();
    for(x=[-C-12,C+35],y=[-35,35]) translate([x,y,3-20*k]) aluminum_standoff();
    color("black") translate([-C-17.5,-17.5,-34-60*k]) cube([35,35,34]);
    translate([-C,0,14]) purchased_pulley(20,5);
    translate([0,0,14+10*k]) purchased_pulley(100,8);
    translate([-C,0,15]) purchased_belt();
    translate([0,0,27+25*k]) purchased_pulley(20,8);
    translate([C,0,27+25*k]) purchased_pulley(100,10);
    translate([0,0,28+25*k]) purchased_belt();
    for(x=[0,C]) {
        id=x==0?8:10; od=x==0?22:26; w=x==0?7:8;
        translate([x,0,3-12*k]) bearing(id,od,w);
        color("teal") translate([x,0,3-4*k]) bearing_cup(x==C);
        translate([x,0,54-w+45*k]) bearing(id,od,w);
        color("teal") translate([x,0,54+55*k]) rotate([180,0,0]) bearing_cup(x==C);
        color("silver") translate([x,0,0]) cylinder(d=id,h=x==0?60:89);
    }
    color("lightgray") translate([0,0,54+75*k]) metal_plate(true);
}
module b_az() {
    color("lightgray") translate([0,0,-30]) light_base();
    color("silver") translate([0,0,6]) metal_tray();
    for(x=[-2*C-12,35],y=[-35,35]) translate([x,y,9]) aluminum_standoff(36);
    translate([-C,0,45+25]) belt_gearbox();
    color("sienna") translate([0,0,105+55]) output_flange();
    color("orange") translate([0,0,126+75]) magnet_holder();
    color("gray") translate([0,0,140+95]) light_encoder_support();
}
module b_station() { belt_station(); }
module b_rotor() {
    // belt_station() without the antenna: same transforms, saddle + 20 mm boom stub only
    light_base();
    color("silver") translate([0,0,6]) metal_tray();
    for(x=[-2*C-12,35],y=[-35,35]) translate([x,y,9]) aluminum_standoff(36);
    translate([-C,0,45]) belt_gearbox();
    color("sienna") translate([0,0,105]) output_flange();
    color("orange") translate([0,0,126]) magnet_holder();
    color("gray") translate([0,0,140]) light_encoder_support();
    color("silver") translate([0,0,123]) metal_el_support();
    translate([-C,26,183]) rotate([90,0,0]) belt_gearbox();
    color("sienna") translate([0,-34,183]) rotate([90,0,0]) output_flange();
    color("orange") translate([0,-55,183]) rotate([90,0,0]) magnet_holder();
    color("gray") translate([0,-69,183]) rotate([90,0,0]) light_encoder_support();
    translate([0,-40,183]) rotate([90,0,0]) rotate([0,0,-45]) { color("orange") saddle(20);
        translate([0,35,24]) rotate([0,90,0]) color("gray") translate([0,0,-60]) cylinder(d=20,h=240); }
}
if(scene=="b_parts") b_parts();
else if(scene=="b_gearbox_x") b_gearbox_x();
else if(scene=="b_az") b_az();
else if(scene=="b_station") b_station();
else if(scene=="b_gearbox") belt_gearbox();
else if(scene=="b_rotor") b_rotor();
