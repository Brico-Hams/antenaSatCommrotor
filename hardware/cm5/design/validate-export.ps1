param(
    [Parameter(Mandatory=$true)][string]$KiCadRoot,
    [switch]$RebuildAndRoute,
    [string]$RouterJar,
    [string]$JavaPath
)
$ErrorActionPreference = 'Stop'
$boardRoot = Split-Path $PSScriptRoot -Parent
$cli = Join-Path $KiCadRoot 'bin\kicad-cli.exe'
$python = Join-Path $KiCadRoot 'bin\python.exe'
$env:KICAD10_SYMBOL_DIR = Join-Path $KiCadRoot 'share\kicad\symbols'
$env:KICAD10_FOOTPRINT_DIR = Join-Path $KiCadRoot 'share\kicad\footprints'
$version = & $cli version
if ($version.Trim() -ne '10.0.7') { throw "Required KiCad 10.0.7; found $version" }
$log = @()
function Invoke-Checked([string]$Name,[string]$Exe,[string[]]$ArgumentList) {
    & $Exe @ArgumentList
    $code = $LASTEXITCODE
    $script:log += [pscustomobject]@{step=$Name; exitCode=$code; executable=$Exe; arguments=$ArgumentList}
    if ($code -ne 0) { throw "$Name failed ($code); manufacturing exports not refreshed" }
}
$sch = Join-Path $boardRoot 'cm5-guard-A.kicad_sch'
$pcb = Join-Path $boardRoot 'cm5-guard-A.kicad_pcb'
$reports = Join-Path $boardRoot 'reports'
$exports = Join-Path $boardRoot 'fabrication\NOT_FOR_MANUFACTURE'
if ($RebuildAndRoute) {
    if (-not $RouterJar) { $RouterJar = Join-Path $PSScriptRoot 'tools\freerouting-1.9.0.jar' }
    if (-not $JavaPath) {
        $JavaPath = Get-ChildItem (Join-Path $PSScriptRoot 'tools\jre17') -Recurse -Filter java.exe | Select-Object -First 1 -ExpandProperty FullName
    }
    if (-not (Test-Path $RouterJar) -or -not $JavaPath) { throw 'Local Freerouting 1.9.0 and JRE17 required for regeneration' }
    Invoke-Checked 'Generate schematic' $python @((Join-Path $PSScriptRoot 'generate_guard.py'),'--kicad-root',$KiCadRoot)
}
Invoke-Checked 'ERC all severities' $cli @('sch','erc','--severity-all','--format','json','--exit-code-violations','-o',(Join-Path $reports 'erc.json'),$sch)
Invoke-Checked 'Netlist' $cli @('sch','export','netlist','--format','kicadxml','-o',(Join-Path $reports 'cm5-guard-A.net.xml'),$sch)
if ($RebuildAndRoute) {
    Invoke-Checked 'Fixed module/SMA/power placement' $python @((Join-Path $PSScriptRoot 'generate_guard.py'),'--board-only','--kicad-root',$KiCadRoot)
    Invoke-Checked 'Local routing preparation' $python @((Join-Path $PSScriptRoot 'route_guard.py'),'prepare')
    Invoke-Checked 'Local autorouter NO ANALYTICS' $JavaPath @('-Xmx2g','-jar',$RouterJar,'-de',(Join-Path $PSScriptRoot 'routing\guard.dsn'),'-do',(Join-Path $PSScriptRoot 'routing\guard.ses'),'-mp','45','-mt','0','-da','-l','en')
    Invoke-Checked 'Import routing and RF reference planes' $python @((Join-Path $PSScriptRoot 'route_guard.py'),'import')
    Invoke-Checked 'Complete bounded residual signal routes' $python @((Join-Path $PSScriptRoot 'finish_missing.py'),'--kicad-root',$KiCadRoot)
}
Invoke-Checked 'DRC all tracks + parity + zone refill' $cli @('pcb','drc','--schematic-parity','--all-track-errors','--severity-all','--refill-zones','--save-board','--format','json','--exit-code-violations','-o',(Join-Path $reports 'drc.json'),$pcb)
Invoke-Checked 'PDF' $cli @('sch','export','pdf','-o',(Join-Path $reports 'cm5-guard-A.pdf'),$sch)
Invoke-Checked 'Gerber review snapshot' $cli @('pcb','export','gerbers','-l','F.Cu,B.Cu,F.Paste,B.Paste,F.SilkS,B.SilkS,F.Mask,B.Mask,Edge.Cuts','-o',((Join-Path $exports 'gerber')+'\'),$pcb)
Invoke-Checked 'Excellon review snapshot' $cli @('pcb','export','drill','--format','excellon','--excellon-units','mm','--excellon-separate-th','--generate-map','-o',((Join-Path $exports 'gerber')+'\'),$pcb)
Invoke-Checked 'SMT positions (exclude DNP/net-tie/THT)' $cli @('pcb','export','pos','--format','csv','--units','mm','--side','front','--smd-only','--exclude-dnp','-o',(Join-Path $exports 'positions-kicad.csv'),$pcb)
$log | ConvertTo-Json -Depth 6 | Set-Content -Encoding UTF8 (Join-Path $reports 'commands.json')
Invoke-Checked 'Contract/circuit/rearm/geometry tests and review BOM/CPL' $python @((Join-Path $PSScriptRoot 'export_review.py'))
Write-Warning 'Digital checks PASS; electrical, mechanical, EMC/RF and sourcing qualification PENDING. NOT FABRICABLE / DO NOT OPERATE.'

