include <parameters.scad>
include <gears.scad>
include <mechanical.scad>
include <antenna.scad>

module station() {
    color("gray") tripod_base();
    for(a=[30:60:330]) color("gray")
        translate([58.5*cos(a),58.5*sin(a),12]) spacer(38);
    translate([0,0,50]) gearbox();
    translate([0,0,209]) sensor_bracket(); // fixed to AZ housing, not AZ carrier
    translate([0,0,50]) rotate([0,0,azimuth]) {
        translate([0,0,124]) output_flange();
        translate([0,0,142]) elevation_bracket();
        translate([0,0,145]) magnet_holder();
        translate([0,22,226]) rotate([90,0,0]) gearbox();
        translate([0,-102,226]) rotate([90,0,0]) output_flange();
        translate([0,-123,226]) rotate([90,0,0]) magnet_holder();
        translate([0,-137,226]) rotate([90,0,0]) sensor_bracket();
        translate([0,-108,226]) rotate([90,0,0]) rotate([0,0,-elevation]) {
            saddle();
            translate([reflector_gap(vhf_mhz)/2,35,24]) rotate([0,-90,0]) antennas();
        }
    }
    // Radio and RF/electronics boxes stay on the stationary base or tripod tray.
    translate([85,-65,0]) radio_cradle();
    translate([-210,-35,0]) enclosure();
    translate([-210,50,0]) enclosure(diplexor=true);
}

if(part=="assembly") station();
else if(part=="gearbox") gearbox();
else if(part=="sun1") sun(1);
else if(part=="sun2") sun(2);
else if(part=="planet") planet();
else if(part=="ring") internal_ring();
else if(part=="carrier1") carrier(1);
else if(part=="carrier2") carrier(2);
else if(part=="motor_plate") motor_plate();
else if(part=="intermediate_plate") bearing_plate();
else if(part=="output_plate") bearing_plate(true);
else if(part=="keeper608") bearing_keeper();
else if(part=="keeper6000") bearing_keeper(true);
else if(part=="spacer15") spacer(15);
else if(part=="spacer6") spacer(6);
else if(part=="spacer9") spacer(9);
else if(part=="spacer38") spacer(38);
else if(part=="tripod_base") tripod_base();
else if(part=="output_flange") output_flange();
else if(part=="elevation_bracket") elevation_bracket();
else if(part=="saddle20") saddle(20);
else if(part=="saddle25") saddle(25);
else if(part=="saddle32") saddle(32);
else if(part=="flat_adapter") flat_adapter();
else if(part=="limit_bracket") limit_bracket();
else if(part=="magnet_holder") magnet_holder();
else if(part=="sensor_bracket") sensor_bracket();
else if(part=="radio_cradle") radio_cradle();
else if(part=="enclosure") enclosure();
else if(part=="enclosure_lid") enclosure(true);
else if(part=="diplexor_box") enclosure(diplexor=true);
else if(part=="diplexor_lid") enclosure(true,true);
else if(part=="antenna_hub") antenna_hub();
else if(part=="band_bridge") band_bridge();
else if(part=="arm_socket") arm_socket();
else if(part=="antenna145") band_antenna(vhf_mhz);
else if(part=="antenna435") band_antenna(uhf_mhz);
else if(part=="coupon") coupon();
else assert(false,str("Unknown part: ",part));
