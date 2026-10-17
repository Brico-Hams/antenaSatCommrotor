// Analytic seed geometry. Networks, fasteners and mast joints are not released.
include <antenna-options-parameters.scad>
ao_model = 0; // 0 EB-145, 1 QFH-145, 2 EB-435, 3 QFH-435
ao_part = "assembly";
$fn = 24;

module ao_path(points, diameter) {
    for(i=[0:len(points)-2])
        hull() {
            translate(points[i]) sphere(d=diameter);
            translate(points[i+1]) sphere(d=diameter);
        }
}

module ao_support_coupon() {
    difference() {
        union() {
            translate([-12,-8,0]) cube([24,16,4]);
            translate([0,0,8]) rotate([90,0,0]) cylinder(d=14,h=10,center=true);
        }
        translate([0,0,8]) rotate([90,0,0]) cylinder(d=4.4,h=20,center=true);
        for(x=[-8,8]) translate([x,0,-1]) cylinder(d=3.4,h=6);
    }
}

assert(ao_model>=0 && ao_model<len(ao_names),"Unknown antenna model");
if(ao_part=="support") ao_support_coupon();
else if(ao_part=="assembly") {
    color([0.65,0.72,0.75,0.35])
        cylinder(d=ao_mast_diameter,h=ao_heights[ao_model]);
    for(p=ao_paths[ao_model])
        color(p[0]==0 ? "#e8871e" : p[0]==1 ? "#326488" : "#628a7d")
            ao_path(p[2],p[1]);
}
else assert(false,"Unknown ao_part");
