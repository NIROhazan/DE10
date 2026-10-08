# Class exercise helpers (dot-source from run.ps1).
#   Get-StudentId          the ID, kept in student.txt in the course folder (shared with every exercise)
#   Get-Login $sid         the login number 0-1023 the student sets on SW9..SW0 (public, from the ID)
#   Get-Pub $qid $s $n     which printed text this login number gets (public)
#   Test-CodeDigits        the last code digit is a check digit: catches typos and a wrong login
# The PC knows neither the answers nor the codes - only the board does.
# Kept ASCII so Windows PowerShell 5.1 reads it without a BOM.

$script:utf8 = New-Object System.Text.UTF8Encoding($false)

function Test-StudentId($id) { return ($id -match '^\d{6,10}$') }

# The course folder (the one with locked\): the exercise sits one level below it
function Get-CourseRoot {
	$r = Split-Path (Get-Location) -Parent
	while ($r -and -not (Test-Path (Join-Path $r "locked"))) { $r = Split-Path $r -Parent }
	if ($r) { return $r } else { return (Split-Path (Get-Location) -Parent) }
}
function Get-StudentId {
	$shared = Join-Path (Get-CourseRoot) "student.txt"
	foreach ($f in @($shared, (Join-Path (Get-Location) "student.txt"))) {
		if (Test-Path $f) {
			$id = ([IO.File]::ReadAllText($f)).Trim()
			if (Test-StudentId $id) { return $id }
		}
	}
	Write-Host ""
	Write-Host "  First time: type your student ID number (for example 3160009489)." -ForegroundColor Cyan
	Write-Host "  Your login number is made from it, and it cannot be changed later."
	while ($true) {
		$id = Read-Host "  ID"
		if ($null -eq $id) { exit 0 }
		$id = $id.Trim()
		if (-not (Test-StudentId $id)) { Write-Host "  Type only the digits of your ID (6-10 digits)." -ForegroundColor Yellow; continue }
		$ok = Read-Host "  ID $id - is this right? (Y/N)"
		if ($null -eq $ok) { exit 0 }
		if ($ok.Trim() -match '^[Yy]') { break }
	}
	try { [IO.File]::WriteAllText($shared, $id) } catch { [IO.File]::WriteAllText((Join-Path (Get-Location) "student.txt"), $id) }
	return $id
}

function Get-Md5($s) { return [Security.Cryptography.MD5]::Create().ComputeHash([Text.Encoding]::ASCII.GetBytes($s)) }
function Get-Login($sid) { $b = Get-Md5 "DE10ce|$sid"; return (($b[0] + 256 * $b[1]) % 1024) }
function Get-Pub($qid, $s, $n) { if ($n -le 1) { return 0 }; return ((Get-Md5 "DE10ce|$qid|$s")[0] % $n) }

# Code = 4 hex digits HEX3 HEX2 HEX1 HEX0; HEX0 = check digit over the other three, the login number and the step
# (questions without steps: no step term)
function Test-CodeDigits($code, $s, $step = 0) {
	$d = @($code.ToCharArray() | ForEach-Object { [Convert]::ToInt32([string]$_, 16) })
	$c = ($d[0] + 3 * $d[1] + 5 * $d[2] + 7 + 9 * ($s -band 15) + 11 * (($s -shr 4) -band 15) + 13 * ($s -shr 8) + 15 * $step) % 16
	return ($c -eq $d[3])
}

function Get-Bin($v, $n) { return ([Convert]::ToString([long]$v, 2)).PadLeft($n, '0') }

# The questions: [Qnn] NAME | title | npub n [| steps n], then B: / L: / Pk: / F: / Sk: lines
function Read-Questions {
	$qs = [ordered]@{}; $cur = $null
	foreach ($l in [IO.File]::ReadAllLines((Join-Path $PSScriptRoot "questions.txt"), $script:utf8)) {
		if ($l -match '^\[(Q\d+)\]\s*(\S+)\s*\|\s*(.+?)\s*\|\s*npub\s+(\d+)(?:\s*\|\s*steps\s+(\d+))?(\s*\|\s*flat)?') {
			$cur = [pscustomobject]@{ Id = $Matches[1]; Name = $Matches[2]; Title = $Matches[3]; NPub = [int]$Matches[4]
				NS = $(if ($Matches[5]) { [int]$Matches[5] } else { 0 }); Flat = [bool]$Matches[6]; B = @(); L = @(); F = @(); P = @{}; S = @{} }
			$qs[$cur.Id] = $cur
		} elseif ($cur -and $l -match '^([BLF]):\s?(.*)$') {
			$cur.($Matches[1]) += $Matches[2]
		} elseif ($cur -and $l -match '^S(\d+):\s?(.*)$') {
			$k = [int]$Matches[1]
			if (-not $cur.S.ContainsKey($k)) { $cur.S[$k] = @() }
			$cur.S[$k] += $Matches[2]
		} elseif ($cur -and $l -match '^P(\d+):\s?(.*)$') {
			$k = [int]$Matches[1]
			if (-not $cur.P.ContainsKey($k)) { $cur.P[$k] = @() }
			$cur.P[$k] += $Matches[2]
		}
	}
	return $qs
}

