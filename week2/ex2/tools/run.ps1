# Week 2 runner (the same file in week2\ex1..ex6): Q1_DEC.bat = run.ps1 -Only Q1.
# Programs the exercise's board.sof once, then asks the question in the console with this student's own
# numbers (from the ID). A wrong answer gives NEW numbers - guessing does not help. A right answer gives
# the code for Moodle (moodle.txt). Every try goes to results.txt. The questions are in questions.ps1.
# Kept ASCII so Windows PowerShell 5.1 reads it without a BOM.
param([string]$Only = "")

$ErrorActionPreference = "Stop"
Set-Location (Split-Path $PSScriptRoot -Parent)
$proj = Split-Path -Leaf (Get-Location)
. (Join-Path $PSScriptRoot "common.ps1")
$script:Ex = Get-ExLabel		# w2-ex3: seeds the personal numbers, names the codes
. (Join-Path $PSScriptRoot "questions.ps1")
Read-Secrets

$qbin = @("C:\altera\13.0sp1\quartus\bin64", "C:\altera\13.0sp1\quartus\bin",
          "C:\altera\13.0\quartus\bin64", "C:\altera\13.0\quartus\bin") |
	Where-Object { Test-Path (Join-Path $_ "quartus_pgm.exe") } | Select-Object -First 1

function Log($t) {
	[IO.File]::AppendAllText((Join-Path (Get-Location) "results.txt"),
		"[$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')]  $sid  $proj $t`r`n", $script:utf8)
}
function Get-Tries($qid) {
	$n = 0
	if (Test-Path "results.txt") {
		foreach ($l in [IO.File]::ReadAllLines((Resolve-Path "results.txt"), $script:utf8)) {
			if ($l -match "\]\s+$sid\s+$proj $qid wrong") { $n++ }
		}
	}
	return $n
}

$all = @(Get-QuestionList)
$list = if ($Only) { @($all | Where-Object { $_.Id -eq $Only }) } else { $all }
if ($list.Count -eq 0) { Write-Host "There is no $Only in this exercise." -ForegroundColor Red; exit 1 }
$sid = Get-StudentId

Write-Host ""
Write-Host "  $($script:Title)          ID $sid" -ForegroundColor Cyan
$script:BoardHelp | ForEach-Object { Write-Host "  $_" }
Write-Host "  SW0 is the rightmost switch. Type S to skip, Q to stop."

# ---------------------------------------------------------------- the board
$sof = Join-Path (Get-Location) "board.sof"
$onBoard = $false
if ($qbin -and (Test-Path $sof)) {
	$ErrorActionPreference = "Continue"
	& (Join-Path $qbin "quartus_pgm.exe") -c USB-Blaster -m JTAG -o "p;$sof" > program.log 2>&1
	$onBoard = ($LASTEXITCODE -eq 0)
	$ErrorActionPreference = "Stop"
}
if ($onBoard) { Write-Host "  The board is programmed for $proj." -ForegroundColor Green }
else {
	Write-Host "  The board was NOT programmed (board off? USB cable in the BLASTER port? switch on RUN?)." -ForegroundColor Yellow
	Write-Host "  Questions that need the board cannot be answered without it." -ForegroundColor Yellow
}

# ---------------------------------------------------------------- one question at a time
foreach ($item in $list) {
	$qid = $item.Id
	while ($true) {
		$k = Get-Tries $qid
		$q = Get-Question $sid $qid $k
		Write-Host ""
		Write-Host "=== $proj $qid - $($item.Name) ===" -ForegroundColor Cyan
		$q.Lines | ForEach-Object { Write-Host "  $_" }
		Write-Host "  Answer format: $($q.Format)" -ForegroundColor DarkGray
		$ans = $null
		while ($true) {
			$ans = Read-Host "  $qid answer"
			if ($null -eq $ans) { exit 0 }		# input closed
			$ans = $ans.Trim()
			if ($ans -match '^[Qq]$') { Write-Host "  Stopped. Run the question again to continue."; exit 0 }
			if ($ans -match '^[Ss]$') { break }
			$r = Test-Answer $q.Checks $ans
			if ($null -eq $r) { Write-Host "  Not in the format - $($q.Format)" -ForegroundColor Yellow; continue }
			break
		}
		if ($ans -match '^[Ss]$') { Log "$qid skipped"; break }
		if ($r) {
			Log "$qid OK    try $($k + 1)   asked: $($q.Asked)   answer: $ans"
			$code = Save-MoodleCode $sid $proj "$($script:Ex)-$qid"
			Write-Host "  Correct!  Your code for $proj ${qid}: $code   (saved in moodle.txt - hand that file in on Moodle)" -ForegroundColor Green
			break
		}
		Log "$qid wrong try $($k + 1)   asked: $($q.Asked)   answer: $ans"
		Write-Host "  Wrong. You get NEW numbers - solve it again." -ForegroundColor Red
	}
}
Write-Host ""
