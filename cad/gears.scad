function polar(r,a) = [r*cos(a),r*sin(a)];
function involute_angle(r,rb) =
    r <= rb ? 0 : sqrt(pow(r/rb,2)-1)*180/PI-acos(rb/r);
function pitch_radius(n) = n*gear_module/2;
function external_half(n,r) =
    (PI*gear_module/2-backlash/2)/(2*pitch_radius(n))*180/PI
    + involute_angle(pitch_radius(n),pitch_radius(n)*cos(pressure_angle))
    - involute_angle(r,pitch_radius(n)*cos(pressure_angle));
function internal_half(n,r) =
    (PI*gear_module/2-backlash/2)/(2*pitch_radius(n))*180/PI
    - involute_angle(pitch_radius(n),pitch_radius(n)*cos(pressure_angle))
    + involute_angle(r,pitch_radius(n)*cos(pressure_angle));
module external_gear(n,bore,width=gear_width) {
    rp=pitch_radius(n); rb=rp*cos(pressure_angle);
    rr=rp-gear_module-clearance; rt=rp+gear_module;
    rf=max(rb,rr); steps=18;
    assert(n>=ceil(2/pow(sin(pressure_angle),2)),
           "Unshifted external involute undercut: use >=18 teeth at 20 deg");
    difference() {
        union() {
            cylinder(r=rr+0.04,h=width);
            for(t=[0:n-1]) rotate([0,0,t*360/n])
                linear_extrude(height=width)
                    polygon(concat(
                        [polar(rr-0.02,-external_half(n,rf))],
                        [for(i=[0:steps]) let(r=rf+(rt-rf)*i/steps)
                            polar(r,-external_half(n,r))],
                        [for(i=[steps:-1:0]) let(r=rf+(rt-rf)*i/steps)
                            polar(r,external_half(n,r))],
                        [polar(rr-0.02,external_half(n,rf))]));
        }
        translate([0,0,-1]) cylinder(d=bore+fit,h=width+2);
    }
}
// The ring HOLE follows internal involute flanks, not an external gear cutter.
module internal_ring(width=17) {
    n=ring_teeth; rp=pitch_radius(n);
    rt=rp-gear_module; rr=rp+gear_module+clearance;
    steps=18; tooth_step=360/n;
    assert(rt>rp*cos(pressure_angle),"Internal tip below base circle");
    assert(internal_half(n,rr)<tooth_step/2,"Internal root flanks overlap");
    pts=[for(t=[0:n-1]) each concat(
        [for(i=[0:steps]) let(r=rr-(rr-rt)*i/steps)
            polar(r,180/n+t*tooth_step-internal_half(n,r))],
        [for(i=[steps:-1:0]) let(r=rr-(rr-rt)*i/steps)
            polar(r,180/n+t*tooth_step+internal_half(n,r))],
        [for(j=[1:4]) polar(rr,180/n+t*tooth_step+internal_half(n,rr)
            +(tooth_step-2*internal_half(n,rr))*j/5)])];
    difference() {
        cylinder(r=ring_outer_radius,h=width);
        translate([0,0,-1]) linear_extrude(height=width+2) polygon(pts);
        for(a=[30:60:330]) translate([58.5*cos(a),58.5*sin(a),-1])
            cylinder(d=3.4,h=width+2);
    }
}
module pinned_hub(bore,height=8) {
    difference() {
        cylinder(d=20,h=height);
        translate([0,0,-1]) cylinder(d=bore+fit,h=height+2);
        translate([-11,0,height/2]) rotate([0,90,0]) cylinder(d=3.2,h=22);
    }
}
module sun(stage=1) {
    bore=stage==1?motor_shaft:8;
    union() {
        translate([0,0,8]) external_gear(sun_teeth,bore);
        if(stage==2) pinned_hub(bore);
        else difference() {
            cylinder(d=20,h=8);
            translate([0,0,-1]) cylinder(d=bore+fit,h=10);
            translate([-11,0,4]) rotate([0,90,0]) cylinder(d=2.5,h=11);
            // M3 brass heat-set insert counterbore, installed from outside.
            translate([-10.1,0,4]) rotate([0,90,0]) cylinder(d=4.2,h=4);
        }
    }
}
module planet() { external_gear(planet_teeth,6); }
