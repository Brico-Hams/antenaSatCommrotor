param(
    [Parameter(Mandatory=$true)][string]$OpenSCAD,
    [string]$Node = 'node'
)
$ErrorActionPreference = 'Stop'
$root = Split-Path $PSScriptRoot -Parent
if (-not (Test-Path -LiteralPath $OpenSCAD -PathType Leaf)) { throw 'Supply an existing OpenSCAD executable.' }
& $Node (Join-Path $root 'scripts\antenna-options.cjs') --check
if ($LASTEXITCODE -ne 0) { throw 'Regenerate option parameters first.' }
$logs = Join-Path $root '.tools\antenna-options'
$parts = Join-Path $PSScriptRoot 'options-stl'
New-Item -ItemType Directory -Force -Path $logs,$parts | Out-Null
$scad = Join-Path $PSScriptRoot 'antenna_options.scad'
function Export-Option([string]$Name,[string]$Destination,[string[]]$Extra) {
    $stderr = Join-Path $logs "$Name.stderr.log"
    $stdout = Join-Path $logs "$Name.stdout.log"
    $arguments = @('-o',"`"$Destination`"") + $Extra + @("`"$scad`"")
    $process = Start-Process -FilePath $OpenSCAD -ArgumentList $arguments -Wait -PassThru -NoNewWindow `
        -RedirectStandardError $stderr -RedirectStandardOutput $stdout
    if ($process.ExitCode -ne 0 -or -not (Test-Path -LiteralPath $Destination)) { throw "Option export failed: $Name" }
    if (Select-String -LiteralPath @($stderr,$stdout) -Pattern 'ERROR:|WARNING:') { throw "Option export diagnostic: $Name" }
}
$pending = Join-Path $parts 'support.pending.stl'
Export-Option 'support' $pending @('-D','ao_part=\"support\"','--export-format','binstl')
& $Node (Join-Path $root 'tests\mechanical-stl.cjs') $pending
if ($LASTEXITCODE -ne 0) { throw 'Support coupon mesh invalid.' }
Move-Item -LiteralPath $pending -Destination (Join-Path $parts 'support.stl') -Force
$names = @('EB-145','QFH-145','EB-435','QFH-435')
for ($i=0; $i -lt $names.Count; $i++) {
    Export-Option $names[$i] (Join-Path $root "docs\assembly\options\$($names[$i])-cad.png") `
        @('-D',"ao_model=$i",'--imgsize=1200,800','--projection=o','--camera=1100,-1500,1000,0,0,300','--viewall','--autocenter','--colorscheme=Tomorrow')
}
Write-Output 'Four CAD previews and one closed support coupon exported. No RF or structural acceptance.'
