# Class exercise runner: Q01_GATE.bat = run.ps1 -Only Q01.
# Programs sof\Qnn.sof and talks to the board over the USB cable (tools\link.tcl in quartus_stp): it writes the
# student's login number and the step to start from into the board, and reads the board's step and code.
# So the student only flips switches and presses KEY2; the screen moves on by itself, and the code at the end
# goes into moodle.txt by itself. The board alone knows the answers and the codes.
# progress.txt keeps the last step passed: a closed window goes on from there, never from the start.
# -Deadline (from LESSON.bat): the end of the topic - the window title counts down, and at that time the question
# stops with exit code 2 (progress saved). Exit 0 = done, 1 = a problem with the board.
# Kept ASCII so Windows PowerShell 5.1 reads it without a BOM.
param([Parameter(Mandatory = $true)][string]$Only, [string]$Deadline = "")

$ErrorActionPreference = "Stop"
Set-Location (Split-Path $PSScriptRoot -Parent)
. (Join-Path $PSScriptRoot "common.ps1")
if ($env:CE_LESSON -ne "1") {		# questions open only through LESSON.bat (lesson.ps1 sets it)
	Write-Host ""
	Write-Line (U "only_lesson") Yellow
	Write-Line (U "only_lesson_en") Yellow
	exit 1
}

$qs = Read-Questions
if (-not $qs.Contains($Only)) { Write-Host "There is no $Only in tools\questions.txt." -ForegroundColor Red; exit 1 }
$q = $qs[$Only]
$dl = if ($Deadline) { [datetime]::Parse($Deadline, $null, [Globalization.DateTimeStyles]::RoundtripKind).ToLocalTime() } else { $null }
function Test-TimeUp {
	if (-not $dl) { return $false }
	$left = $dl - (Get-Date)
	if ($left.TotalSeconds -le 0) { return $true }
	$Host.UI.RawUI.WindowTitle = "$($q.Id) - {0:mm\:ss} left in this topic" -f $left
	return $false
}
$sid = Get-StudentId
$s = Get-Login $sid
$pub = Get-Pub $q.Id $s $q.NPub
$last = $q.NS - 1

$done = Get-Progress $sid $q.Id
if ($done -ge $last) {
	Write-Host ""
	Write-Line (U "already") Green
	Write-Line ("ce-$($q.Id): $(Get-SavedCode $q.Id)") Green
	exit 0
}
$from = $done + 1
if (Test-TimeUp) { exit 2 }

# ---------------------------------------------------------------- program the board
$qbin = @("C:\altera\13.0sp1\quartus\bin64", "C:\altera\13.0sp1\quartus\bin") |
	Where-Object { Test-Path (Join-Path $_ "quartus_pgm.exe") } | Select-Object -First 1
$sof = Join-Path (Get-Location) "sof\$($q.Id).sof"
if (-not $qbin) { Write-Host "  Quartus II 13.0sp1 not found under C:\altera." -ForegroundColor Red; exit 1 }
Get-Process quartus_stp -ErrorAction SilentlyContinue | Stop-Process -Force		# an old link from a closed window
Write-Host ""
Write-Line (U "prep")
$ErrorActionPreference = "Continue"
& (Join-Path $qbin "quartus_pgm.exe") -c USB-Blaster -m JTAG -o "p;$sof" > program.log 2>&1
if ($LASTEXITCODE -ne 0) {		# jtagd may still be starting: once more
	& (Join-Path $qbin "jtagconfig.exe") > $null 2>&1
	& (Join-Path $qbin "quartus_pgm.exe") -c USB-Blaster -m JTAG -o "p;$sof" > program.log 2>&1
}
$okPgm = ($LASTEXITCODE -eq 0)
$ErrorActionPreference = "Stop"
if (-not $okPgm) {
	Write-Line (U "board_fail") Red
	Write-Line (U "board_fail_en") Red
	exit 1
}

