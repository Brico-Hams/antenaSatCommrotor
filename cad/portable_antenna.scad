// Original PF-01 candidate. The visual reference supplies no dimensions or RF design.
include <portable-antenna-parameters.scad>
pf_part = "deployed";
$fn = 48;
pf_fit = 0.3;

module pf_tube(od, id, length) {
    difference() {
        cylinder(d=od,h=length);
        translate([0,0,-1]) cylinder(d=id,h=length+2);
    }
}

module pf_cross_hole(d, length) {
    rotate([90,0,0]) cylinder(d=d,h=length,center=true);
}

module pf_hub() {
    difference() {
        union() {
            cylinder(r=pf_hubRingRadiusMm,h=pf_hubBaseHeightMm);
            for(a=[0:90:270]) rotate([0,0,a])
                for(y=[-8,4.2])
                    translate([pf_hubRingRadiusMm-2,y,0])
                        cube([pf_clevisOuterRadiusMm-pf_hubRingRadiusMm+2,3.8,pf_hubHeightMm]);
        }
        translate([0,0,-1]) cylinder(d=pf_boomOuterMm+pf_hubBoreClearanceMm,h=pf_hubHeightMm+2);
        for(a=[0:90:270]) rotate([0,0,a]) {
            translate([pf_pivotRadiusMm,0,pf_pivotHeightMm]) pf_cross_hole(4.4,24);
            translate([pf_pivotRadiusMm+16,0,pf_pivotHeightMm]) pf_cross_hole(3.4,24);
        }
        rotate([0,0,45]) translate([0,0,4]) pf_cross_hole(3.4,60);
    }
}

module pf_hinge() {
    difference() {
        translate([-6,-3.5,-6]) cube([36,7,12]);
        pf_cross_hole(4.4,14);
        translate([16,0,0]) pf_cross_hole(3.4,14);
        translate([18,0,0]) rotate([0,90,0])
            cylinder(d=pf_rodDiameterMm+pf_fit,h=14);
        translate([24,0,-7]) cylinder(d=3.4,h=14);
    }
}

module pf_tip_coupler() {
    difference() {
        cylinder(d=pf_vhfCouplerOuterMm,h=pf_vhfCouplerLengthMm,center=true);
        cylinder(d=pf_vhfCouplerInnerMm,h=pf_vhfCouplerLengthMm+2,center=true);
        for(z=[-8,8]) translate([0,0,z]) rotate([90,0,0])
            cylinder(d=2,h=pf_vhfCouplerOuterMm+2,center=true);
    }
}

module pf_arm(tip, split=false, fold=0, outer=true) {
    translate([pf_pivotRadiusMm,0,pf_pivotHeightMm]) rotate([0,-fold,0]) {
        color("#e8871e") pf_hinge();
        stop=split ? pf_vhfSplitRadiusMm : tip;
        color("silver") translate([pf_rodStartRadiusMm-pf_pivotRadiusMm,0,0])
            rotate([0,90,0]) pf_tube(pf_rodDiameterMm,pf_rodInnerMm,stop-pf_rodStartRadiusMm);
        if(split && outer) {
            color("silver") translate([pf_vhfSplitRadiusMm-pf_pivotRadiusMm,0,0])
                rotate([0,90,0]) pf_tube(pf_rodDiameterMm,pf_rodInnerMm,tip-pf_vhfSplitRadiusMm);
            color("#808c99") translate([pf_vhfSplitRadiusMm-pf_pivotRadiusMm,0,0])
                rotate([0,90,0]) pf_tip_coupler();
        }
    }
}

module pf_cassette(index, fold=0, outer=true) {
    plane=pf_planes[index];
    color(plane[2]==145 ? "#e8871e" : "#326488") pf_hub();
    for(a=[0:90:270]) rotate([0,0,a])
        pf_arm(plane[1]/2,plane[2]==145,fold,outer);
}

module pf_boom_section() {
    difference() {
        pf_tube(pf_boomOuterMm,pf_boomInnerMm,pf_boomSectionMm);
        translate([0,0,pf_boomSectionMm-20]) pf_cross_hole(3.4,24);
    }
}

module pf_spigot() {
    difference() {
        cylinder(d=pf_spigotOuterMm,h=pf_spigotLengthMm);
        for(z=[20,60]) translate([0,0,z]) pf_cross_hole(3.4,20);
    }
}

