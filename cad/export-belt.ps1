param(
 [string]$OpenSCAD="$PSScriptRoot\tools\openscad-2021.01\openscad.exe",
 [string]$Node="C:\Users\anatol.lopez\.copilot\session-state\93e9ed63-2da0-4d79-90a4-39add6c2b259\files\tools\node-v22.16.0-win-x64\node.exe"
)
$ErrorActionPreference='Stop'
$out=Join-Path $PSScriptRoot 'belt-stl'
New-Item -ItemType Directory -Path $out -Force | Out-Null
foreach($part in @('base','encoder_support','cup608','cup6000')) {
 $file=Join-Path $out "$part.stl"
 $log=Join-Path $out "$part.render.log"
 $arguments=@('-o',"`"$file`"",'-D',('belt_part=\"{0}\"' -f $part),"`"$(Join-Path $PSScriptRoot 'belt_station.scad')`"")
 $process=Start-Process $OpenSCAD -ArgumentList $arguments -Wait -PassThru -NoNewWindow `
  -RedirectStandardError $log -RedirectStandardOutput (Join-Path $out "$part.stdout.log")
 if($process.ExitCode-ne 0 -or !(Test-Path $file)){throw "Render failed: $part"}
 if(Select-String $log -Pattern 'ERROR:|WARNING:'){throw "OpenSCAD diagnostic: $part"}
 & $Node (Join-Path $PSScriptRoot '..\tests\mechanical-stl.cjs') $file
 if($LASTEXITCODE-ne 0){throw "Manifold check failed: $part"}
}
foreach($entry in @(
 @('belt-assembly.csg','assembly'),
 @('belt-front-plate.dxf','front_plate_dxf'),
 @('belt-rear-plate.dxf','rear_plate_dxf'),
 @('belt-tray.dxf','tray_dxf'))) {
 $file=Join-Path $PSScriptRoot $entry[0]
 $arguments=@('-o',"`"$file`"",'-D',('belt_part=\"{0}\"' -f $entry[1]),"`"$(Join-Path $PSScriptRoot 'belt_station.scad')`"")
 $log=Join-Path $out "$($entry[0]).log"
 $process=Start-Process $OpenSCAD -ArgumentList $arguments -Wait -PassThru -NoNewWindow `
  -RedirectStandardError $log -RedirectStandardOutput (Join-Path $out "$($entry[0]).stdout.log")
 if($process.ExitCode-ne 0 -or !(Test-Path $file)){throw "Metal/assembly export failed: $($entry[0])"}
 if(Select-String $log -Pattern 'ERROR:|WARNING:'){throw "Export diagnostic: $($entry[0])"}
}
Write-Output 'Four new printable belt components rendered; purchased metal/belt envelopes are CSG only.'
