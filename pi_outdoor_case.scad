// --- Raspberry Pi 4 + Cam V3 + Breadboard Outdoor Case Design ---

// Parameters
case_w = 110;
case_d = 140;
case_h = 80;
wall_thick = 3;

module main_case() {
    difference() {
        // Main Body
        cube([case_w, case_d, case_h], center = true);

        // Hollow Interior
        translate([0,0,wall_thick])
            cube([case_w-wall_thick*2, case_d-wall_thick*2, case_h], center = true);

        // 1. Camera Window (Front)
        translate([0, case_d/2 - 2, 15])
            cube([30, 10, 20], center = true);

        // 2. Cooling Vents (Side - Louvers style)
        for (i = [-2 : 2]) {
            translate([case_w/2 - 2, i*15, 10])
                rotate([0, 45, 0]) cube([10, 10, 2], center = true);
            translate([-case_w/2 + 2, i*15, 10])
                rotate([0, -45, 0]) cube([10, 10, 2], center = true);
        }

        // 3. Power Cable Hole (Bottom)
        translate([0, -case_d/2 + 20, -case_h/2])
            cylinder(h = 20, r = 7, center = true);
    }
}

module internals() {
    // 4. Raspberry Pi 4 Mounts (Stands)
    // Standard Pi 4 holes: 58mm x 49mm
    translate([-29, -24.5, -case_h/2 + wall_thick])
        cylinder(h=15, r=2.5); // Hole 1
    translate([29, -24.5, -case_h/2 + wall_thick])
        cylinder(h=15, r=2.5); // Hole 2
    translate([-29, 24.5, -case_h/2 + wall_thick])
        cylinder(h=15, r=2.5); // Hole 3
    translate([29, 24.5, -case_h/2 + wall_thick])
        cylinder(h=15, r=2.5); // Hole 4

    // 5. Camera Mount (Angled 15 degrees)
    translate([0, case_d/2 - 15, 10])
        rotate([-15, 0, 0])
        difference() {
            cube([40, 2, 40], center = true);
            cube([15, 5, 15], center = true); // Lens hole
        }

    // 6. Breadboard Holder (Bottom Area)
    translate([0, -30, -case_h/2 + wall_thick + 2])
        %cube([55, 85, 5], center = true); // Ghost preview of breadboard
}

// Render the design
union() {
    main_case();
    internals();
}
