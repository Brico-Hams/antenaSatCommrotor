// Illustration scenes for docs/assembly (BricoHams). Render with scripts/make_assembly_figs.py.
// Reuses the real modules; the explosions only add z offsets. Not a manufacturing drawing.
include <parameters.scad>
include <bricohams_logo.scad>
include <gears.scad>
include <mechanical.scad>
include <antenna.scad>
scene = "none";
X = 1; // explosion factor

module gb_parts_sheet() {
    color("gold") translate([-130,0,0]) sun(1);
    color("goldenrod") translate([-75,0,0]) planet();
    color("orange") translate([0,0,0]) internal_ring();
    color("teal") translate([140,0,0]) carrier(1);
    color("darkslategray") translate([0,-150,0]) motor_plate();
    color("gray") translate([-110,-150,0]) bearing_plate();
    color("gray") translate([110,-150,0]) bearing_plate(true);
}
module stage_exploded() {
    // one planetary stage, bottom to top
    color("darkslategray") translate([0,0,-40*X]) motor_plate();
    color("gold") translate([0,0,4+0*X]) sun(1);
    color("orange") translate([0,0,9+25*X]) internal_ring();
    for(a=[0:120:240]) translate([planet_radius*cos(a),planet_radius*sin(a),12+12*X])
        rotate([0,0,a+180-180/planet_teeth]) color("goldenrod") planet();
    for(a=[0:120:240]) color("silver") translate([planet_radius*cos(a),planet_radius*sin(a),10+12*X])
        cylinder(d=4,h=23);
    color("teal") translate([0,0,26+60*X]) carrier(1);
}
module az_stack() {
    color("gray") translate([0,0,-70*X]) tripod_base();
    for(a=[30:60:330]) color("gray") translate([58.5*cos(a),58.5*sin(a),12-40*X]) spacer(38);
    translate([0,0,50]) gearbox();
    color("sienna") translate([0,0,124+60*X]) output_flange();
}
module el_axis() {
    color("gray") translate([0,0,0]) elevation_bracket();
    translate([0,22,100]) rotate([90,0,0]) gearbox();
    color("sienna") translate([0,-102-30*X,100]) rotate([90,0,0]) output_flange();
    color("orange") translate([0,-140-60*X,100]) rotate([90,0,0]) rotate([0,0,-45]) saddle();
}
module antenna_parts() {
    color("orange") antenna_hub();
    color("orange") translate([90,0,0]) band_bridge();
    color("orange") translate([-90,0,0]) arm_socket();
}
module antenna_band() { translate([0,0,0]) band_antenna(vhf_mhz); }
module boxes() {
    color("steelblue") translate([0,0,0]) radio_cradle();
    color("seagreen") translate([100,0,0]) enclosure();
    color("seagreen") translate([100,0,60*X]) enclosure(true);
    color("seagreen") translate([250,0,0]) enclosure(diplexor=true);
    color("seagreen") translate([250,0,50*X]) enclosure(true,true);
}
module station_full() {
    translate([0,0,0]) {
        color("gray") tripod_base();
        for(a=[30:60:330]) color("gray") translate([58.5*cos(a),58.5*sin(a),12]) spacer(38);
        translate([0,0,50]) gearbox();
        translate([0,0,50]) rotate([0,0,0]) {
            translate([0,0,124]) color("sienna") output_flange();
            translate([0,0,142]) color("gray") elevation_bracket();
            translate([0,22,226]) rotate([90,0,0]) gearbox();
            translate([0,-102,226]) rotate([90,0,0]) color("sienna") output_flange();
            translate([0,-108,226]) rotate([90,0,0]) rotate([0,0,-45]) {
                color("orange") saddle();
                translate([reflector_gap(vhf_mhz)/2,35,24]) rotate([0,-90,0]) antennas();
            }
        }
        translate([85,-65,0]) color("steelblue") radio_cradle();
    }
}
module logo_demo() { color("orange") linear_extrude(2) bh_lockup_2d(100); }

if(scene=="parts_sheet") gb_parts_sheet();
else if(scene=="stage_exploded") stage_exploded();
else if(scene=="gearbox") gearbox();
else if(scene=="az_stack") az_stack();
else if(scene=="el_axis") el_axis();
else if(scene=="antenna_parts") antenna_parts();
else if(scene=="antenna_band") antenna_band();
else if(scene=="boxes") boxes();
else if(scene=="station") station_full();
