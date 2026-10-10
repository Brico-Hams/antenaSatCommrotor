function wavelength(f) = 299792.458/f;
function driven_length(f) = wavelength(f)/2*0.92;
function reflector_length(f) = driven_length(f)*1.05;
function reflector_gap(f) = wavelength(f)*0.225;
module arm_socket() {
    // Two-piece bolted hinge lug. Metal rod bond uses external braid, not plastic.
    difference() {
        cube([32,16,12]);
        translate([8,-1,6]) rotate([-90,0,0]) cylinder(d=4.5,h=18);
        translate([14,-1,6]) rotate([-90,0,0]) cylinder(d=3.4,h=18);
        translate([18,8,6]) rotate([0,90,0]) cylinder(d=rod_diameter+fit,h=15);
        translate([26,8,-1]) cylinder(d=3.4,h=14);
    }
}
module antenna_hub() {
    difference() {
        union() {
            difference() {
                cylinder(d=64,h=12);
                for(a=[0:90:270]) rotate([0,0,a])
                    translate([28,-8.1,-1]) cube([20,16.2,14]);
            }
            for(a=[0:90:270]) rotate([0,0,a])
                for(y=[-12,8.1]) translate([28,y,0]) cube([16,3.9,12]);
        }
        translate([0,0,-1]) cylinder(d=20+fit,h=14);
        for(a=[0:90:270]) rotate([0,0,a]) {
            translate([12,0,6]) rotate([0,90,0]) cylinder(d=rod_diameter+fit,h=17);
            translate([36,-13,6]) rotate([-90,0,0]) cylinder(d=4.5,h=26);
            translate([42,-13,6]) rotate([-90,0,0]) cylinder(d=3.4,h=26);
            translate([23,0,-1]) cylinder(d=3.4,h=14);
        }
        for(a=[45:90:315]) rotate([0,0,a]) translate([24,0,-1]) cylinder(d=3.4,h=14);
    }
}
module rod_pair(total,z) {
    // Centre feed gap 24 mm is INCLUDED in tip-to-tip driven length.
    for(a=[0:90:270]) rotate([0,0,a]) {
        translate([12,0,z]) rotate([0,90,0]) color("silver") cylinder(d=rod_diameter,h=16);
        translate([36,0,z]) rotate([0,-antenna_arm_angle,0]) {
            translate([-8,-8,-6]) color("orange") arm_socket();
            translate([10,0,0]) rotate([0,90,0]) color("silver")
                cylinder(d=rod_diameter,h=total/2-46);
            if(total/2-46>400) translate([210,0,0]) rotate([0,90,0])
                color("silver") difference() {
                    cylinder(d=8,h=50);
                    translate([0,0,-1]) cylinder(d=rod_diameter,h=52);
                }
        }
    }
}
module band_antenna(f) {
    length=driven_length(f); gap=reflector_gap(f);
    color("gray") cylinder(d=20,h=gap+24);
    color("orange") antenna_hub();
    rod_pair(reflector_length(f),6);
    translate([0,0,gap]) color("orange") antenna_hub();
    rod_pair(length,gap+6);
}
module antennas() {
    // Independent booms per band; their mutual coupling remains unvalidated.
    center=reflector_gap(vhf_mhz)/2;
    translate([0,-40,0]) band_antenna(vhf_mhz);
    translate([0,40,center-reflector_gap(uhf_mhz)/2]) band_antenna(uhf_mhz);
    translate([0,0,center+50]) color("orange") band_bridge();
    color("gray") translate([0,0,center-52]) cylinder(d=20,h=175);
}
module band_bridge() {
    difference() {
        translate([-14,-55,-8]) cube([28,110,16]);
        for(y=[-40,0,40]) {
            translate([0,y,-9]) cylinder(d=20+fit,h=18);
            translate([-15,y,0]) rotate([0,90,0]) cylinder(d=4.5,h=30);
        }
    }
}
