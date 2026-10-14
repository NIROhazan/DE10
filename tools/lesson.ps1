# The lesson runner: weekN\LESSON.bat runs this in the week's folder (questions.txt, lesson.txt, sof\ are there).
# No class clock: the lesson's time starts when the student types the student ID (lesson_start.txt), and lasts the
# minutes of all the TOPIC lines of lesson.txt together. The topic times are only a recommendation. A menu shows the
# questions of one topic at a time: left / right arrows = another topic, up / down = a question, Enter = open it -
# only then is the board programmed (run.ps1).
# Kept ASCII for PowerShell 5.1.
param([string]$Schedule = "", [string]$First = "")	# -First Q13: the menu stands on that question

$ErrorActionPreference = "Stop"
. (Join-Path $PSScriptRoot "common.ps1")
if (-not $Schedule) { $Schedule = Join-Path (Get-Location) "lesson.txt" }

# Quartus cannot program or talk to the board from a folder whose path has Hebrew (or other non-ASCII) letters,
# e.g. the Hebrew desktop folder of OneDrive: say so at once instead of failing later.
if ((Get-Location).Path -match '[^\x00-\x7F]') {
	Write-Host ""
	Write-Line (U "path_he") Red
	Write-Line (U "path_he_copy") Yellow
	Write-Line ((U "path_he_en") -f "C:\DE10") Yellow
	Write-Host ""
	exit 1
}

# ---------------------------------------------------------------- the topics
$topics = @()
foreach ($l in [IO.File]::ReadAllLines($Schedule, $script:utf8)) {
	if ($l -match '^\s*TOPIC\s+([\d.]+)\s*\|\s*(.+?)\s*\|\s*(.+?)\s*$') {
		$topics += [pscustomobject]@{ Min = [double]$Matches[1]; Name = $Matches[2]; Qs = @($Matches[3] -split '\s+' | Where-Object { $_ }) }
	}
}
if ($topics.Count -eq 0) { Write-Host "No TOPIC lines in $Schedule." -ForegroundColor Red; exit 1 }
$qs = Read-Questions
foreach ($tp in $topics) { foreach ($x in $tp.Qs) { if (-not $qs.Contains($x)) { Write-Host "lesson.txt: there is no $x." -ForegroundColor Red; exit 1 } } }

# ---------------------------------------------------------------- the student and the lesson's own clock
$sid = Get-StudentId
# lesson_start.txt = this computer's start: written right after the student ID (closing and opening LESSON.bat again
# does not restart the clock), or set by the instructor's reset_time.bat; reset_lesson.bat deletes it.
$startFile = Join-Path (Get-Location) "lesson_start.txt"
$back = $false
$t = $null
if (Test-Path $startFile) {
	try { $t = [datetime]::Parse(([IO.File]::ReadAllText($startFile)).Trim(), $null, [Globalization.DateTimeStyles]::RoundtripKind).ToLocalTime() } catch { }
	$len = ($topics | Measure-Object -Property Min -Sum).Sum
	if ($t -and (Get-Date) -gt $t.AddMinutes($len + 120)) { $t = $null }	# that lesson ended over 2 hours ago: a new lesson
	if ($t) { $back = $true }
}
if (-not $t) {
	$t = Get-Date
	[IO.File]::WriteAllText($startFile, $t.ToString("o"))
}
foreach ($tp in $topics) {
	$tp | Add-Member Begin $t
	$t = $t.AddMinutes($tp.Min)
	$tp | Add-Member End $t
}
$lessonEnd = $topics[-1].End
$posFile = Join-Path (Get-Location) "lesson_pos.txt"		# the question the student opened last
$env:CE_LESSON = "1"		# run.ps1 runs only from here
function Test-Done($qid) { return ((Get-Progress $sid $qid) -ge ($qs[$qid].NS - 1)) }
function Topic-Of($qid) { for ($i = 0; $i -lt $topics.Count; $i++) { if ($topics[$i].Qs -contains $qid) { return $i } }; return 0 }

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

