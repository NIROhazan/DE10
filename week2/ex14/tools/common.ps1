# Week 2 shared helpers (the same file in ex14..ex19; dot-source before questions.ps1).
#   Get-StudentId             the ID, kept in student.txt in the course folder (shared with every exercise)
#   Get-Num $sid $tag $k $n   this student's own number 0..n-1 for a question (k = which try)
#   Test-Answer $checks $ans  $true / $false, or $null when the answer is not in the asked format
#   Save-MoodleCode           the code for Moodle, the same as in every other exercise
# Kept ASCII so Windows PowerShell 5.1 reads it without a BOM.

$script:codeKey = [Text.Encoding]::ASCII.GetBytes("Sapir-DE10-ex0-2026-numerical-systems")
$script:codeAbc = "23456789ABCDEFGHJKLMNPQRSTUVWXYZ"	# no 0/O, 1/I
$script:utf8 = New-Object System.Text.UTF8Encoding($false)

function Test-StudentId($id) { return ($id -match '^\d{6,10}$') }

# The course folder (the one with locked\): the exercise sits one or two levels below it (week3\exN)
function Get-CourseRoot {
	$r = Split-Path (Get-Location) -Parent
	while ($r -and -not (Test-Path (Join-Path $r "locked"))) { $r = Split-Path $r -Parent }
	if ($r) { return $r } else { return (Split-Path (Get-Location) -Parent) }
}
# The ID is kept in student.txt in the course folder, so every exercise of the course uses the same one.
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
	Write-Host "  Your numbers are made from it, and it cannot be changed later."
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

function Get-Code($id, $label) {
	$h = New-Object Security.Cryptography.HMACSHA256 (, $script:codeKey)
	$b = $h.ComputeHash([Text.Encoding]::ASCII.GetBytes("$id|$label"))
	return (($b[0..4] | ForEach-Object { $script:codeAbc[$_ % 32] }) -join "")
}

function Save-MoodleCode($sid, $proj, $label) {
	$f = Join-Path (Get-Location) "moodle.txt"
	$codes = [ordered]@{}
	if (Test-Path $f) {
		foreach ($l in [IO.File]::ReadAllLines($f, $script:utf8)) { if ($l -match '^\s*(ex\d+(?:-Q\d+)?):\s*(\S+)\s*$') { $codes[$Matches[1]] = $Matches[2] } }
	}
	$codes[$label] = Get-Code $sid $label
	$out = @("Exercise $($proj -replace '\D', '')", "ID: $sid") + @($codes.Keys | Sort-Object | ForEach-Object { "${_}: $($codes[$_])" })
	[IO.File]::WriteAllLines($f, $out, $script:utf8)
	return $codes[$label]
}

# This student's own number 0..n-1 for one value of one question; k = the try (a wrong answer gives new numbers)
function Get-Num($sid, $tag, $k, $n) {
	$b = [Security.Cryptography.MD5]::Create().ComputeHash([Text.Encoding]::ASCII.GetBytes("$sid|$($script:Ex)|$tag|$k"))
	return [int](([uint32]$b[0] + 256 * [uint32]$b[1] + 65536 * [uint32]$b[2]) % $n)
}
function Get-Pick($sid, $tag, $k, $list) { $list = @($list); return $list[(Get-Num $sid $tag $k $list.Count)] }

# ---------------------------------------------------------------- secrets.txt: pools and answer hashes
$script:pools = @{}; $script:okHash = @{}
function Read-Secrets {
	$f = Join-Path $PSScriptRoot "secrets.txt"
	if (-not (Test-Path $f)) { return }
	foreach ($l in [IO.File]::ReadAllLines($f, $script:utf8)) {
		$w = @($l.Trim() -split '\s+')
		if ($w[0] -eq "pool") { $script:pools[$w[1]] = @($w | Select-Object -Skip 2) }
		elseif ($w[0] -eq "ok") { $w | Select-Object -Skip 1 | ForEach-Object { $script:okHash[$_] = $true } }
	}
}
function Get-Hash($s) {
	$b = [Security.Cryptography.SHA256]::Create().ComputeHash([Text.Encoding]::ASCII.GetBytes("DE10w2|$s"))
	return ((($b[0..4]) | ForEach-Object { $_.ToString("x2") }) -join "")
}

# ---------------------------------------------------------------- answers
# A check is @{ Parts = "hex","dec"; Value = "A7 167" } or @{ Parts = "word","word"; Secret = "p3k4" } or
# @{ Parts = "sw"; Value = "1 3 8" } (all the switch numbers). Parts: dec, hex, bin, word, sw.
# $script:Synonyms (questions.ps1) maps other spellings of a word to the one in the answers.
function ConvertTo-Part($kind, $t) {
	switch ($kind) {
		"dec" { if ($t -match '^[+-]?\d+$') { return ([long]$t).ToString() } }
		"hex" { $h = $t -replace '^0X', '' -replace 'H$', ''; if ($h -match '^[0-9A-F]+$') { return ([Convert]::ToInt64($h, 16)).ToString("X") } }
		"bin" { $b = $t -replace '^0B', '' -replace '_', ''; if ($b -match '^[01]+$') { return $b } }
		"word" {
			$w = $t -replace '[^A-Z0-9]', ''
			if ($script:Synonyms -and $script:Synonyms.ContainsKey($w)) { $w = $script:Synonyms[$w] }
			if ($w) { return $w }
		}
	}
	return $null
}
function Test-Answer($checks, $ans) {
	$tokens = @(($ans.ToUpper() -replace '[,;]', ' ').Trim() -split '\s+' | Where-Object { $_ })
	if ($tokens.Count -eq 0) { return $null }
	$checks = @($checks)
	if ($checks[0].Parts -contains "sw") {
		$sw = @()
		foreach ($t in $tokens) {
			if ($t -notmatch '^(SW)?(\d)$') { return $null }
			$sw += [int]$Matches[2]
		}
		return ((@($sw | Sort-Object -Unique) -join " ") -eq $checks[0].Value)
	}
	$need = 0; foreach ($c in $checks) { $need += @($c.Parts).Count }
	if ($tokens.Count -ne $need) { return $null }
	$i = 0; $good = $true
	foreach ($c in $checks) {
		$got = @()
		foreach ($p in @($c.Parts)) {
			$v = ConvertTo-Part $p $tokens[$i]; $i++
			if ($null -eq $v) { return $null }
			$got += $v
		}
		$got = $got -join " "
		if ($c.Secret) { if (-not $script:okHash[(Get-Hash "$($script:Ex)|$($c.Secret)|$got")]) { $good = $false } }
		elseif ($got -ne $c.Value) { $good = $false }
	}
	return $good
}

# Switch numbers of a value: Get-Switches 0x2B7 -> "0 1 2 4 5 7 9" (SW0 = bit 0); $from = the lowest switch
function Get-Switches($v, $from = 0) { return ((0..15 | Where-Object { $v -band (1 -shl $_) } | ForEach-Object { $_ + $from }) -join " ") }
function Get-Bin($v, $n) { return ([Convert]::ToString([long]$v, 2)).PadLeft($n, '0') }
