# Antenna-only installation

The antenna module does not need this Raspberry Pi OS image or any host
software. Build and qualify the antenna independently; use a mechanically
qualified manual support and a compatible external radio if desired.

1. Select the antenna revision, bands, approved frequencies, and matching
   mechanical parts from the antenna module documentation and BOM.
2. Assemble without connecting an SDR or applying transmit power. Verify
   cables, connector type, strain relief, and mounting loads.
3. Measure and record resonance/matching, feed isolation, and (if installed)
   circular-polarization phase/amplitude and axial ratio. Do not infer RF
   performance from CAD dimensions or mechanical POL rotation.
4. Begin RF tests at low power into a suitable load. Do not connect a PA or
   transmit until the RF path is measured and qualified.

See [`../../docs/MODULE-ANTENNA.md`](../../docs/MODULE-ANTENNA.md),
[`../../docs/MECHANICAL.md`](../../docs/MECHANICAL.md), and
[`../../docs/ACCEPTANCE.md`](../../docs/ACCEPTANCE.md). This guide does not
claim measured antenna performance.