# The question menu: one topic per page. Left / right = another topic, up / down = a question, Enter = open it.
# Returns the chosen question, or "" when the lesson's time is over.
function Select-Question($default) {
	$p = Topic-Of $default
	$i = [Math]::Max(0, [array]::IndexOf($topics[$p].Qs, $default))
	$draw = $true
	while ($true) {
		if ((Get-Date) -ge $lessonEnd) { return "" }
		if ($draw) {
			$tp = $topics[$p]
			Show-Plan $p @(((U "pick_topic") -f ($p + 1), $topics.Count, $tp.Name), ((U "lesson_end") -f ('{0:HH:mm}' -f $lessonEnd)), (U "pick_title")) Yellow
			for ($j = 0; $j -lt $tp.Qs.Count; $j++) {
				$x = $tp.Qs[$j]
				$st = if (Test-Done $x) { U "pick_done" } elseif ((Get-Progress $sid $x) -gt 0) { U "pick_started" } else { "" }
				$row = (U "pick_row") -f ($j + 1), $qs[$x].Title, $st
				if ($j -eq $i) { Write-Line ("<<  " + $row) Yellow } else { Write-Line $row $(if (Test-Done $x) { "Green" } else { "Gray" }) }
			}
			Write-Host ""
			Write-Line (U "pick_keys") Cyan
			$draw = $false
		}
		Start-Sleep -Milliseconds 100
		try {
			while ([Console]::KeyAvailable) {
				$key = [Console]::ReadKey($true)
				if ($key.Key -eq "UpArrow" -and $i -gt 0) { $i--; $draw = $true }
				elseif ($key.Key -eq "DownArrow" -and $i -lt $topics[$p].Qs.Count - 1) { $i++; $draw = $true }
				elseif ($key.Key -eq "RightArrow" -and $p -lt $topics.Count - 1) { $p++; $i = 0; $draw = $true }	# right = the next topic (like the steps)
				elseif ($key.Key -eq "LeftArrow" -and $p -gt 0) { $p--; $i = 0; $draw = $true }
				elseif ($key.Key -eq "Enter") { return $topics[$p].Qs[$i] }
			}
		} catch { return $topics[$p].Qs[$i] }		# no console (a test run): the default question
	}
}

# the question the menu stands on first: the first one not done, from the last opened (or the current topic's) on
function Default-Question {
	$all = @($topics | ForEach-Object { $_.Qs })
	$pos = if (Test-Path $posFile) { ([IO.File]::ReadAllText($posFile)).Trim() } else { "" }
	if (-not $pos) {
		$now = Get-Date
		$cur = 0
		for ($i = 0; $i -lt $topics.Count; $i++) { if ($now -ge $topics[$i].Begin) { $cur = $i } }
		$pos = $topics[$cur].Qs[0]
	}
	$from = [Math]::Max(0, [array]::IndexOf($all, $pos))
	$q = @($all[$from..($all.Count - 1)] + $all | Where-Object { -not (Test-Done $_) }) | Select-Object -First 1
	if ($q) { return $q } else { return $all[0] }
}

# ---------------------------------------------------------------- the lesson
if ($back) {
	Show-Plan -1 @((U "welcome_back"), ((U "lesson_end") -f ('{0:HH:mm}' -f $lessonEnd))) Green
	Start-Sleep -Seconds 3
}
$prefer = if ($First) { $First } else { "" }		# the question the menu stands on (-First, or the arrows in a question)
while ($true) {
	if ((Get-Date) -ge $lessonEnd) {
		Show-Plan -1 @((U "over"), (U "over_en")) Green
		exit 0
	}
	$def = if ($prefer -and $qs.Contains($prefer)) { $prefer } else { Default-Question }
	$prefer = ""
	$pick = Select-Question $def
	if (-not $pick) { continue }			# the lesson's time is over
	[IO.File]::WriteAllText($posFile, $pick)
	$review = Test-Done $pick			# a finished question opens again from step 1 (review)
	& (Join-Path $PSScriptRoot "run.ps1") -Only $pick -Deadline $lessonEnd.ToString("o") -Review:([bool]$review)
	$code = $LASTEXITCODE
	$all = @($topics | ForEach-Object { $_.Qs })
	$ix = [array]::IndexOf($all, $pick)
	if ($code -eq 3) { $prefer = $all[[Math]::Min($all.Count - 1, $ix + 1)]; continue }	# down arrow in a question
	if ($code -eq 4) { $prefer = $all[[Math]::Max(0, $ix - 1)]; continue }			# up arrow in a question
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
