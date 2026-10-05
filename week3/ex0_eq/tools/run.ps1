# Exercise 0 (equation) runner. Q03.bat = run.ps1 -Only Q3 (without -Only: every unsolved question in order).
# questions.txt holds templates; each student gets their own numbers from their ID (student.ps1):
#   Qn:  Y = <equation> | SW                 -> the student gets switches, types the four digits HEX3 HEX2 HEX1 HEX0
#   Qn:  Y = <equation> | HEX: Y ? ? A       -> the student gets digits (? hidden), types switches that show them
# The right answer is never printed. A correct answer gives a code (from the ID) that goes into moodle.txt;
# every try goes to results.txt. Kept ASCII so Windows PowerShell 5.1 reads it without a BOM.
param([string]$Only = "")

$ErrorActionPreference = "Stop"
Set-Location (Split-Path $PSScriptRoot -Parent)
$utf8 = New-Object System.Text.UTF8Encoding($false)
. (Join-Path $PSScriptRoot "eq.ps1")
. (Join-Path $PSScriptRoot "board.ps1")
. (Join-Path $PSScriptRoot "student.ps1")

function Fail($t) { Write-Host $t -ForegroundColor Red; exit 1 }
function Log($t) {
	[IO.File]::AppendAllText((Join-Path (Get-Location) "results.txt"),
		"[$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')]  $sid  $t`r`n", $utf8)
}
# moodle.txt = the ID and the code of every solved question - this is what the student hands in
function Save-Moodle {
	$out = @("Exercise 0 - DE1 equations", "ID: $sid")
	foreach ($q in $qs) { if ($solved[$q.Id]) { $out += "$($q.Id): $(Get-Code $sid $q.Id)" } }
	[IO.File]::WriteAllLines((Join-Path (Get-Location) "moodle.txt"), $out, $utf8)
}

# ---------------------------------------------------------------- questions
if (-not (Test-Path "questions.txt")) { Fail "questions.txt is missing." }
$qs = @()
$re = '^\s*Q(\d+):\s*Y\s*=\s*(.+?)\s*\|\s*(SW|HEX:\s*[YCBA?](?:\s*[YCBA?]){3})\s*(?:\|\s*MAX:\s*(\d+)\s*)?(?:\|\s*IF:\s*(.*))?$'
foreach ($line in [IO.File]::ReadAllLines((Resolve-Path "questions.txt"), $utf8)) {
	if ($line -match $re) {
		$kind = if ($Matches[3] -eq "SW") { "SW" } else { "HEX" }
		$qs += [pscustomobject]@{
			Id = "Q" + $Matches[1]; Eq = $Matches[2]; Kind = $kind
			Show = ($Matches[3] -replace '^HEX:|\s', ''); Max = [int]$Matches[4]; If = $Matches[5] }
	}
}
if ($qs.Count -eq 0) { Fail "No Q lines in questions.txt." }

$sid = Get-StudentId

# Questions this ID already solved (OK in results.txt) are skipped
$solved = @{}
if (Test-Path "results.txt") {
	foreach ($l in [IO.File]::ReadAllLines((Resolve-Path "results.txt"), $utf8)) {
		if ($l -match "\]\s+$sid\s+(Q\d+)\s+OK") { $solved[$Matches[1]] = $true }
	}
}
$left = @($qs | Where-Object { -not $solved[$_.Id] })
if ($Only) {
	$left = @($qs | Where-Object { $_.Id -eq $Only })
	if ($left.Count -eq 0) { Fail "There is no $Only in questions.txt." }
}

Write-Host ""
Write-Host "  Exercise 0 - equations on the board          ID $sid" -ForegroundColor Cyan
Write-Host "  Board, left to right:   HEX3  HEX2  HEX1  HEX0"
Write-Host "                           Y     C     B     A"
Write-Host "  A = SW3..SW0   B = SW6..SW4   C = SW9..SW7   (SW0 is the rightmost switch)"
Write-Host "  + is OR, * is AND, ~ and ' are NOT, ^ is XOR - bit by bit on 4 bits."
Write-Host "  Solved $(@($qs | Where-Object { $solved[$_.Id] }).Count) of $($qs.Count).  Type S to skip a question, Q to stop."
if ($left.Count -eq 0) { Write-Host "  All questions are solved. Hand in moodle.txt on Moodle." -ForegroundColor Green; Save-Moodle; exit 0 }

# ---------------------------------------------------------------- one question at a time
foreach ($q in $left) {
	$id = $q.Id; $eq = $q.Eq; $kind = $q.Kind
	$null, $f = Read-Equation $eq
	try { $given = New-Question $q $sid } catch { Fail "  $($_.Exception.Message)" }
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
		if ($ans -match '^[Qq]$') { Write-Host "  Stopped. Run the question again to continue."; exit 0 }
		if ($ans -match '^[Ss]$') { Log "$id skipped after $tries tries"; break }
		if ($kind -eq "SW") {
			$mine = ($ans -replace '\s', '').ToUpper()
			if ($mine -notmatch '^[0-9A-F]{4}$') { Write-Host "  Type 4 digits 0-9 / A-F, e.g. 3 0 2 1" -ForegroundColor Yellow; continue }
			$good = ($mine -eq (Get-Display $f $sw))
		} else {
			if ($ans -notmatch '^[\sSWsw0-9,]+$' -or $ans -notmatch '\d') { Write-Host "  Type switch numbers, e.g. 0 4 6" -ForegroundColor Yellow; continue }
			$mine = @([regex]::Matches($ans, '\d') | ForEach-Object { [int]$_.Value })
			$good = Test-Pattern (Get-Display $f $mine) (($given -replace '\s', '').ToUpper())
		}
		$tries++
		if ($good) {
			Log "$id OK   try $tries   Y = $eq   asked: $given   answer: $ans"
			$solved[$id] = $true
			Save-Moodle
			Write-Host "  Correct!  Your code for ${id}: $(Get-Code $sid $id)   (saved in moodle.txt)" -ForegroundColor Green
			break
		}
		Log "$id wrong try $tries   Y = $eq   asked: $given   answer: $ans"
		Write-Host "  Wrong - look at the board again and try again." -ForegroundColor Red
	}
}

$n = @($qs | Where-Object { $solved[$_.Id] }).Count
Write-Host ""
Write-Host "  Solved $n of $($qs.Count). When you finish, hand in the file moodle.txt on Moodle." -ForegroundColor Cyan
