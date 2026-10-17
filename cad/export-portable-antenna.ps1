param(
    [Parameter(Mandatory=$true)][string]$OpenSCAD,
    [string]$Node = 'node'
)
$ErrorActionPreference = 'Stop'
$root = Split-Path $PSScriptRoot -Parent
$scad = Join-Path $PSScriptRoot 'portable_antenna.scad'
$figures = Join-Path $root 'docs\assembly\portable'
$parts = Join-Path $PSScriptRoot 'portable-stl'
$logs = Join-Path $root '.tools\antenna-portable'
if (-not (Test-Path -LiteralPath $OpenSCAD -PathType Leaf)) { throw 'Supply an existing OpenSCAD executable.' }
& $Node (Join-Path $root 'scripts\portable-antenna.cjs') --check
if ($LASTEXITCODE -ne 0) { throw 'Regenerate PF-01 parameters first.' }
New-Item -ItemType Directory -Force -Path $figures,$parts,$logs | Out-Null
function Export-Part([string]$Selector,[string]$Destination,[string[]]$Extra) {
    $log = Join-Path $logs "$Selector.log"
    $arguments = @('-o',"`"$Destination`"",'-D',('pf_part=\"{0}\"' -f $Selector)) + $Extra + @("`"$scad`"")
    $process = Start-Process -FilePath $OpenSCAD -ArgumentList $arguments -Wait -PassThru -NoNewWindow `
        -RedirectStandardError $log -RedirectStandardOutput (Join-Path $logs "$Selector.stdout.log")
    if ($process.ExitCode -ne 0 -or -not (Test-Path -LiteralPath $Destination)) {
        throw "PF-01 export failed: $Selector; see $log"
    }
    if (Select-String -LiteralPath @($log,(Join-Path $logs "$Selector.stdout.log")) -Pattern 'ERROR:|WARNING:') {
        throw "PF-01 export diagnostic: $Selector"
    }
}
foreach ($part in @('hub','arm')) {
    $pending = Join-Path $parts "$part.pending.stl"
    Export-Part $part $pending @('--export-format','binstl')
    & $Node (Join-Path $root 'tests\mechanical-stl.cjs') $pending
    if ($LASTEXITCODE -ne 0) { throw "PF-01 mesh check failed: $part" }
    Move-Item -LiteralPath $pending -Destination (Join-Path $parts "$part.stl") -Force
}
$views = @(
    @('deployed','1100,-1500,1100,0,0,220'),
    @('front','0,0,1800,0,0,220'),
    @('folded','600,-800,600,0,0,125'),
    @('hinge','180,-240,190,15,0,8'),
    @('reflector','1100,-1300,950,0,0,10')
)
foreach ($view in $views) {
    Export-Part $view[0] (Join-Path $figures "PF-$($view[0]).png") `
        @('--imgsize=1200,800','--projection=o',('--camera='+$view[1]),'--viewall','--autocenter','--colorscheme=Tomorrow')
}
foreach ($check in @('hinge-clearance','stow-clearance')) {
    $destination = Join-Path $logs "$check.stl"
    if (Test-Path -LiteralPath $destination) { throw "Use a fresh diagnostic path: $destination" }
    $log = Join-Path $logs "$check.log"
    $arguments = @('-o',"`"$destination`"",'-D',('pf_part=\"{0}\"' -f $check),"`"$scad`"")
    $process = Start-Process -FilePath $OpenSCAD -ArgumentList $arguments -Wait -PassThru -NoNewWindow `
        -RedirectStandardError $log -RedirectStandardOutput (Join-Path $logs "$check.stdout.log")
    $diagnostics = @($log,(Join-Path $logs "$check.stdout.log"))
    if ($process.ExitCode -notin @(0,1) -or (Test-Path -LiteralPath $destination) -or
        -not (Select-String -LiteralPath $diagnostics -SimpleMatch 'Current top level object is empty.')) {
        throw "Nominal collision or unexpected OpenSCAD result: $check; see $log"
    }
    if (Select-String -LiteralPath $diagnostics -Pattern 'ERROR:|WARNING:') { throw "Clearance diagnostic: $check" }
    Write-Output "$check : empty intersection (nominal sampled CAD only)"
}
Write-Output 'PF-01 exported: two printable candidate meshes, five views. No RF or load acceptance.'
