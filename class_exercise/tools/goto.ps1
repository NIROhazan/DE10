# GOTO.bat = goto.ps1: reads goto.txt (TOPIC n [minutes], QUESTION nn [minutes] or MINUTE m), sets this computer's lesson clock so that
# that moment of the lesson is NOW (lesson_start.txt, which lesson.ps1 prefers over START), then runs the lesson.
# The progress stays. Kept ASCII for PowerShell 5.1.
$ErrorActionPreference = "Stop"
Set-Location (Split-Path $PSScriptRoot -Parent)

$mins = @()
foreach ($l in [IO.File]::ReadAllLines((Join-Path $PSScriptRoot "lesson.txt"))) {
	if ($l -match '^\s*TOPIC\s+([\d.]+)\s*\|\s*(.+?)\s*\|\s*(.+?)\s*$') {
		$mins += [pscustomobject]@{ Min = [double]$Matches[1]; Name = $Matches[2]; Qs = @($Matches[3] -split '\s+' | Where-Object { $_ }) }
	}
}
$total = ($mins | Measure-Object Min -Sum).Sum

function Fail($t) {
	Write-Host ""
	Write-Host "  $t" -ForegroundColor Red
	Write-Host "  Fix goto.txt (open it in Notepad) and run GOTO.bat again." -ForegroundColor Yellow
	exit 1
}

$f = Join-Path (Get-Location) "goto.txt"
if (-not (Test-Path $f)) { Fail "goto.txt is missing." }
$line = @([IO.File]::ReadAllLines($f) | Where-Object { $_ -notmatch '^\s*(#|$)' }) | Select-Object -First 1
if (-not $line) { Fail "goto.txt has no line - write for example:  TOPIC 2" }

if ($line -match '^\s*TOPIC\s+(\d+)(?:\s+([\d.]+))?\s*$') {
	$n = [int]$Matches[1]
	$into = if ($Matches[2]) { [double]$Matches[2] } else { 0 }
	if ($n -lt 1 -or $n -gt $mins.Count) { Fail "There are $($mins.Count) topics - TOPIC 1 to TOPIC $($mins.Count)." }
	if ($into -ge $mins[$n - 1].Min) { Fail "Topic $n is $($mins[$n - 1].Min) minutes long - give fewer minutes than that." }
	$offset = $into
	for ($i = 0; $i -lt $n - 1; $i++) { $offset += $mins[$i].Min }
} elseif ($line -match '^\s*QUESTION\s+Q?(\d{1,2})(?:\s+([\d.]+))?\s*$') {
	$first = "Q{0:D2}" -f [int]$Matches[1]
	$into = if ($Matches[2]) { [double]$Matches[2] } else { 0 }
	$n = 0
	for ($i = 0; $i -lt $mins.Count; $i++) { if ($mins[$i].Qs -contains $first) { $n = $i + 1 } }
	if ($n -eq 0) { Fail "There is no question $first in the lesson." }
	if ($into -ge $mins[$n - 1].Min) { Fail "Its topic is $($mins[$n - 1].Min) minutes long - give fewer minutes than that." }
	$offset = $into
	for ($i = 0; $i -lt $n - 1; $i++) { $offset += $mins[$i].Min }
} elseif ($line -match '^\s*MINUTE\s+([\d.]+)\s*$') {
	$offset = [double]$Matches[1]
	if ($offset -ge $total) { Fail "The lesson is $total minutes long - give fewer minutes than that." }
} else {
	Fail "I do not understand '$($line.Trim())'. Write TOPIC 2, TOPIC 2 10, QUESTION 13, QUESTION 13 10 or MINUTE 45."
}

if (-not (Get-Variable first -ErrorAction SilentlyContinue)) { $first = "" }
$start = (Get-Date).AddMinutes(-$offset)
[IO.File]::WriteAllText((Join-Path (Get-Location) "lesson_start.txt"), $start.ToString("o"))
Write-Host ""
Write-Host "  Going to '$($line.Trim())': $offset minutes into the lesson." -ForegroundColor Green
Start-Sleep -Seconds 2
& (Join-Path $PSScriptRoot "lesson.ps1") -First $first
exit $LASTEXITCODE
