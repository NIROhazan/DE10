# The lesson runner: LESSON.bat = lesson.ps1. Runs tools\lesson.txt by the clock: before START a countdown,
# then each topic for its minutes - its questions one after another (run.ps1 -Deadline = the topic's end),
# then the next topic. A question already done (progress.txt) is skipped. Kept ASCII for PowerShell 5.1.
param([string]$Schedule = "", [string]$Start = "", [string]$First = "")	# -First Q13: open that question first (GOTO.bat)

$ErrorActionPreference = "Stop"
Set-Location (Split-Path $PSScriptRoot -Parent)
. (Join-Path $PSScriptRoot "common.ps1")
if (-not $Schedule) { $Schedule = Join-Path $PSScriptRoot "lesson.txt" }

# ---------------------------------------------------------------- the schedule
$startText = "now"; $topics = @()
foreach ($l in [IO.File]::ReadAllLines($Schedule, $script:utf8)) {
	if ($l -match '^\s*START\s+(\S+)') { $startText = $Matches[1] }
	elseif ($l -match '^\s*TOPIC\s+([\d.]+)\s*\|\s*(.+?)\s*\|\s*(.+?)\s*$') {
		$topics += [pscustomobject]@{ Min = [double]$Matches[1]; Name = $Matches[2]; Qs = @($Matches[3] -split '\s+' | Where-Object { $_ }) }
	}
}
if ($Start) { $startText = $Start }
if ($topics.Count -eq 0) { Write-Host "No TOPIC lines in $Schedule." -ForegroundColor Red; exit 1 }
# lesson_start.txt = this computer's own start: written on the first launch of a START now lesson (leaving and
# coming back does not restart the clock), or by the instructor's reset_time.bat (a personal clock, e.g. after a
# technical problem). When it exists it wins over START; reset_lesson.bat deletes it (back to the class clock).
$startFile = Join-Path (Get-Location) "lesson_start.txt"
$back = $false
if (Test-Path $startFile) {
	$t = [datetime]::Parse(([IO.File]::ReadAllText($startFile)).Trim(), $null, [Globalization.DateTimeStyles]::RoundtripKind).ToLocalTime()
	$back = $true
} elseif ($startText -eq "now") {
	$t = Get-Date
	[IO.File]::WriteAllText($startFile, $t.ToString("o"))
} else {
	$t = [datetime]::ParseExact($startText, "HH:mm", $null)
}
foreach ($tp in $topics) {
	$tp | Add-Member Begin $t
	$t = $t.AddMinutes($tp.Min)
	$tp | Add-Member End $t
}
$qs = Read-Questions
foreach ($tp in $topics) { foreach ($x in $tp.Qs) { if (-not $qs.Contains($x)) { Write-Host "lesson.txt: there is no $x." -ForegroundColor Red; exit 1 } } }

$sid = Get-StudentId
$env:CE_LESSON = "1"		# run.ps1 runs only from here
if ((Test-Path "progress.txt") -and ([IO.File]::ReadAllText((Join-Path (Get-Location) "progress.txt")) -match "(?m)^$sid ")) { $back = $true }
function Test-Done($qid) { return ((Get-Progress $sid $qid) -ge ($qs[$qid].NS - 1)) }
function Show-Plan($cur, $title, $color) {
	Clear-Host
	Write-Host ""
	Write-Host "  $title" -ForegroundColor $color
	Write-Host ""
	for ($i = 0; $i -lt $topics.Count; $i++) {
		$tp = $topics[$i]
		$done = @($tp.Qs | Where-Object { Test-Done $_ }).Count
		$mark = if ($i -eq $cur) { ">" } else { " " }
		$line = "  $mark {0:HH:mm}-{1:HH:mm}   {2,-52} {3}/{4} done" -f $tp.Begin, $tp.End, $tp.Name, $done, $tp.Qs.Count
		if ($i -eq $cur) { Write-Host $line -ForegroundColor Yellow } else { Write-Host $line }
	}
	Write-Host ""
}
function Wait-Until($when, $cur, $title, $color) {
	Show-Plan $cur $title $color
	while ((Get-Date) -lt $when) {
		$left = $when - (Get-Date)
		$Host.UI.RawUI.WindowTitle = "Class lesson - next in {0:mm\:ss}" -f $left
		Write-Host ("`r  Starts in {0:hh\:mm\:ss}   " -f $left) -NoNewline -ForegroundColor Cyan
		Start-Sleep -Milliseconds 500
	}
	Write-Host ""
}

# ---------------------------------------------------------------- the lesson
while ($true) {
	$now = Get-Date
	if ($now -lt $topics[0].Begin) { Wait-Until $topics[0].Begin 0 "The lesson starts at $('{0:HH:mm}' -f $topics[0].Begin). Today:" Cyan; continue }
	$cur = -1
	for ($i = 0; $i -lt $topics.Count; $i++) { if ($now -ge $topics[$i].Begin -and $now -lt $topics[$i].End) { $cur = $i } }
	if ($cur -lt 0) {
		Show-Plan -1 "The lesson is over. Your codes are in moodle.txt - hand it in on Moodle." Green
		exit 0
	}
	$tp = $topics[$cur]
	$next = @($tp.Qs | Where-Object { -not (Test-Done $_) }) | Select-Object -First 1
	if ($First) {
		if (($tp.Qs -contains $First) -and -not (Test-Done $First)) { $next = $First }
		elseif (Test-Done $First) { Write-Host "  $First is already done - going on with the topic." -ForegroundColor Green; Start-Sleep -Seconds 3 }
		$First = ""
	}
	if (-not $next) {
		$after = if ($cur + 1 -lt $topics.Count) { "The next topic starts at $('{0:HH:mm}' -f $tp.End)." } else { "That was the last topic." }
		Wait-Until $tp.End $cur "Well done - every question of this topic is done!  $after" Green
		continue
	}
	Show-Plan $cur "Topic $($cur + 1) of $($topics.Count): $($tp.Name) - next question $next" Yellow
	if ($back) {
		Write-Host ("  Welcome back! Your progress is saved, and the lesson went on while you were away - now topic {0}, until {1:HH:mm}." -f ($cur + 1), $tp.End) -ForegroundColor Green
		$back = $false
		Start-Sleep -Seconds 4
	}
	Start-Sleep -Seconds 2
	& (Join-Path $PSScriptRoot "run.ps1") -Only $next -Deadline $tp.End.ToString("o")
	$code = $LASTEXITCODE
	if ($code -eq 2) {
		Write-Host ""
		Write-Host "  Time is up for this topic - your progress is saved. On to the next topic." -ForegroundColor Yellow
		Start-Sleep -Seconds 4
	} elseif ($code -ne 0) {
		Write-Host ""
		$null = Read-Host "  Something went wrong (see above). Enter = try again"
	} else {
		Start-Sleep -Seconds 3
	}
}