# progress.txt: "ID Qnn k" = the last step this student passed in that question (a closed window goes on from there)
function Get-Progress($sid, $qid) {
	$f = Join-Path (Get-Location) "progress.txt"
	$k = 0
	if (Test-Path $f) {
		foreach ($l in [IO.File]::ReadAllLines($f, $script:utf8)) {
			if ($l -match "^\s*$sid\s+$qid\s+(\d+)\s*$" -and [int]$Matches[1] -gt $k) { $k = [int]$Matches[1] }
		}
	}
	return $k
}
function Save-Progress($sid, $qid, $k) {
	[IO.File]::AppendAllText((Join-Path (Get-Location) "progress.txt"), "$sid $qid $k`r`n", $script:utf8)
}
function Get-SavedCode($qid) {
	$f = Join-Path (Get-Location) "moodle.txt"
	if (Test-Path $f) {
		foreach ($l in [IO.File]::ReadAllLines($f, $script:utf8)) { if ($l -match "^\s*ce-${qid}:\s*(\S+)") { return $Matches[1] } }
	}
	return "(not found - ask the lecturer)"
}

# moodle.txt: "ID: ..." and one "ce-Qnn: CODE" line per solved question
function Save-MoodleCode($sid, $qid, $code) {
	$f = Join-Path (Get-Location) "moodle.txt"
	$codes = [ordered]@{}
	if (Test-Path $f) {
		foreach ($l in [IO.File]::ReadAllLines($f, $script:utf8)) { if ($l -match '^\s*(ce-Q\d+):\s*(\S+)\s*$') { $codes[$Matches[1]] = $Matches[2] } }
	}
	$codes["ce-$qid"] = $code
	$out = @("Class exercise - lecture 3", "ID: $sid") + @($codes.Keys | Sort-Object | ForEach-Object { "${_}: $($codes[$_])" })
	[IO.File]::WriteAllLines($f, $out, $script:utf8)
}

# ---- Hebrew in the console. The console shows text left to right, so a Hebrew line comes out reversed. Write-Line
# turns a line that has Hebrew into visual order (the order of its pieces reversed; Latin / digit pieces like SW9 or
# 16 kept as they are; brackets mirrored) and aligns it to the right. Lines without Hebrew are written as they are.
# The question texts keep English (switch names, formulas) on lines of their own, so a line is either Hebrew or not.
function ConvertTo-Visual([string]$s) {
	$tok = [regex]::Matches($s, "[A-Za-z0-9][A-Za-z0-9_.+'=/:-]*|.")
	$out = New-Object System.Text.StringBuilder
	for ($i = $tok.Count - 1; $i -ge 0; $i--) {
		$t = $tok[$i].Value
		switch ($t) { '(' { $t = ')' } ')' { $t = '(' } '[' { $t = ']' } ']' { $t = '[' } '<' { $t = '>' } '>' { $t = '<' } }
		[void]$out.Append($t)
	}
	return $out.ToString()
}
function Write-Line([string]$s, [string]$color = "Gray") {
	if ($s -match '[\u0590-\u05FF]') {
		$w = 100
		try { $w = [Math]::Max(60, $Host.UI.RawUI.WindowSize.Width - 2) } catch { }
		$v = (ConvertTo-Visual $s.Trim())
		Write-Host ($v.PadLeft([Math]::Max($v.Length, $w))) -ForegroundColor $color
	} else {
		Write-Host "  $s" -ForegroundColor $color
	}
}

# ---- the fixed screen texts, in Hebrew (ui.txt, UTF-8). U "key" -> the text; a missing key shows the key itself.
$script:UI = @{}
$uiFile = Join-Path $PSScriptRoot "ui.txt"
if (Test-Path $uiFile) {
	foreach ($l in [IO.File]::ReadAllLines($uiFile, $script:utf8)) {
		if ($l -match '^\s*([A-Za-z_]+)\s*=\s?(.*)$') { $script:UI[$Matches[1]] = $Matches[2] }
	}
}
function U([string]$k) { if ($script:UI.ContainsKey($k)) { return $script:UI[$k] } else { return $k } }
