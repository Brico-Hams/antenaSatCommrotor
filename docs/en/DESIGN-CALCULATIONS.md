# Reproducible calculations and limits on their interpretation

The sole input for these examples is [design.json](../../calc/design.json).
Run [engineering-report.cjs](../../scripts/engineering-report.cjs) to
recompute them, and run the project tests to verify the relationships. These
calculations are independent of RF and load testing.

## Initial lengths by band

Starting empirical model from the Tomas Brincil reference:

```text
lambda = c / f
L_total_dipole = lambda / 2 * 0.92
L_total_reflector = 1.05 * L_total_dipole
reflector_spacing = 0.225 * lambda
```

| Quantity | 145 MHz | 435 MHz |
| --- | ---: | ---: |
| Wavelength, mm | 2067.534 | 689.178 |
| TOTAL dipole length, mm | 951.066 | 317.022 |
| Each dipole arm, mm | 475.533 | 158.511 |
| Initial cut per arm (+10 mm), mm | 485.533 | 168.511 |
| TOTAL reflector length, mm | 998.619 | 332.873 |
| Reflector spacing, mm | 465.195 | 155.065 |

Do not confuse total length with each arm. A crossed dipole has two
orthogonal dipoles per band; a crossed reflector likewise has two orthogonal
elements. Conductor diameter, feed gap, joints, plastics, boom, and other
bands affect resonance and impedance. These numbers are not an optimized
Yagi and do not demonstrate circular polarization.

The VHF spacing explains why a rigid 300 mm boom is insufficient for this
geometry; the original mount must use removable sections. Folded conductors
retain continuity through metal and mechanical locks, not incidental hinge
contact.

### Coax quarter wavelength: an example, not a complete hybrid

`L_coax = lambda / 4 * VF`

With assumed VF 0.66: 341.143 mm at 145 MHz and 113.714 mm at 435 MHz.
Measure the cable's actual VF. Two 50-ohm jumpers of these lengths do not
automatically make a matched 50-ohm divider/hybrid. The topology, impedances,
termination, balance, and measurement described in the RF manual are needed.

## Planetary reduction

For a fixed ring, sun input, and carrier output:

`i = 1 + N_ring / N_sun = 1 + 72/18 = 5`

Two cascaded stages: `i_total = 5*5 = 25`.

| Parameter | Value |
| --- | ---: |
| Module | 1.5 mm |
| Pressure angle | 20 degrees |
| Sun / planet / ring | 18 / 27 / 72 teeth |
| Pitch diameters | 27 / 40.5 / 108 mm |
| Planet orbit radius | 33.75 mm |
| Number of planets | 3 |
| Phasing condition | (18+72)/3 = 30, integer |

`N_ring = N_sun + 2*N_planet = 18+54 = 72`.
Center distance between adjacent planets:
`2*33.75*sin(60 degrees) = 58.46 mm`.
Approximate planet outside diameter with one-module addendum:
`1.5*(27+2) = 43.5 mm`. The planets do not intersect in this ideal
cross-section; this does not check supports, screws, or axial stacking.

For a standard uncorrected 20-degree involute tooth:
`N_min ~= 2/sin(20 degrees)^2 = 17.10`.
A 12-tooth sun requires profile correction or another criterion. The
18-tooth base avoids accepting a small gear without analyzing undercut.

## Resolution is not accuracy

```text
200 steps/revolution * 16 microsteps * 25 = 80000 commands/revolution
360 / 80000 = 0.0045 degrees/command
```

Do not count internal driver interpolation as command resolution. Final
accuracy depends on sensors, heading, tilt, backlash, deformation,
eccentricity, and available torque. Measure it at the output.

## Load torque: example that does NOT meet 8 m/s wind

Example assumptions, not specifications for a purchased motor:

- 0.5 kg antenna mass and 0.03 m imbalance.
- 0.1 Nm motor torque and 0.7 efficiency per stage.
- 0.06 m2 projected area, Cd=1.2, air density=1.225 kg/m3.
- Wind 8 m/s and aerodynamic arm 0.25 m.
- Required safety factor 2.

```text
T_gravity = m*g*d = 0.14715 Nm
F_wind = 0.5*rho*Cd*A*v^2 = 2.8224 N
T_wind = F*arm = 0.7056 Nm
T_required_with_margin = 2*(0.14715+0.7056) = 1.7055 Nm
T_assumed_output = 0.1*25*0.7^2 = 1.225 Nm
```

**The margin is not met. Do not operate at 8 m/s based on this calculation.**
Advertised stepper holding torque is not its running torque. Gusts, friction,
acceleration, and tilt require additional margin. Balancing helps gravity but
does not remove wind load.

Do not resolve this failure by exceeding the specified current or assuming a
printed gear can withstand all reduced torque. Measure, reduce load/wind,
change aerodynamics, or change architecture.

## Tripod

A 1/4-20 photographic thread has nominal diameter 6.35 mm and pitch
25.4/20 = 1.27 mm. A 3/8-16 thread has nominal diameter 9.525 mm and pitch
1.5875 mm. Use a metal insert/nut, not a load-bearing ASA thread. These
dimensions do not prove torsional stiffness or tripod capacity.