module pf_deployed() {
    color("#adb9bd") translate([0,0,-pf_boomRearOverhangMm]) pf_boom_section();
    color("#adb9bd") translate([0,0,pf_boomSplitZmm+pf_boomSectionMm])
        rotate([180,0,0]) pf_boom_section();
    color("#65767d") translate([0,0,pf_boomSplitZmm-pf_spigotLengthMm/2]) pf_spigot();
    for(i=[0:3]) translate([0,0,pf_planes[i][0]]) rotate([0,0,pf_planes[i][3]]) pf_cassette(i);
    pf_reflector_mesh();
}

module pf_reflector_mesh() {
    radius=pf_planes[0][1]/2;
    inner=pf_mesh_centralOpeningRadiusMm;
    color([0.22,0.43,0.42,0.8]) translate([0,0,pf_pivotHeightMm-3])
        for(a=[0:90:270]) rotate([0,0,a])
            linear_extrude(pf_mesh_wireDiameterMm) intersection() {
                polygon([[inner,0],[radius,0],[0,radius],[0,inner]]);
                union() {
                    for(t=[0:pf_mesh_pitchMm:radius]) {
                        translate([t,0]) square([pf_mesh_wireDiameterMm,radius]);
                        translate([0,t]) square([radius,pf_mesh_wireDiameterMm]);
                    }
                }
            }
}

module pf_folded() {
    color("#adb9bd") pf_boom_section();
    color("#adb9bd") translate([pf_stowSpareBoomXmm,0,0]) pf_boom_section();
    for(i=[0:3]) translate([0,0,i*pf_stowHubPitchMm])
        rotate([0,0,i*pf_stowHubClockingDeg])
            pf_cassette(pf_stowOrder[i],90,false);
    for(i=[0:7]) {
        plane=pf_planes[i<4 ? 0 : 3];
        color("silver") translate([pf_stowTipsXmm,(i-3.5)*pf_stowTipPitchMm,0])
            pf_tube(pf_rodDiameterMm,pf_rodInnerMm,plane[1]/2-pf_vhfSplitRadiusMm);
    }
    color("#65767d") pf_spigot();
    color([0.22,0.43,0.42,0.4])
        translate([-pf_mesh_reservedFoldedPacketMm[0]/2,-pf_mesh_reservedFoldedPacketMm[1]/2,pf_mesh_packetBaseZmm])
            cube(pf_mesh_reservedFoldedPacketMm);
}

module pf_hinge_view() {
    color("#326488") pf_hub();
    translate([pf_pivotRadiusMm,-30,pf_pivotHeightMm]) color("#e8871e") pf_hinge();
    translate([pf_pivotRadiusMm+16,-50,pf_pivotHeightMm])
        color("silver") pf_cross_hole(3,28);
    translate([pf_pivotRadiusMm,30,pf_pivotHeightMm])
        color("silver") pf_cross_hole(4,28);
    translate([pf_pivotRadiusMm,0,pf_pivotHeightMm]) rotate([0,-60,0])
        color([0.9,0.55,0.15,0.3]) pf_hinge();
}

module pf_stowed_cassette(i) {
    translate([0,0,i*pf_stowHubPitchMm])
        rotate([0,0,i*pf_stowHubClockingDeg])
            pf_cassette(pf_stowOrder[i],90,false);
}

module pf_sampled_hinge_collisions() {
    for(angle=[0:5:90]) intersection() {
        pf_hub();
        pf_arm(pf_planes[0][1]/2,true,angle,false);
    }
}

module pf_stow_collisions() {
    for(i=[0:2],j=[i+1:3]) intersection() {
        pf_stowed_cassette(i);
        pf_stowed_cassette(j);
    }
}

assert(pf_rodStartRadiusMm>pf_pivotRadiusMm+6,"Rod must clear pivot");
assert(pf_hubHeightMm<pf_stowHubPitchMm,"Stacked hubs need clearance");
assert(pf_vhfSplitRadiusMm<pf_planes[3][1]/2,"VHF tips must be positive");
if(pf_part=="deployed" || pf_part=="front") pf_deployed();
else if(pf_part=="folded") pf_folded();
else if(pf_part=="hinge") pf_hinge_view();
else if(pf_part=="reflector") {
    pf_cassette(0);
    pf_reflector_mesh();
}
else if(pf_part=="hub") pf_hub();
else if(pf_part=="arm") pf_hinge();
else if(pf_part=="coupler") pf_tip_coupler();
else if(pf_part=="boom") pf_boom_section();
else if(pf_part=="spigot") pf_spigot();
else if(pf_part=="hinge-clearance") pf_sampled_hinge_collisions();
else if(pf_part=="stow-clearance") pf_stow_collisions();
else assert(false,"Unknown pf_part");
