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
$posFile = Join-Path (Get-Location) "lesson_pos.txt"		# the question the student is at (see the lesson loop)
$env:CE_LESSON = "1"		# run.ps1 runs only from here
if ((Test-Path "progress.txt") -and ([IO.File]::ReadAllText((Join-Path (Get-Location) "progress.txt")) -match "(?m)^$sid ")) { $back = $true }
function Test-Done($qid) { return ((Get-Progress $sid $qid) -ge ($qs[$qid].NS - 1)) }
# $title: one line or several (Hebrew and English lines apart); the plan rows are Hebrew (topic names from lesson.txt)
function Show-Plan($cur, $title, $color) {
	Clear-Host
	Write-Host ""
	@($title) | ForEach-Object { Write-Line $_ $color }
	Write-Host ""
	for ($i = 0; $i -lt $topics.Count; $i++) {
		$tp = $topics[$i]
		$done = @($tp.Qs | Where-Object { Test-Done $_ }).Count
		$line = (U "plan_row") -f ('{0:HH:mm}' -f $tp.Begin), ('{0:HH:mm}' -f $tp.End), $tp.Name, $done, $tp.Qs.Count
		Write-Line $line $(if ($i -eq $cur) { "Yellow" } else { "Gray" })
	}
	Write-Host ""
}
function Wait-Until($when, $cur, $title, $color) {
	Show-Plan $cur $title $color
	$w = 100
	try { $w = [Math]::Max(60, $Host.UI.RawUI.WindowSize.Width - 2) } catch { }
	while ((Get-Date) -lt $when) {
		$left = $when - (Get-Date)
		$Host.UI.RawUI.WindowTitle = "Class lesson - next in {0:mm\:ss}" -f $left
		$v = ConvertTo-Visual ("{0}  {1:hh\:mm\:ss}" -f (U "countdown"), $left)
		Write-Host ("`r" + $v.PadLeft($w)) -NoNewline -ForegroundColor Cyan
		Start-Sleep -Milliseconds 500
	}
	Write-Host ""
}

# ---------------------------------------------------------------- the lesson
while ($true) {
	$now = Get-Date
	if ($now -lt $topics[0].Begin) { Wait-Until $topics[0].Begin 0 ((U "starts_at") -f ('{0:HH:mm}' -f $topics[0].Begin)) Cyan; continue }
	$cur = -1
	for ($i = 0; $i -lt $topics.Count; $i++) { if ($now -ge $topics[$i].Begin -and $now -lt $topics[$i].End) { $cur = $i } }
	if ($cur -lt 0) {
		Show-Plan -1 @((U "over"), (U "over_en")) Green
		exit 0
	}
	$tp = $topics[$cur]
	# by question number: from the saved position (lesson_pos.txt - the question last opened, or chosen by GOTO) on,
	# the first one not done yet; after the last one, the questions skipped earlier; all done - wait for the next topic
	$review = ""
	if ($First) {			# chosen in goto.txt: a question already done opens again from step 1 (review)
		[IO.File]::WriteAllText($posFile, $First)
		if ((Test-Done $First) -and ($tp.Qs -contains $First)) { $review = $First }
		$First = ""
	}
	$pos = if (Test-Path $posFile) { ([IO.File]::ReadAllText($posFile)).Trim() } else { "" }
	$from = [Math]::Max(0, [array]::IndexOf($tp.Qs, $pos))
	$next = @($tp.Qs[$from..($tp.Qs.Count - 1)] | Where-Object { -not (Test-Done $_) }) | Select-Object -First 1
	if (-not $next) {		# past the last question: back to the topic's questions not done yet (skipped earlier)
		$next = @($tp.Qs | Where-Object { -not (Test-Done $_) }) | Select-Object -First 1
	}
	if ($review) { $next = $review }
	if (-not $next) {
		$after = if ($cur + 1 -lt $topics.Count) { (U "next_topic_at") -f ('{0:HH:mm}' -f $tp.End) } else { U "last_topic" }
		Wait-Until $tp.End $cur @((U "end_topic"), $after) Green
		continue
	}
	[IO.File]::WriteAllText($posFile, $next)
	Show-Plan $cur @(((U "topic_now") -f ($cur + 1), $topics.Count, $tp.Name), ((U "next_q") -f $next)) Yellow
	if ($back) {
		Write-Line ((U "welcome") -f ($cur + 1), ('{0:HH:mm}' -f $tp.End)) Green
		$back = $false
		Start-Sleep -Seconds 4
	}
	Start-Sleep -Seconds 2
	& (Join-Path $PSScriptRoot "run.ps1") -Only $next -Deadline $tp.End.ToString("o") -Review:([bool]$review)
	$code = $LASTEXITCODE
	if ($code -eq 2) {
		Write-Host ""
		Write-Line (U "timeup_next") Yellow
		Start-Sleep -Seconds 4
	} elseif ($code -ne 0) {
		Write-Host ""
		Write-Line (U "wrong") Yellow
		$null = Read-Host "  Enter"
	} else {
		Start-Sleep -Seconds 3
	}
}
