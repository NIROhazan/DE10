# Builds a week's student kit and its one-file installer:
#   C:\DE10\dist\labN_kit.zip          labN_kit\weekN (LESSON.bat, questions.txt, lesson.txt, label.txt, README.md,
#                                      QUESTIONS.md, sof\*.sof) + labN_kit\tools (the shared lesson tools)
#   C:\DE10\dist\labN_kit_install.bat  make_installer.ps1 around the zip: the file the student downloads and double-clicks
#   powershell -NoProfile -ExecutionPolicy Bypass -File make_kit.ps1 -Week 6
# Per-computer files (student.txt, progress.txt, moodle.txt, lesson_*.txt, link_state.txt, program.log) never go in.
# Kept ASCII for PowerShell 5.1.
param([Parameter(Mandatory = $true)][int]$Week, [string]$Root = "C:\DE10")

$ErrorActionPreference = "Stop"
Add-Type -AssemblyName System.IO.Compression.FileSystem
$src = Join-Path $Root "week$Week"
$kit = "lab${Week}_kit"
$dist = Join-Path $Root "dist"
$need = @("LESSON.bat", "questions.txt", "lesson.txt", "label.txt")
foreach ($f in $need) { if (-not (Test-Path (Join-Path $src $f))) { throw "week$Week has no $f" } }
$sofs = @(Get-ChildItem (Join-Path $src "sof") -Filter *.sof -ErrorAction SilentlyContinue)
if ($sofs.Count -eq 0) { throw "week$Week\sof has no .sof files" }

# every question of lesson.txt must have its board
$qs = @(Get-Content (Join-Path $src "lesson.txt") -Encoding UTF8 | Where-Object { $_ -match '^TOPIC ' } |
	ForEach-Object { ($_ -split '\|')[2].Trim() -split '\s+' })
$miss = @($qs | Where-Object { -not (Test-Path (Join-Path $src "sof\$_.sof")) })
if ($miss.Count) { throw "lesson.txt questions with no .sof: $($miss -join ' ')" }

$stage = Join-Path $env:TEMP "${kit}_stage"
if (Test-Path $stage) { Remove-Item -Recurse -Force $stage }
$wk = Join-Path $stage "$kit\week$Week"
New-Item -ItemType Directory -Force (Join-Path $wk "sof") | Out-Null
foreach ($f in $need + @("README.md", "QUESTIONS.md")) {
	if (Test-Path (Join-Path $src $f)) { Copy-Item (Join-Path $src $f) $wk }
}
$sofs | Copy-Item -Destination (Join-Path $wk "sof")
Copy-Item (Join-Path $Root "tools") (Join-Path $stage $kit) -Recurse

New-Item -ItemType Directory -Force $dist | Out-Null
$zip = Join-Path $dist "$kit.zip"
if (Test-Path $zip) { Remove-Item -Force $zip }
Add-Type -AssemblyName System.IO.Compression
$z = [IO.Compression.ZipFile]::Open($zip, "Create")		# entry names with "/" (PowerShell 5.1 would write "\")
foreach ($f in Get-ChildItem $stage -Recurse -File) {
	$name = $f.FullName.Substring($stage.Length + 1).Replace("\", "/")
	[void][IO.Compression.ZipFileExtensions]::CreateEntryFromFile($z, $f.FullName, $name)
}
$z.Dispose()
Remove-Item -Recurse -Force $stage

& (Join-Path $PSScriptRoot "make_installer.ps1") -Zip $zip
$bat = Join-Path $dist "${kit}_install.bat"
Write-Host ("  {0}  ({1} boards, {2:N1} MB)" -f $bat, $sofs.Count, ((Get-Item $bat).Length / 1MB))
