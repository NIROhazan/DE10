# Personal questions and completion codes (dot-source after eq.ps1).
#   Get-StudentId            asks for the ID once, keeps it in student.txt
#   New-Question $q $id      fills a question template with this student's own numbers
#   Get-Code $id "Q7"        the completion code the student hands in on Moodle
# The numbers and codes come from the ID, so a friend's answers and codes do not fit.
# Kept ASCII so Windows PowerShell 5.1 reads it without a BOM.

$script:codeKey = [Text.Encoding]::ASCII.GetBytes("Sapir-DE10-ex0-2026-numerical-systems")
$script:codeAbc = "23456789ABCDEFGHJKLMNPQRSTUVWXYZ"	# no 0/O, 1/I

# Student number, e.g. 3160009489: 6-10 digits (no check digit - the Y/N question catches typos)
function Test-StudentId($id) { return ($id -match '^\d{6,10}$') }

function Get-StudentId {
	if (Test-Path "student.txt") {
		$id = ([IO.File]::ReadAllText((Resolve-Path "student.txt"))).Trim()
		if (Test-StudentId $id) { return $id }
	}
	Write-Host ""
	Write-Host "  First time: type your student ID number (for example 3160009489)." -ForegroundColor Cyan
	Write-Host "  Your questions are made from it, and it cannot be changed later."
	while ($true) {
		$id = Read-Host "  ID"
		if ($null -eq $id) { exit 0 }
		$id = $id.Trim()
		if (-not (Test-StudentId $id)) { Write-Host "  Type only the digits of your ID (6-10 digits)." -ForegroundColor Yellow; continue }
		$ok = Read-Host "  ID $id - is this right? (Y/N)"
		if ($null -eq $ok) { exit 0 }
		if ($ok.Trim() -match '^[Yy]') { break }
	}
	[IO.File]::WriteAllText((Join-Path (Get-Location) "student.txt"), $id)
	return $id
}

function Get-Code($id, $qid) {
	$h = New-Object Security.Cryptography.HMACSHA256 (, $script:codeKey)
	$b = $h.ComputeHash([Text.Encoding]::ASCII.GetBytes("$id|$qid"))
	return (($b[0..4] | ForEach-Object { $script:codeAbc[$_ % 32] }) -join "")
}

function Bits($n) { $c = 0; for ($i = 0; $i -lt 4; $i++) { if ($n -band (1 -shl $i)) { $c++ } }; return $c }

# A question template:  Eq, Kind (SW or HEX), Show (for HEX: e.g. "Y??A" - a letter shows that digit, ? hides it),
# Max (most switch settings allowed to give the shown digits - keeps it hard), If (PowerShell condition on $A $B $C $Y).
# Picks this student's switch setting from the ID, so every question still has an answer on the board.
function New-Question($q, $id) {
	$null, $f = Read-Equation $q.Eq
	$cond = if ($q.If) { [scriptblock]::Create("param(`$A, `$B, `$C, `$Y) $($q.If)") } else { { $true } }
	$all = if ($q.Kind -eq "HEX") { Get-AllDisplays $f } else { $null }
	$md5 = [Security.Cryptography.MD5]::Create()
	for ($k = 0; $k -lt 4000; $k++) {
		$b = $md5.ComputeHash([Text.Encoding]::ASCII.GetBytes("$id|$($q.Id)|$k"))
		$v = ($b[0] + 256 * $b[1]) % 1024
		$A = $v -band 15; $B = ($v -shr 4) -band 7; $C = ($v -shr 7) -band 7; $Y = & $f $A $B $C
		if (-not (& $cond $A $B $C $Y)) { continue }
		if ($q.Kind -eq "SW") {
			return ((0..9 | Where-Object { $v -band (1 -shl $_) }) -join " ")
		}
		$d = Get-DisplayOf $f $v; $want = ""
		for ($i = 0; $i -lt 4; $i++) { $want += $(if ($q.Show[$i] -eq '?') { '?' } else { $d[$i] }) }
		if ($q.Max -and @($all | Where-Object { Test-Pattern $_ $want }).Count -gt $q.Max) { continue }
		return (($want.ToCharArray()) -join " ")
	}
	throw "$($q.Id): no switch setting fits the IF / MAX of this question - fix questions.txt."
}
