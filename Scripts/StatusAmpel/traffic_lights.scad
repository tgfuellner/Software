shaftInner=3.5;
wallwidth=1;
overlap=0.01;
wiggle=0.1;
screwDiameter=3;

deltaFix=10;
led=8;

module shade(shadeSize) {
	echo(shadeSize);
	translate([0, 0, shadeSize/4]) difference() {
		cylinder(center=true,r=shadeSize/2,h=shadeSize/2);
		translate([0, 0, 0]) rotate([27, 0, 0]) translate([0, 0, shadeSize/4]) cube([2*shadeSize, 2*shadeSize, shadeSize/2], center=true);
	}
}

module chamber(size, shadeSize) {
	echo(shadeSize);
        
	rotate(a=[90, 0, 0]) cylinder(center=true, r=shadeSize/2-1.2*wallwidth, h=2*size);
	rotate(a=[0, 90, 0]) cylinder(center=true, r=shadeSize/2-1.2*wallwidth, h=2*size);
        translate([0,0,-shadeSize/2]) cube(center=true, [led, led, 5]);
}

module three_shades(size, delta, shadeSize) {
	translate([0, overlap-size/2, delta-deltaFix]) rotate([90, 0, 0]) shade(shadeSize);
	translate([0, overlap-size/2, -deltaFix]) rotate([90, 0, 0]) shade(shadeSize);
	//translate([0, overlap-size/2, -delta]) rotate([90, 0, 0]) shade(shadeSize);
}

module corpse(size=21, height=58) {
	delta=10+(height-4*wallwidth)/3;
	shadeSize=min(size-4*wallwidth, delta-2*wallwidth);
	translate([0, 0, height/2]) difference() {
		union() {
			cube(center=true,[size, size, height]);
			three_shades(size, delta, shadeSize);
			rotate([0, 0, 90]) three_shades(size, delta, shadeSize);
			rotate([0, 0, 180]) three_shades(size, delta, shadeSize);
			rotate([0, 0, 270]) three_shades(size, delta, shadeSize);
		}
		translate([0, 0, delta-deltaFix]) chamber(size, shadeSize);
		//chamber(size, shadeSize);
		translate([0, 0, -deltaFix]) chamber(size, shadeSize);
		translate([0, 0, -10]) cylinder(r=shaftInner, h=height, center=true, $fn=30);
#		translate([0, 0, 1.5*wallwidth-height/2-overlap]) cylinder(r=shaftInner+wallwidth+0.5+wiggle/2, h=3*wallwidth, center=true, $fn=30);
	}
}

module shaft(size, length) {
  difference() {
	translate([0, 0, length/2 + 2*wallwidth]) {
		difference() {
			union() {
				cylinder(r=shaftInner+wallwidth+0.5, h=length, center=true, $fn=30);
				translate([0, 0, -length/2-wallwidth+overlap]) cube([size, size, 2*wallwidth+overlap], center=true);
			}
			cylinder(r=shaftInner, h=2*length, center=true, $fn=30);
			translate([size/2-4*wallwidth, size/2-4*wallwidth,-length/2-3*wallwidth]) cylinder(r=screwDiameter/2, h=4*wallwidth, $fn=30);
			rotate([0, 0, 90]) translate([size/2-4*wallwidth, size/2-4*wallwidth,-length/2-3*wallwidth]) cylinder(r=screwDiameter/2, h=4*wallwidth, $fn=30);
			rotate([0, 0, 180]) translate([size/2-4*wallwidth, size/2-4*wallwidth,-length/2-3*wallwidth]) cylinder(r=screwDiameter/2, h=4*wallwidth, $fn=30);
			rotate([0, 0, 270]) translate([size/2-4*wallwidth, size/2-4*wallwidth,-length/2-3*wallwidth]) cylinder(r=screwDiameter/2, h=4*wallwidth, $fn=30);

		}
	}

    translate([0,13,0]) cube([size-20,1.2,10], center=true);
    translate([0,-13,0]) cube([size-20,1.2,10], center=true);
  }
}

module screwMount(radius, height) {
	outer = radius+1.5*wallwidth;
	difference() {
		union() {
			cylinder(r=outer, height-2*wallwidth, $fn=30);
			cube([outer, outer, height-2*wallwidth], center=false);
		}
		translate([0,0,-wallwidth/2]) cylinder(r=0.85*radius, height, $fn=30);
	}	
}

module casing(size, height) {
	translate([0, 0, height/2]) difference() {
		cube([size+4*wallwidth, size+4*wallwidth, height], center=true);
		translate([0, 0, height/2 - wallwidth + overlap]) cube([size+wiggle, size+wiggle, 2*wallwidth+wiggle], center=true);
		translate([0, 0, 2*wallwidth]) cube([size-2*wallwidth, size-2*wallwidth, height], center=true);
		// translate([size/2, 0, 0]) cube([5*wallwidth, 12.5, 11], center=true);
	}
	translate([size/2-4*wallwidth+overlap, size/2-4*wallwidth+overlap, 0]) screwMount(screwDiameter/2, height);
	rotate([0, 0, 90]) translate([size/2-4*wallwidth+overlap, size/2-4*wallwidth+overlap, 0]) screwMount(screwDiameter/2, height);
	rotate([0, 0, 180]) translate([size/2-4*wallwidth+overlap, size/2-4*wallwidth+overlap, 0]) screwMount(screwDiameter/2, height);
	rotate([0, 0, 270]) translate([size/2-4*wallwidth+overlap, size/2-4*wallwidth+overlap, 0]) screwMount(screwDiameter/2, height);
}

// design=true;
// plate=true;

if (design) {
	translate([0, 0, 20 - 2*wallwidth]) shaft(50, 90);
	translate([0, 0, 110 - 2*wallwidth]) corpse();
	casing(50, 20);
} else if (plate) {
	corpse();
	translate([60, 0, 0]) shaft(50, 90);
	translate([-60, 0, 0]) casing(50, 20);
} else {
//corpse();
shaft(50, 56);
//casing(50, 30);
}

