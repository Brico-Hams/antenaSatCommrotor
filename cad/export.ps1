param(
    [string]$OpenSCAD = "$PSScriptRoot\tools\openscad-2021.01\openscad.exe",
    [string]$Node = 'node',
    [string[]]$Only = @()
)
$ErrorActionPreference = 'Stop'
if (!(Test-Path -LiteralPath $OpenSCAD)) { throw 'Supply a local OpenSCAD CLI path; no global installation is needed.' }
$parts = @('sun1','sun2','planet','ring','carrier1','carrier2','motor_plate',
    'intermediate_plate','output_plate','keeper608','keeper6000','spacer15',
    'spacer6','spacer9','spacer38','tripod_base','output_flange','elevation_bracket',
    'saddle20','saddle25','saddle32','flat_adapter','limit_bracket',
    'magnet_holder','sensor_bracket','radio_cradle','enclosure','enclosure_lid',
    'diplexor_box','diplexor_lid','antenna_hub','band_bridge','arm_socket','coupon')
if ($Only.Count -gt 0) {
    foreach ($requested in $Only) {
        if ($parts -notcontains $requested) { throw "Unknown printable selector: $requested" }
    }
    $parts = $Only
}
$out = Join-Path $PSScriptRoot 'stl'
New-Item -ItemType Directory -Path $out -Force | Out-Null
foreach ($part in $parts) {
    $file = Join-Path $out "$part.stl"
    $log = Join-Path $out "$part.render.log"
    $arguments = @('-o',"`"$file`"",'-D',('part=\"{0}\"' -f $part),"`"$(Join-Path $PSScriptRoot 'station.scad')`"")
    $process = Start-Process -FilePath $OpenSCAD -ArgumentList $arguments -Wait -PassThru -NoNewWindow `
        -RedirectStandardError $log -RedirectStandardOutput (Join-Path $out "$part.stdout.log")
    if ($process.ExitCode -ne 0 -or !(Test-Path $file)) { throw "OpenSCAD render failed: $part; see $log" }
    if (Select-String -Path $log -Pattern 'ERROR:|WARNING:') { throw "OpenSCAD diagnostic in $log" }
    & $Node (Join-Path $PSScriptRoot '..\tests\mechanical-stl.cjs') $file
    if ($LASTEXITCODE -ne 0) { throw "STL validation failed: $part" }
}
# Assemblies contain overlapping installed components, so do NOT export them
# as a purported printable/manifold STL. CSG retains the component preview.
& $OpenSCAD -o (Join-Path $PSScriptRoot 'assembly.csg') -D 'part=\"assembly\"' (Join-Path $PSScriptRoot 'station.scad')
if ($LASTEXITCODE -ne 0) { throw 'Assembly CSG failed' }
Write-Output "Rendered and edge-manifold checked $($parts.Count) printable part selectors."
