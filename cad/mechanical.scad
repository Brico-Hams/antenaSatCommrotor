planet_radius=pitch_radius(sun_teeth)+pitch_radius(planet_teeth);
module bolt_pattern(d=3.4,h=20,r=58.5) {
    for(a=[30:60:330]) translate([r*cos(a),r*sin(a),-1]) cylinder(d=d,h=h);
}
module carrier(stage=1) {
    bore=stage==1?8:10;
    union() {
        difference() {
            cylinder(r=46,h=6);
            translate([0,0,-1]) cylinder(d=bore+fit,h=8);
            for(a=[0:120:240]) translate([planet_radius*cos(a),planet_radius*sin(a),-1])
                cylinder(d=4+fit,h=8);
            // Lightening windows outside shaft hub and pin bosses.
            for(a=[60:120:300]) rotate([0,0,a]) translate([25,0,-1])
                cylinder(d=20,h=8);
        }
        translate([0,0,6]) pinned_hub(bore);
    }
}
module bearing_plate(output=false) {
    // 608: 8 x 22 x 7; 6000: 10 x 26 x 8. Open bearing seats:
    // retain with separate screwed keeper, never rely on a printed press fit.
    od=output?26:22; id=output?10:8; width=output?8:7;
    difference() {
        cylinder(r=ring_outer_radius,h=output?10:9);
        translate([0,0,-1]) cylinder(d=id+1,h=12);
        translate([0,0,1]) cylinder(d=od+fit,h=11);
        bolt_pattern(h=12);
        if(output) for(y=[-10,10]) translate([-55,y,-1]) cylinder(d=3.4,h=12);
        for(a=[0:90:270]) translate([19*cos(a),19*sin(a),-1]) cylinder(d=3.4,h=12);
        for(a=[45:90:315]) rotate([0,0,a]) translate([39,0,-1]) cylinder(d=22,h=12);
    }
}
module bearing_keeper(output=false) {
    difference() {
        cylinder(d=48,h=3);
        translate([0,0,-1]) cylinder(d=(output?10:8)+1,h=5);
        for(a=[0:90:270]) translate([19*cos(a),19*sin(a),-1]) cylinder(d=3.4,h=5);
    }
}
module motor_plate() {
    difference() {
        cylinder(r=ring_outer_radius,h=8);
        translate([0,0,-1]) cylinder(d=23,h=10);
        for(x=[-1,1],y=[-1,1]) translate([x*motor_hole_pitch/2,y*motor_hole_pitch/2,-1])
            cylinder(d=3.4,h=10);
        bolt_pattern(h=10);
        for(a=[45:90:315]) rotate([0,0,a]) translate([39,0,-1]) cylinder(d=22,h=10);
    }
}
module spacer(length=15) {
    difference() { cylinder(d=9,h=length); translate([0,0,-1]) cylinder(d=3.4,h=length+2); }
}
module bearing(id,od,w) {
    color("silver") difference() { cylinder(d=od,h=w); translate([0,0,-1]) cylinder(d=id,h=w+2); }
}
module gearbox() {
    assert(ring_teeth==sun_teeth+2*planet_teeth,"Pitch mesh condition");
    assert((sun_teeth+ring_teeth)%planet_count==0,"Planet assembly closure");
    color("darkslategray") motor_plate();
    color("orange") translate([0,0,9]) internal_ring();
    color("orange") translate([0,0,59]) internal_ring();
    color("gold") translate([0,0,4]) sun(1);
    color("gold") translate([0,0,54]) sun(2);
    for(stage=[1,2]) {
        z=stage==1?12:62;
        for(a=[0:120:240]) {
            translate([planet_radius*cos(a),planet_radius*sin(a),z])
                rotate([0,0,a+180-180/planet_teeth]) color("goldenrod") planet();
            color("silver") translate([planet_radius*cos(a),planet_radius*sin(a),z-2])
                cylinder(d=4,h=23);
            // OD6/ID4 metal bushes, exactly gear width. Pin bolts need
            // ground shoulders and shims; ordinary threaded screws are not bearings.
            translate([planet_radius*cos(a),planet_radius*sin(a),z])
                bearing(4,6,12);
        }
    }
    color("teal") translate([0,0,26]) carrier(1);
    color("teal") translate([0,0,76]) carrier(2);
    color("gray") translate([0,0,41]) bearing_plate();
    color("gray") translate([0,0,91]) bearing_plate(true);
    color("gray") translate([0,0,110]) bearing_plate(true);
    translate([0,0,42]) bearing(8,22,7);
    translate([0,0,92]) bearing(10,26,8);
    translate([0,0,111]) bearing(10,26,8);
    color("gray") translate([0,0,50]) bearing_keeper();
    color("gray") translate([0,0,101]) bearing_keeper(true);
    color("gray") translate([0,0,120]) bearing_keeper(true);
    color("silver") translate([0,0,26]) cylinder(d=8,h=36);
    color("silver") translate([0,0,76]) cylinder(d=10,h=77);
    for(a=[30:60:330]) {
        color("gray") translate([58.5*cos(a),58.5*sin(a),26]) spacer(15);
        color("gray") translate([58.5*cos(a),58.5*sin(a),50]) spacer(9);
        color("gray") translate([58.5*cos(a),58.5*sin(a),76]) spacer(15);
        color("gray") translate([58.5*cos(a),58.5*sin(a),101]) spacer(9);
    }
    color("black") translate([-motor_face/2,-motor_face/2,-34])
        cube([motor_face,motor_face,34]);
}
module tripod_base() {
    difference() {
        translate([-70,-70,0]) cube([140,140,12]);
        translate([0,0,-1]) cylinder(d=7,h=14);
        // Captured REAL 1/4-20 UNC nut: verify 11.1 AF / 5.6 high nut.
        translate([0,0,6]) cylinder(d=11.1/cos(30)+fit,h=7,$fn=6);
        bolt_pattern(h=14);
        for(x=[-58,58]) translate([x,-54,-1]) cylinder(d=4.5,h=14);
        // Recess nonstructural fields from underside; preserve 3 mm skin,
        // central nut boss and continuous webs to all six housing tie rods.
        translate([0,0,-1]) linear_extrude(height=10) difference() {
            translate([-66,-66]) square([132,132]);
            circle(r=19);
            for(a=[30:60:330]) rotate(a) translate([0,-7]) square([74,14]);
            for(x=[-58,58]) translate([x,-54]) circle(r=9);
        }
    }
}
module output_flange() {
    difference() {
        union() { cylinder(d=60,h=6); translate([0,0,6]) pinned_hub(10,12); }
        translate([0,0,-1]) cylinder(d=10+fit,h=22);
        for(a=[45:90:315]) translate([22*cos(a),22*sin(a),-1]) cylinder(d=4.5,h=8);
    }
}
module elevation_bracket() {
    // Clear motor opening; six tie rods join EL motor plate to cheek.
    difference() {
        union() {
            translate([-42,-32,0]) cube([84,64,8]);
            translate([-66,22,0]) cube([132,10,150]);
        }
        for(x=[-15.556,15.556],y=[-15.556,15.556])
            translate([x,y,-1]) cylinder(d=4.5,h=10);
        translate([-19,21,65]) cube([38,12,38]);
        translate([0,0,-1]) cylinder(d=22,h=10);
        for(a=[30:60:330]) translate([58.5*cos(a),21,84+58.5*sin(a)])
            rotate([-90,0,0]) cylinder(d=3.4,h=12);
    }
}
module saddle(diameter=boom_diameter) {
    assert(diameter==20||diameter==25||diameter==32);
    difference() {
        union() {
            translate([-35,-25,0]) cube([70,85,8]);
            translate([-35,10,0]) cube([70,50,24]);
        }
        translate([-36,35,24]) rotate([0,90,0]) cylinder(d=diameter+fit,h=72);
        translate([0,0,-1]) cylinder(d=22,h=26); // output encoder clearance
        for(x=[-22,22],y=[-1,1]) translate([x,35+y*(diameter/2+5),-1])
            cylinder(d=5.5,h=26);
        for(x=[-15.556,15.556],y=[-15.556,15.556])
            translate([x,y,-1]) cylinder(d=4.5,h=26);
    }
}
module flat_adapter() {
    difference() {
        translate([-35,-25,0]) cube([70,50,8]);
        for(x=[-15.556,15.556],y=[-15.556,15.556])
            translate([x,y,-1]) cylinder(d=4.5,h=10);
        for(x=[-27,27],y=[-18,18]) translate([x,y,-1]) cylinder(d=5.5,h=10);
    }
}
module limit_bracket() {
    difference() {
        union() { cube([34,22,4]); cube([34,4,25]); }
        for(x=[7,27]) translate([x,13,-1]) cylinder(d=3.4,h=6);
        for(x=[8,26]) translate([x,-1,16]) rotate([-90,0,0]) cylinder(d=2.4,h=6);
    }
}
module magnet_holder() {
    // Shaft end cross-pin locks hub; glued 6x2 diametrically magnetized disc.
    difference() {
        cylinder(d=20,h=12);
        translate([0,0,-1]) cylinder(d=10+fit,h=9);
        translate([0,0,10]) cylinder(d=6+fit,h=3);
        translate([-11,0,4]) rotate([0,90,0]) cylinder(d=3.2,h=22);
    }
}
module sensor_bracket() {
    difference() {
        union() {
            translate([-66,-12,0]) cube([78,24,3]);
            translate([-66,-16,-39]) cube([4,32,42]);
            translate([-66,-16,-39]) cube([16,32,3]);
        }
        for(x=[-8,8],y=[-8,8]) translate([x,y,-1]) cylinder(d=2.4,h=5);
        translate([0,0,-1]) cylinder(d=8,h=5);
        for(y=[-10,10]) translate([-55,y,-40]) cylinder(d=3.4,h=5);
    }
}
module radio_cradle() {
    w=radio_width+2*radio_clearance; d=radio_depth+2*radio_clearance;
    difference() {
        union() {
            cube([w+8,d+8,5]);
            cube([4,d+8,45]); translate([w+4,0,0]) cube([4,d+8,45]);
            cube([w+8,4,65]);
        }
        for(x=[12,w-4]) translate([x,18,-1]) cylinder(d=4.5,h=7);
        for(x=[-1,w+3]) translate([x,14,28]) cube([6,20,5]); // webbing
    }
    // BricoHams logo raised 0.6 mm on the outer face of the back wall (y=0), 0.05 mm overlap.
    lw=min(50,w-6);
    translate([(w+8-lw)/2,0.05,40]) rotate([90,0,0]) linear_extrude(height=0.65) bh_lockup_2d(lw);
}
module enclosure(lid=false,diplexor=false) {
    w=diplexor?80:130; d=70; h=diplexor?35:45;
    if(lid) union() {
      difference() {
        cube([w,d,3]);
        for(x=[5,w-5],y=[5,d-5]) translate([x,y,-1]) cylinder(d=3.4,h=5);
        // Interior-only pockets preserve a continuous 1.6 mm roof and ribs;
        // RF shielding remains the independent metal liner.
        for(x=[10,w/2+3]) translate([x,10,-1])
            cube([w/2-16,d-20,2.4]);
      }
      // BricoHams logo, raised 0.6 mm on the top face (0.05 mm overlap joins every island to the lid).
      lw=diplexor?50:60;
      translate([(w-lw)/2,(d-lw*bh_lockup_aspect)/2,2.95]) linear_extrude(height=0.65) bh_lockup_2d(lw);
    } else difference() {
        union() {
            difference() { cube([w,d,h]); translate([3,3,3]) cube([w-6,d-6,h]); }
            for(x=[5,w-5],y=[5,d-5]) translate([x,y,0]) cylinder(d=8,h=h);
            translate([0,-10,0]) cube([w,10,4]);
        }
        for(x=[5,w-5],y=[5,d-5]) translate([x,y,3]) cylinder(d=2.5,h=h);
        for(x=[12,w-12]) translate([x,-5,-1]) cylinder(d=4.5,h=6);
        for(x=[w/3,2*w/3]) translate([x,-1,h/2]) rotate([-90,0,0]) cylinder(d=10,h=5);
    }
}
module coupon() {
    difference() {
        cube([70,30,10]);
        for(i=[0:3]) translate([10+16*i,15,-1]) cylinder(d=8+0.1*i,h=12);
    }
}
