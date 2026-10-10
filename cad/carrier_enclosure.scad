// ORIGINAL stationary modular enclosure for ACTUAL reported routed carrier.
// PCB180x130, holes5/175 by5/125, thickness1.6 and holes3.2 confirmed.
carrier_part="assembly";
pcb_w=180;
pcb_d=130;
pcb_t=1.6; // confirmed by carrier hardware designer
pcb_hole=3.2; // confirmed PCB M3 holes; verify finished board before assembly
wall=2;
edge_clearance=22; // verified design allowance for mating connectors / bends
floor_t=2;
standoff_h=6;
component_headroom=32;
brand_font="Liberation Sans:style=Bold"; // bundled with isolated OpenSCAD2021.01
brand_raise=0.7;
brand_name="BRICOHAMS";
brand_url="bricohams.org";
fit=0.25;
w=pcb_w+2*edge_clearance+2*wall;
d=pcb_d+2*edge_clearance+2*wall;
h=floor_t+standoff_h+pcb_t+component_headroom+2;
$fn=48;
module pcb_mounts() {
    for(x=[5,175],y=[5,125]) translate([wall+edge_clearance+x,wall+edge_clearance+y,0])
        children();
}
module carrier_base() {
    difference() {
        union() {
            difference() {
                cube([w,d,h]);
                translate([wall,wall,floor_t]) cube([w-2*wall,d-2*wall,h]);
                // Removable connector plates; no invented connector positions.
                for(x=[20,w-60]) translate([x,-1,15]) cube([40,wall+2,22]);
                for(y=[25,d-55]) translate([-1,y,15]) cube([wall+2,30,22]);
            }
            pcb_mounts() cylinder(d=8,h=floor_t+standoff_h);
            for(x=[5,w-5],y=[5,d-5]) translate([x,y,0]) cylinder(d=8,h=h);
            for(x=[18,w-18]) translate([x-6,-10,0]) cube([12,10,4]);
        }
        pcb_mounts() translate([0,0,-1]) cylinder(d=pcb_hole,h=floor_t+standoff_h+2);
        for(x=[5,w-5],y=[5,d-5]) translate([x,y,3]) cylinder(d=2.5,h=h);
        for(x=[18,w-18]) translate([x,-5,-1]) cylinder(d=4.5,h=6);
        for(x=[20,w-60]) for(dx=[-4,44]) translate([x+dx,-1,26]) rotate([-90,0,0]) cylinder(d=2.4,h=wall+2);
        for(y=[25,d-55]) for(dy=[-4,34]) translate([-1,y+dy,26]) rotate([0,90,0]) cylinder(d=2.4,h=wall+2);
    }
}
module carrier_lid() {
    union() {
        difference() {
            cube([w,d,2]);
            for(x=[5,w-5],y=[5,d-5]) translate([x,y,-1]) cylinder(d=3.4,h=4);
        }
        // 0.05 mm overlap joins every glyph to the actual lid, no floating badge.
        translate([w/2,d/2+10,1.95]) linear_extrude(height=brand_raise+0.05)
            offset(delta=0.03) text(brand_name,size=12,font=brand_font,halign="center",valign="center");
        translate([w/2,d/2-10,1.95]) linear_extrude(height=brand_raise+0.05)
            offset(delta=0.03) text(brand_url,size=8,font=brand_font,halign="center",valign="center");
    }
}
module port_cover(wide=true) {
    span=wide?52:42;
    difference() {
        cube([span,30,2]);
        for(x=[2,span-2]) translate([x,15,-1]) cylinder(d=2.4,h=4);
    }
}
module carrier_assembly() {
    color("gray") carrier_base();
    color("green") translate([wall+edge_clearance,wall+edge_clearance,8]) difference() {
        cube([pcb_w,pcb_d,pcb_t]);
        for(x=[5,175],y=[5,125]) translate([x,y,-1]) cylinder(d=pcb_hole,h=pcb_t+2);
    }
    // Header/component clearance envelope is transparent, NOT routed components.
    %translate([wall+edge_clearance,wall+edge_clearance,8+pcb_t]) cube([pcb_w,pcb_d,component_headroom]);
    color("gray") translate([0,0,h]) carrier_lid();
    for(x=[20,w-60]) translate([x-6,-2,11]) rotate([90,0,0]) port_cover();
    for(y=[25,d-55]) translate([-2,y-6,11]) rotate([90,0,90]) port_cover(false);
}
module carrier_metal_mount() {
    // Separate 2 mm aluminum stationary tray, NOT a printable ASA part.
    difference() {
        translate([-6,-12,0]) cube([w+12,d+18,2]);
        for(x=[18,w-18]) translate([x,-5,-1]) cylinder(d=4.5,h=4);
        for(x=[24,w-24],y=[d/2-15,d/2+15]) translate([x,y,-1]) cylinder(d=5.5,h=4);
    }
}
if(carrier_part=="assembly") carrier_assembly();
else if(carrier_part=="base") carrier_base();
else if(carrier_part=="lid") carrier_lid();
else if(carrier_part=="port40") port_cover();
else if(carrier_part=="port30") port_cover(false);
else if(carrier_part=="mount_dxf") projection(cut=true) translate([0,0,-1]) carrier_metal_mount();
else assert(false,"Unknown carrier_part");
