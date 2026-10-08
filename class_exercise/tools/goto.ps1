# GOTO.bat = goto.ps1: reads goto.txt - TOPIC n, or TOPIC n QUESTION k (the k-th question of topic n) - starts topic n
# now with its full time (lesson_start.txt, which lesson.ps1 prefers over START) and opens that question first
# (lesson.ps1 -First). No choosing of minutes. The progress stays. Kept ASCII for PowerShell 5.1.
$ErrorActionPreference = "Stop"
Set-Location (Split-Path $PSScriptRoot -Parent)

$topics = @()
foreach ($l in [IO.File]::ReadAllLines((Join-Path $PSScriptRoot "lesson.txt"))) {
	if ($l -match '^\s*TOPIC\s+([\d.]+)\s*\|\s*(.+?)\s*\|\s*(.+?)\s*$') {
		$topics += [pscustomobject]@{ Min = [double]$Matches[1]; Name = $Matches[2]; Qs = @($Matches[3] -split '\s+' | Where-Object { $_ }) }
	}
}

function Fail($t) {
	Write-Host ""
	Write-Host "  $t" -ForegroundColor Red
	Write-Host ""
	for ($i = 0; $i -lt $topics.Count; $i++) {
		Write-Host ("    TOPIC {0}: {1}  ({2} questions)" -f ($i + 1), $topics[$i].Name, $topics[$i].Qs.Count)
	}
	Write-Host ""
	Write-Host "  Fix goto.txt (open it in Notepad) and run GOTO.bat again." -ForegroundColor Yellow
	exit 1
}

$f = Join-Path (Get-Location) "goto.txt"
if (-not (Test-Path $f)) { Fail "goto.txt is missing." }
# every non-comment line together: "TOPIC 1 QUESTION 3" on one line, or TOPIC 1 and QUESTION 3 on two lines
$line = (@([IO.File]::ReadAllLines($f) | Where-Object { $_ -notmatch '^\s*(#|$)' } | ForEach-Object { $_.Trim() }) -join " ")
if (-not $line) { Fail "goto.txt has no line - write for example:  TOPIC 2   or   TOPIC 1 QUESTION 3" }
if ($line -notmatch '^\s*TOPIC\s+(\d+)(?:\s+QUESTION\s+(\d+))?\s*$') {
	Fail "I do not understand '$($line.Trim())'. Write  TOPIC 2   or   TOPIC 1 QUESTION 3"
}
$n = [int]$Matches[1]
$k = if ($Matches[2]) { [int]$Matches[2] } else { 1 }
if ($n -lt 1 -or $n -gt $topics.Count) { Fail "There is no topic $n - the lesson has TOPIC 1 to TOPIC $($topics.Count)." }
$tp = $topics[$n - 1]
if ($k -lt 1 -or $k -gt $tp.Qs.Count) { Fail "Topic $n has $($tp.Qs.Count) questions - QUESTION 1 to QUESTION $($tp.Qs.Count)." }
$first = $tp.Qs[$k - 1]

$offset = 0
for ($i = 0; $i -lt $n - 1; $i++) { $offset += $topics[$i].Min }
$start = (Get-Date).AddMinutes(-$offset)
[IO.File]::WriteAllText((Join-Path (Get-Location) "lesson_start.txt"), $start.ToString("o"))
Write-Host ""
Write-Host "  Topic $n ($($tp.Name)) starts now, with its question $k of $($tp.Qs.Count) ($first)." -ForegroundColor Green
Start-Sleep -Seconds 2
& (Join-Path $PSScriptRoot "lesson.ps1") -First $first
exit $LASTEXITCODE