# ---------------------------------------------------------------- the link: login + start step in, step + code out
$srcHex = '{0:X4}' -f ((1 -shl 13) -bor ($from -shl 10) -bor $s)
$state = Join-Path (Get-Location) "link_state.txt"	# the link writes the board's state here (see link.tcl)
Remove-Item $state -ErrorAction SilentlyContinue
$psi = New-Object System.Diagnostics.ProcessStartInfo
$psi.FileName = Join-Path $qbin "quartus_stp.exe"
$psi.Arguments = "-t `"$(Join-Path $PSScriptRoot 'link.tcl')`" $srcHex `"$state`""
$psi.UseShellExecute = $false
$psi.CreateNoWindow = $true
$link = [System.Diagnostics.Process]::Start($psi)

function Show-Step($k) {
	Clear-Host
	Write-Host ""
	Write-Line "$($q.Id)" Cyan
	Write-Line ("$($q.Title)     " + ((U "step_head") -f $k, $last)) Cyan
	Write-Host ""
	$q.B | ForEach-Object { Write-Line $_ DarkGray }
	# the student's own text (statement, expression, story...): inside the step where a line is "@P", else at the top
	# every step shows ALL the data of the question on its own screen: the student's own text is either inside the
	# step (an "@P" line) or, in every other step, at the top under a label - never missing
	$mine = if ($q.P.ContainsKey($pub)) { @($q.P[$pub]) } else { @() }
	$inline = @($q.S[$k]) -contains "@P"
	if ($mine.Count -and -not $inline) { Write-Host ""; Write-Line (U "mine") White; $mine | ForEach-Object { Write-Line $_ White } }
	Write-Host ""
	foreach ($l in $q.S[$k]) {
		if ($l -eq "@P") { $mine | ForEach-Object { Write-Line $_ White } } else { Write-Line $l Yellow }
	}
	Write-Host ""
	Write-Line (U "foot") Green
	Write-Line (U "foot_en") Green
	if ($dl) { Write-Line ((U "topic_end") -f ('{0:HH:mm}' -f $dl)) DarkGray }
}

try {
	$cur = 0
	$prev = ""
	$t0 = Get-Date
	while ($true) {
		Start-Sleep -Milliseconds 200
		if (Test-TimeUp) {
			Write-Host ""
			Write-Line (U "timeup") Yellow
			exit 2
		}
		$line = $null
		try { $line = ([IO.File]::ReadAllText($state)).Trim() } catch { }
		if ($link.HasExited -or ($line -like "X*")) {
			Write-Host ""
			Write-Line (U "link_stop") Red
			if ($line -like "X *") { Write-Host "  ($($line.Substring(2)))" -ForegroundColor DarkGray }
			exit 1
		}
		if ($cur -eq 0 -and ((Get-Date) - $t0).TotalSeconds -gt 40) {
			Write-Line (U "no_answer") Red
			exit 1
		}
		if (-not $line -or $line -eq $prev) { continue }
		$prev = $line
		if ($line -notmatch '^P\s+([0-9A-Fa-f]+)') { continue }
		$v = [Convert]::ToInt32($Matches[1], 16)
		$fin = ($v -shr 19) -band 1
		$step = ($v -shr 16) -band 7
		if ($cur -eq 0) {
			if ($step -lt $from) { continue }		# the board is still starting
			$cur = $step; Show-Step $cur; continue
		}
		while ($cur -lt $step) {			# a step passed on the board
			Save-Progress $sid $q.Id $cur
			Write-Host ""
			Write-Line (U "pass") Green
			Start-Sleep -Milliseconds 1500
			$cur++
			Show-Step $cur
		}
		if ($fin) {
			$code = '{0:X4}' -f ($v -band 0xFFFF)
			Save-Progress $sid $q.Id $last
			Save-MoodleCode $sid $q.Id $code
			Write-Host ""
			Write-Line (U "done") Green
			Write-Line ((U "done_en") -f $q.Id, $code) Green
			exit 0
		}
	}
} finally {
	if (-not $link.HasExited) { $link.Kill() }
}
