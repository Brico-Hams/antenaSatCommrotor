param(
    [Parameter(Mandatory = $true)][string]$KiCadCli
)
$ErrorActionPreference = 'Stop'
$root = Split-Path $PSScriptRoot -Parent
$pcb = Join-Path $PSScriptRoot 'PortableSatCarrier.kicad_pcb'
$sch = Join-Path $PSScriptRoot 'PortableSatCarrier.kicad_sch'
$fab = Join-Path $root 'fabrication'
$reports = Join-Path $fab 'reports'
$gerbers = Join-Path $fab 'gerbers'
New-Item -ItemType Directory -Force $reports, $gerbers | Out-Null
if (-not (Test-Path $KiCadCli -PathType Leaf)) { throw 'Supply an existing official kicad-cli executable; no global install required.' }
$version = (& $KiCadCli version | Out-String).Trim()
$statusPath = Join-Path $fab 'release-status.json'
$status = [ordered]@{
    kicad_version = $version
    timestamp_utc = [DateTime]::UtcNow.ToString('o')
    cad_verified = $false
    production_release = $false
    assembly_operation_release = $false
    blockers = @(
        'Physical ESP32 DevKitC V4 38pin and Watterott TMC2209 v2.x footprint/pinout measurement',
        'Exact external maintained-latching NC stop with >=5A at 12V DC breaking rating and isolated NC auxiliary selection',
        'Commercial protected source, source cable fuse, power transient/current/thermal/selectivity bench qualification',
        '3V3 current budget and external sensor/GNSS breakout physical/voltage verification',
        'Firmware carrierVerified remains false until physical checkout; encoders/calibration/mechanics/stop-rearm bench tests'
    )
}
function Write-Status { $status | ConvertTo-Json -Depth 8 | Set-Content -Encoding UTF8 $statusPath }
Write-Status
& $KiCadCli pcb drc $pcb --output (Join-Path $reports 'drc.json') --format json --schematic-parity --severity-all --exit-code-violations
if ($LASTEXITCODE -ne 0) { throw 'DRC failed. Old fabrication files, if present, are invalid: cad_verified=false.' }
& $KiCadCli sch erc $sch --output (Join-Path $reports 'erc.json') --format json --severity-all --exit-code-violations
if ($LASTEXITCODE -ne 0) { throw 'ERC failed. Fabrication export blocked.' }
$drc = Get-Content (Join-Path $reports 'drc.json') -Raw | ConvertFrom-Json
$erc = Get-Content (Join-Path $reports 'erc.json') -Raw | ConvertFrom-Json
$ercCount = @($erc.sheets | ForEach-Object { $_.violations } | Where-Object { $null -ne $_ }).Count
if (@($drc.violations).Count -ne 0 -or @($drc.unconnected_items).Count -ne 0 -or @($drc.schematic_parity).Count -ne 0 -or $ercCount -ne 0) {
    throw 'Nonempty CAD reports: fabrication export blocked, even if CLI exit status was zero.'
}
& $KiCadCli sch export netlist $sch --output (Join-Path $fab 'PortableSatCarrier.net')
if ($LASTEXITCODE -ne 0) { throw 'Netlist export failed.' }
& $KiCadCli sch export pdf $sch --output (Join-Path $fab 'PortableSatCarrier-schematic.pdf')
if ($LASTEXITCODE -ne 0) { throw 'Schematic PDF export failed.' }
& $KiCadCli pcb export gerbers $pcb --output $gerbers --layers 'F.Cu,B.Cu,F.Mask,B.Mask,F.SilkS,B.SilkS,Edge.Cuts'
if ($LASTEXITCODE -ne 0) { throw 'Gerber export failed.' }
& $KiCadCli pcb export drill $pcb --output $gerbers --format excellon --drill-origin absolute --excellon-units mm --excellon-zeros-format decimal --excellon-separate-th --generate-report --report-path (Join-Path $reports 'drill.txt')
if ($LASTEXITCODE -ne 0) { throw 'Excellon export failed.' }
& $KiCadCli pcb export pos $pcb --output (Join-Path $fab 'assembly-positions.csv') --format csv --units mm
if ($LASTEXITCODE -ne 0) { throw 'Assembly position export failed.' }
& $KiCadCli pcb export pdf $pcb --output (Join-Path $fab 'assembly-drawing.pdf') --layers 'F.Fab,F.SilkS,Edge.Cuts'
if ($LASTEXITCODE -ne 0) { throw 'Assembly drawing export failed.' }
$archive = Join-Path $fab 'PortableSatCarrier-Gerbers-CAD-VERIFIED-NOT-RELEASED.zip'
$archiveInputs = @(Get-ChildItem $gerbers -File | Where-Object { $_.Extension -in @('.gtl','.gbl','.gts','.gbs','.gto','.gbo','.gm1','.drl','.gbrjob') } | ForEach-Object { $_.FullName })
if ($archiveInputs.Count -ne 10) { throw 'Unexpected fabrication layer/drill set: archive export blocked.' }
Compress-Archive -LiteralPath $archiveInputs -DestinationPath $archive -Force
$status['cad_verified'] = $true
$status['drc_violations'] = @($drc.violations).Count
$status['unconnected_items'] = @($drc.unconnected_items).Count
$status['schematic_parity_issues'] = @($drc.schematic_parity).Count
$status['erc_violations'] = $ercCount
$connectionData = Get-Content (Join-Path $PSScriptRoot 'connectivity.json') -Raw | ConvertFrom-Json
$status['board_mm'] = $connectionData.board_mm
$status['mounting_holes_mm'] = $connectionData.holes_mm
$status['router'] = $connectionData.router
$hashes = [ordered]@{}
$files = @($pcb, $sch, (Join-Path $PSScriptRoot 'PortableSatCarrier.kicad_pro'), (Join-Path $PSScriptRoot 'connectivity.json'),
    (Join-Path $PSScriptRoot 'generate-carrier.cjs'), (Join-Path $reports 'drc.json'), (Join-Path $reports 'erc.json'),
    (Join-Path $fab 'PortableSatCarrier.net'), (Join-Path $fab 'assembly-positions.csv'))
$files += @(Get-ChildItem $gerbers -File | ForEach-Object { $_.FullName })
$files += @(Get-ChildItem (Join-Path $PSScriptRoot 'PortableSatCarrier.pretty') -File | ForEach-Object { $_.FullName })
$files += @((Join-Path $PSScriptRoot 'PortableSatCarrier.kicad_sym'), (Join-Path $PSScriptRoot 'fp-lib-table'),
    (Join-Path $PSScriptRoot 'PortableSatCarrier.kicad_dru'),
    (Join-Path $PSScriptRoot 'sym-lib-table'), (Join-Path $PSScriptRoot 'validate-export.ps1'),
    (Join-Path $root 'bom\pcb.csv'), (Join-Path $fab 'STACKUP.txt'),
    (Join-Path $fab 'PortableSatCarrier-schematic.pdf'), (Join-Path $fab 'assembly-drawing.pdf'), $archive)
foreach ($file in $files) {
    $relative = $file.Substring($root.Length + 1).Replace('\','/')
    $hashes[$relative] = (Get-FileHash $file -Algorithm SHA256).Hash.ToLowerInvariant()
}
$status['sha256'] = $hashes
Write-Status
Write-Output "CAD verified with KiCad ${version}: DRC=0 ERC=0 unconnected=0 parity=0. Production/assembly/operation remain HOLD; read docs\PCB.md."
