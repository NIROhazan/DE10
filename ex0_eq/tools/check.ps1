# Exercise 0 (equation) checker: reads the Q / A lines of answer.txt and says OK / wrong / empty for each.
# The right answer is computed from the Q line itself, so questions can be changed freely:
#   Qn:  Y = <equation> | SW: 0 5 8          -> An = the four digits HEX3 HEX2 HEX1 HEX0 (e.g. 3 2 2 1)
#   Qn:  Y = <equation> | HEX: 7 0 3 4       -> An = the switches raised (e.g. 2 4 5); ? in HEX = any digit
# It never prints the right answer. Kept ASCII so Windows PowerShell 5.1 reads it without a BOM.

$ErrorActionPreference = "Stop"
Set-Location (Split-Path $PSScriptRoot -Parent)
$utf8 = New-Object System.Text.UTF8Encoding($false)
. (Join-Path $PSScriptRoot "eq.ps1")

if (-not (Test-Path "answer.txt")) { Write-Host "answer.txt is missing." -ForegroundColor Red; exit 1 }
$q = [ordered]@{}; $a = @{}
foreach ($line in [IO.File]::ReadAllLines((Resolve-Path "answer.txt"), $utf8)) {
	if ($line.TrimStart().StartsWith("#")) { continue }
	if ($line -match '^\s*Q(\d+):\s*Y\s*=\s*(.+?)\s*\|\s*(SW|HEX)\s*:\s*(.*)$') {
		$q["Q" + $Matches[1]] = @($Matches[2], $Matches[3].ToUpper(), $Matches[4].Trim())
	} elseif ($line -match '^\s*A(\d+)\s*=(.*)$') {
		$a["Q" + $Matches[1]] = $Matches[2].Trim()
	}
}
if ($q.Count -eq 0) { Write-Host "No Q lines found in answer.txt." -ForegroundColor Red; exit 1 }

Write-Host ""
Write-Host "=== Checking answer.txt ===" -ForegroundColor Cyan
$ok = 0
foreach ($n in $q.Keys) {
	$eq, $kind, $given = $q[$n]
	$label = "  {0,-4} Y = {1,-16}" -f $n, $eq
	$ans = $a[$n]
	if (-not $ans) { Write-Host "$label empty" -ForegroundColor DarkGray; continue }
	try { $null, $f = Read-Equation $eq } catch { Write-Host "$label bad Q line: $($_.Exception.Message)" -ForegroundColor Red; continue }

	if ($kind -eq "SW") {
		# Level 1: switches given, the student writes the four digits
		$sw = @([regex]::Matches($given, '\d') | ForEach-Object { [int]$_.Value })
		$right = Get-Display $f $sw
		$mine = ($ans -replace '\s', '').ToUpper()
		if ($mine -notmatch '^[0-9A-F]{4}$') {
			Write-Host "$label write 4 digits HEX3 HEX2 HEX1 HEX0, e.g.  3 0 2 1" -ForegroundColor Yellow; continue
		}
		$good = ($mine -eq $right)
	} else {
		# Level 2: digits given (? = any), the student writes the switches
		$want = ($given -replace '\s', '').ToUpper()
		$sw = @([regex]::Matches($ans, '\d') | ForEach-Object { [int]$_.Value })
		if ($sw.Count -eq 0) { Write-Host "$label write switch numbers, e.g.  0 4 6" -ForegroundColor Yellow; continue }
		$shown = Get-Display $f $sw
		$good = $true
		for ($i = 0; $i -lt 4; $i++) { if ($want[$i] -ne '?' -and $want[$i] -ne $shown[$i]) { $good = $false } }
	}
	if ($good) { $ok++; Write-Host "$label OK" -ForegroundColor Green }
	else { Write-Host "$label wrong" -ForegroundColor Red }
}
Write-Host ""
Write-Host "  $ok of $($q.Count) correct"
