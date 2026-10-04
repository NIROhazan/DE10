# Exercise 0 (equation) runner: asks the questions of questions.txt one by one.
# For each question it programs the board with that question's equation, then the student types the answer here:
#   Qn:  Y = <equation> | SW: 0 5 8      -> type the four digits HEX3 HEX2 HEX1 HEX0
#   Qn:  Y = <equation> | HEX: 7 0 3 4   -> type the switches that make the board show this (? = any digit)
# The right answer is computed from the Q line and never printed. Every try goes to results.txt.
# Kept ASCII so Windows PowerShell 5.1 reads it without a BOM (the console cannot print Hebrew anyway).

# run.ps1 -Only Q3 asks just that question (even if it was solved before) - that is what Q03.bat does.
param([string]$Only = "")

$ErrorActionPreference = "Stop"
Set-Location (Split-Path $PSScriptRoot -Parent)
$utf8 = New-Object System.Text.UTF8Encoding($false)
. (Join-Path $PSScriptRoot "eq.ps1")
. (Join-Path $PSScriptRoot "board.ps1")

function Fail($t) { Write-Host $t -ForegroundColor Red; exit 1 }
function Log($t) {
	[IO.File]::AppendAllText((Join-Path (Get-Location) "results.txt"),
		"[$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')]  $t`r`n", $utf8)
}

# ---------------------------------------------------------------- questions
if (-not (Test-Path "questions.txt")) { Fail "questions.txt is missing." }
$qs = @()
foreach ($line in [IO.File]::ReadAllLines((Resolve-Path "questions.txt"), $utf8)) {
	if ($line -match '^\s*Q(\d+):\s*Y\s*=\s*(.+?)\s*\|\s*(SW|HEX)\s*:\s*(.*)$') {
		$qs += [pscustomobject]@{ Id = "Q" + $Matches[1]; Eq = $Matches[2]; Kind = $Matches[3].ToUpper(); Given = $Matches[4].Trim() }
	}
}
if ($qs.Count -eq 0) { Fail "No Q lines in questions.txt." }

# Questions already solved (OK in results.txt) are skipped
$solved = @{}
if (Test-Path "results.txt") {
	foreach ($l in [IO.File]::ReadAllLines((Resolve-Path "results.txt"), $utf8)) {
		if ($l -match '\]\s+(Q\d+)\s+OK') { $solved[$Matches[1]] = $true }
	}
}
$left = @($qs | Where-Object { -not $solved[$_.Id] })
if ($Only) {
	$left = @($qs | Where-Object { $_.Id -eq $Only })
	if ($left.Count -eq 0) { Fail "There is no $Only in questions.txt." }
}

Write-Host ""
Write-Host "  Exercise 0 - equations on the board" -ForegroundColor Cyan
Write-Host "  Board, left to right:   HEX3  HEX2  HEX1  HEX0"
Write-Host "                           Y     C     B     A"
Write-Host "  A = SW3..SW0   B = SW6..SW4   C = SW9..SW7   (SW0 is the rightmost switch)"
Write-Host "  + is OR, * is AND, ~ and ' are NOT, ^ is XOR - bit by bit on 4 bits."
Write-Host "  Solved $($qs.Count - $left.Count) of $($qs.Count).  Type S to skip a question, Q to stop."
if ($left.Count -eq 0) { Write-Host "  All questions are solved." -ForegroundColor Green; exit 0 }

# ---------------------------------------------------------------- one question at a time
foreach ($q in $left) {
	$id = $q.Id; $eq = $q.Eq; $kind = $q.Kind; $given = $q.Given
	$null, $f = Read-Equation $eq
	Write-Host ""
	Write-Host "=== $id   Y = $eq ===" -ForegroundColor Cyan
	try { Send-Sof (Get-Sof $eq) } catch { Fail "  $($_.Exception.Message)" }
	Write-Host "  The board now has Y = $eq."
	if ($kind -eq "SW") {
		$sw = @([regex]::Matches($given, '\d') | ForEach-Object { [int]$_.Value })
		Write-Host "  Raise ONLY these switches: $(($sw | ForEach-Object { "SW$_" }) -join ' ')"
		Write-Host "  What do HEX3 HEX2 HEX1 HEX0 show? (4 digits, e.g. 3 0 2 1)"
	} else {
		Write-Host "  Make the board show (HEX3 HEX2 HEX1 HEX0):   $given      (? = any digit)"
		Write-Host "  Which switches did you raise? (switch numbers, e.g. 0 4 6)"
	}

	$tries = 0
	while ($true) {
		$ans = Read-Host "  $id answer"
		if ($null -eq $ans) { exit 0 }		# input closed
		$ans = $ans.Trim()
		if ($ans -match '^[Qq]$') { Write-Host "  Stopped. Run run.bat again to continue."; exit 0 }
		if ($ans -match '^[Ss]$') { Log "$id skipped after $tries tries"; break }
		if ($kind -eq "SW") {
			$mine = ($ans -replace '\s', '').ToUpper()
			if ($mine -notmatch '^[0-9A-F]{4}$') { Write-Host "  Type 4 digits 0-9 / A-F, e.g. 3 0 2 1" -ForegroundColor Yellow; continue }
			$good = ($mine -eq (Get-Display $f $sw))
		} else {
			if ($ans -notmatch '^[\sSWsw0-9,]+$' -or $ans -notmatch '\d') { Write-Host "  Type switch numbers, e.g. 0 4 6" -ForegroundColor Yellow; continue }
			$mine = @([regex]::Matches($ans, '\d') | ForEach-Object { [int]$_.Value })
			$shown = Get-Display $f $mine
			$want = ($given -replace '\s', '').ToUpper()
			$good = $true
			for ($i = 0; $i -lt 4; $i++) { if ($want[$i] -ne '?' -and $want[$i] -ne $shown[$i]) { $good = $false } }
		}
		$tries++
		if ($good) {
			Log "$id OK   try $tries   Y = $eq   answer: $ans"
			Write-Host "  Correct!" -ForegroundColor Green
			break
		}
		Log "$id wrong try $tries   Y = $eq   answer: $ans"
		Write-Host "  Wrong - look at the board again and try again." -ForegroundColor Red
	}
}

$n = 0
foreach ($l in [IO.File]::ReadAllLines((Resolve-Path "results.txt"), $utf8)) { if ($l -match '\]\s+Q\d+\s+OK') { $n++ } }
Write-Host ""
Write-Host "  Done. Solved $n of $($qs.Count). Your tries are saved in results.txt." -ForegroundColor Cyan
