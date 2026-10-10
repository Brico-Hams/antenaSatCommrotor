param(
    [string]$NodePath = 'node'
)

$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
$node = Get-Command $NodePath -ErrorAction Stop
$tests = @(Get-ChildItem (Join-Path $root 'tests') -Filter '*.test.cjs' |
    Select-Object -ExpandProperty FullName)
if ($tests.Count -eq 0) {
    throw 'No validation tests found.'
}
& $node.Source --test @tests
if ($LASTEXITCODE -ne 0) {
    throw 'Validation tests failed.'
}
& $node.Source (Join-Path $PSScriptRoot 'engineering-report.cjs')
if ($LASTEXITCODE -ne 0) {
    throw 'Engineering report failed.'
}
Write-Output 'Digital checks passed. Hardware and RF acceptance remain separate.'
