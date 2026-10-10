# Technical risks and mitigations

| Risk | Cause | Mitigation | Evidence needed |
| --- | --- | --- | --- |
| Wind exceeds available torque | Area/lever arm dominate; small NEMA14 | Limit operation, balance, stop | Running torque and load test |
| Tripod slips | Camera rating is not AZ torque rating | Metal attachment, secondary retention, test | Torsion without loosening |
| Planetary backlash | Play, printing, flexible carrier | Tolerances and feedback | Measure output backlash |
| Sun gear undercut | Insufficient tooth count | 18-tooth, module-1.5 base | Inspect profile/contact |
| Impossible gear mesh | Incorrect phase/clearance/support | Assemble one stage first | Full manual rotation |
| Lost reference | Reboot, switch, broken wire | Disarm and re-home | Fault injection |
| Wrong heading | Magnets/motors, declination | Verify true north | Measure orientation error |
| Invalid UTC/position | No GNSS fix or stale clock | Validity states and inhibition | Test without GNSS and after reboot |
| Old TLE | Cache or provider stale | Per-satellite epoch and inhibit | Age tests |
| V/U coupling | Shared radiators and reflector | Simulation and assembled VNA | Final VSWR/pattern |
| Hybrid out of band | SATCOM device not 145/435 MHz | Manufacturer data and measurement | Per-band S-parameters |
| Incompatible diplexer | Name/project reference, not measurement | Verify exact revision and test | Dimensions, power, isolation |
| Poor foldable RF contact | Plastic hinge, oxidation | Positive metal joint | Repeat VNA after 50 cycles |
| Rotor EMI | Driver/DC-DC close to coax | Metal sub-enclosure and filtering | RX with motors on/off |
| Assumed full duplex | Single half-duplex RT3S | Explicit operation or separate receiver | Test actual radio |
| Zenith / cable wrap | Speed singularity and limits | Exclude unreachable passes | Simulation and bench |
| Heating / ASA | Sunlit enclosure and driver current | Correct current and ventilation | Measured temperature |
| Mass exceeds target | Forgotten battery, steel, and coax | Weigh actual assembly | Documented weighing |
| Third-party rights | Public URL is not a license | Original work; cite without copying STL | Provenance register |

Mechanical and RF risks are not closed by software tests. A `pending` status
is intentional and must remain visible.
