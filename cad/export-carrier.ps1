param(
 [string]$OpenSCAD="$PSScriptRoot\tools\openscad-2021.01\openscad.exe",
 [string]$Node="C:\Users\anatol.lopez\.copilot\session-state\93e9ed63-2da0-4d79-90a4-39add6c2b259\files\tools\node-v22.16.0-win-x64\node.exe"
)
$ErrorActionPreference='Stop'
$out=Join-Path $PSScriptRoot 'carrier-stl'
New-Item -ItemType Directory -Path $out -Force | Out-Null
foreach($part in @('base','lid','port40','port30')) {
 $file=Join-Path $out "$part.stl";$staged=Join-Path $out "$part.pending.stl";$log=Join-Path $out "$part.render.log"
 $args=@('--export-format','binstl','-o',"`"$staged`"",'-D',('carrier_part=\"{0}\"' -f $part),"`"$(Join-Path $PSScriptRoot 'carrier_enclosure.scad')`"")
 $proc=Start-Process $OpenSCAD -ArgumentList $args -Wait -PassThru -NoNewWindow `
  -RedirectStandardError $log -RedirectStandardOutput (Join-Path $out "$part.stdout.log")
 if($proc.ExitCode-ne 0 -or !(Test-Path $staged)){throw "Render failed: $part"}
 if(Select-String $log -Pattern 'ERROR:|WARNING:'){throw "Render diagnostic: $part"}
 & $Node (Join-Path $PSScriptRoot '..\tests\mechanical-stl.cjs') $staged
 if($LASTEXITCODE-ne 0){throw "STL check failed: $part"}
 Move-Item -LiteralPath $staged -Destination $file -Force
}
$file=Join-Path $PSScriptRoot 'carrier-assembly.csg'
$args=@('-o',"`"$file`"","`"$(Join-Path $PSScriptRoot 'carrier_enclosure.scad')`"")
$proc=Start-Process $OpenSCAD -ArgumentList $args -Wait -PassThru -NoNewWindow `
 -RedirectStandardError (Join-Path $out 'assembly.log')
if($proc.ExitCode-ne 0 -or !(Test-Path $file)){throw 'Carrier assembly CSG failed'}
$file=Join-Path $PSScriptRoot 'carrier-metal-mount.dxf'
$args=@('-o',"`"$file`"",'-D','carrier_part=\"mount_dxf\"',"`"$(Join-Path $PSScriptRoot 'carrier_enclosure.scad')`"")
$proc=Start-Process $OpenSCAD -ArgumentList $args -Wait -PassThru -NoNewWindow `
 -RedirectStandardError (Join-Path $out 'mount.log')
if($proc.ExitCode-ne 0 -or !(Test-Path $file)){throw 'Carrier stationary metal tray DXF failed'}
