# Personal truth table for each student (dot-sourced by run.ps1; identical in ex1..ex6).
# tools/base_top.v holds the original exercise. Each student gets the same function with the variables
# renamed and/or complemented (a permutation P and a mask M picked from the student ID), so every property
# the exercise is built on - number of 1s, minimal SOP/POS size, uniqueness, don't-cares - stays the same,
# while the table and every answer differ from a friend's.
#   // VARIANTS: perms=all masks=all            (in base_top.v; default)
#   // VARIANTS: perms=ABCD,CDAB masks=-,A,C,AC (only these: e.g. keep the K-map picture of ex5)
#   // EXPR: AB + A(B + C)' + A'BC              (ex7, ex8: the expression the student starts from;
#                                                 @EXPR@ in answer.txt becomes this student's version)
# perms: the student's letter for each original variable, in order. masks: original variables to complement.
# Kept ASCII so Windows PowerShell 5.1 reads it without a BOM.

# Same key as ex0_eq/tools/student.ps1 - the codes of all exercises are checked by one verify script.
$script:codeKey = [Text.Encoding]::ASCII.GetBytes("Sapir-DE10-ex0-2026-numerical-systems")
$script:codeAbc = "23456789ABCDEFGHJKLMNPQRSTUVWXYZ"	# no 0/O, 1/I

function Test-StudentId($id) { return ($id -match '^\d{6,10}$') }

# The ID is kept in ..\student.txt, so every exercise of the course uses the same one.
function Get-StudentId {
	$shared = Join-Path (Split-Path (Get-Location) -Parent) "student.txt"
	foreach ($f in @($shared, (Join-Path (Get-Location) "student.txt"))) {
		if (Test-Path $f) {
			$id = ([IO.File]::ReadAllText($f)).Trim()
			if (Test-StudentId $id) { return $id }
		}
	}
	Write-Host ""
	Write-Host "  First time: type your student ID number (for example 3160009489)." -ForegroundColor Cyan
	Write-Host "  Your truth tables are made from it, and it cannot be changed later."
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

function Get-Permutations([string[]]$items) {
	if ($items.Count -le 1) { return , $items }
	$out = @()
	for ($i = 0; $i -lt $items.Count; $i++) {
		$rest = @($items | Select-Object -Index (@(0..($items.Count - 1)) | Where-Object { $_ -ne $i }))
		foreach ($p in (Get-Permutations $rest)) { $out += , (@($items[$i]) + $p) }
	}
	return $out
}

# The variant of this exercise for this student: Vars (A B C [D]), P[i] = index of the student's variable
# for original variable i, M[i] = 1 when it is complemented, Rows = original table.
function Get-Variant($sid, $proj, $baseFile) {
	$t = [IO.File]::ReadAllText($baseFile)
	if ($t -notmatch 'case\s*\(\{([^}]*)\}\)') { throw "No truth table in $baseFile" }
	$vars = @($Matches[1] -split ',' | ForEach-Object { $_.Trim() })
	$n = $vars.Count
	$perms = @(Get-Permutations $vars | ForEach-Object { $_ -join "" })
	$masks = @(0..([math]::Pow(2, $n) - 1) | ForEach-Object { $m = $_; -join (0..($n - 1) | ForEach-Object { if ($m -band (1 -shl $_)) { $vars[$_] } }) })
	if ($t -match '//\s*VARIANTS:\s*perms=(\S+)\s+masks=(\S+)') {
		if ($Matches[1] -ne "all") { $perms = @($Matches[1] -split ',') }
		if ($Matches[2] -ne "all") { $masks = @($Matches[2] -split ',' | ForEach-Object { $_ -replace '-', '' }) }
	}
	$h = [Security.Cryptography.MD5]::Create().ComputeHash([Text.Encoding]::ASCII.GetBytes("$sid|$proj|table"))
	$perm = $perms[($h[0] + 256 * $h[1]) % $perms.Count]
	$mask = $masks[($h[2] + 256 * $h[3]) % $masks.Count]
	$P = @(0..($n - 1) | ForEach-Object { [array]::IndexOf($vars, [string]$perm[$_]) })
	$M = @(0..($n - 1) | ForEach-Object { if ($mask.Contains($vars[$_])) { 1 } else { 0 } })
	$rows = @([regex]::Matches($t, "\d+'b([01]+):\s*(?:begin\s*)?Y\s*=\s*1'b([01]);(\s*dc\s*=\s*1'b1)?") |
		ForEach-Object { [pscustomobject]@{ Bits = $_.Groups[1].Value; Y = [int]$_.Groups[2].Value; Dc = $_.Groups[3].Success } })
	$expr = if ($t -match '(?m)^//\s*EXPR:\s*(.+?)\s*$') { $Matches[1] } else { "" }
	return [pscustomobject]@{ Vars = $vars; P = $P; M = $M; Rows = $rows; Text = $t; Expr = $expr }
}

# Original row (bits in variable order) -> this student's row
function Convert-Row($v, [string]$b) {
	$s = New-Object char[] $v.Vars.Count
	for ($i = 0; $i -lt $v.Vars.Count; $i++) { $s[$v.P[$i]] = [char](48 + ([int]("" + $b[$i]) -bxor $v.M[$i])) }
	return (-join $s)
}

# "A=0 B=1" in an original-table sentence -> the same row of this student's table
function Convert-Text($v, [string]$text) {
	return [regex]::Replace($text, '\b[A-D]=[01](?:\s+[A-D]=[01])*', {
		param($m)
		$pairs = @([regex]::Matches($m.Value, '([A-D])=([01])') | ForEach-Object {
			$i = [array]::IndexOf($v.Vars, $_.Groups[1].Value)
			if ($i -lt 0) { return }
			[pscustomobject]@{ K = $v.P[$i]; T = "$($v.Vars[$v.P[$i]])=$([int]$_.Groups[2].Value -bxor $v.M[$i])" } })
		($pairs | Sort-Object K | ForEach-Object { $_.T }) -join " "
	})
}

# An expression over the original variables -> the same expression for this student (A' etc.)
function Convert-Expr($v, [string]$expr) {
	return [regex]::Replace($expr, "([A-D])('*)", {
		param($m)
		$i = [array]::IndexOf($v.Vars, $m.Groups[1].Value)
		if ($i -lt 0) { return $m.Value }
		$neg = ($m.Groups[2].Value.Length + $v.M[$i]) % 2
		$v.Vars[$v.P[$i]] + $(if ($neg) { "'" } else { "" })
	})
}

# This student's table: one row per combination, in order
function Get-StudentRows($v) {
	$out = @{}
	foreach ($r in $v.Rows) { $out[(Convert-Row $v $r.Bits)] = [pscustomobject]@{ Bits = (Convert-Row $v $r.Bits); Y = $r.Y; Dc = $r.Dc } }
	return @($out.Keys | Sort-Object | ForEach-Object { $out[$_] })
}

function Format-Table($v, $prefix, $sep) {
	$rows = Get-StudentRows $v
	$cell = { param($r) (($r.Bits.ToCharArray()) -join $sep) + " | " + $(if ($r.Dc) { "X" } else { $r.Y }) }
	$head = ($v.Vars -join $sep) + " | Y"
	if ($rows.Count -le 8) { return @("$prefix$head") + @($rows | ForEach-Object { "$prefix$(& $cell $_)" }) }
	$half = $rows.Count / 2
	$lines = @("$prefix$head          $head")
	for ($i = 0; $i -lt $half; $i++) { $lines += "$prefix$(& $cell $rows[$i])          $(& $cell $rows[$i + $half])" }
	return $lines
}

# Writes <proj>_top.v (the board checks this student's table) and tools/tutor_personal.md (Claude's
# instructions with this student's table). Fills the table into answer.txt the first time; returns $true then.
function New-PersonalFiles($sid, $proj) {
	$utf8 = New-Object System.Text.UTF8Encoding($false)
	$v = Get-Variant $sid $proj (Join-Path (Get-Location) "tools\base_top.v")
	$n = $v.Vars.Count

	# --- the top level: case labels renamed, the comment table rewritten
	$top = [regex]::Replace($v.Text, "(\d+)'b([01]+):", { param($m) "$($m.Groups[1].Value)'b$(Convert-Row $v $m.Groups[2].Value):" })
	$lines = @($top -split "`r?`n")
	$out = @(); $skip = $false
	foreach ($l in $lines) {
		if ($l -match '^// Truth table:') {
			$t = @(Format-Table $v "" " ")
			$out += "// Truth table:  " + $t[0]
			$out += @($t | Select-Object -Skip 1 | ForEach-Object { "//               $_" })
			$skip = $true; continue
		}
		if ($skip -and $l -match '^//\s+[01X]') { continue }
		$skip = $false
		if ($l -match '^//\s*VARIANTS:') { continue }
		if ($l -match '^//\s*EXPR:') { $out += "// EXPR: $(Convert-Expr $v $v.Expr)"; continue }
		$out += $l
	}
	[IO.File]::WriteAllText((Join-Path (Get-Location) "${proj}_top.v"), (($out -join "`r`n").TrimEnd() + "`r`n"), $utf8)

	# --- Claude's instructions: this student's table + how to read the background written for the original
	$p = [IO.File]::ReadAllText((Join-Path (Get-Location) "tools\tutor_prompt.md"))
	$md = @(("| " + ($v.Vars -join " ") + " | Y |"), ("|" + ("---|" * 2))) +
		@(Get-StudentRows $v | ForEach-Object { "| " + (($_.Bits.ToCharArray()) -join " ") + " | " + $(if ($_.Dc) { "X" } else { $_.Y }) + " |" })
	$ren = @(0..($n - 1) | ForEach-Object { "original $($v.Vars[$_]) = this student's $($v.Vars[$v.P[$_]])$(if ($v.M[$_]) { "'" })" }) -join ", "
	$map = @($v.Rows | ForEach-Object { "$($_.Bits) -> $(Convert-Row $v $_.Bits)" }) -join ", "
	$note = @(
		"",
		"**This student's own table.** Every student gets this exercise with the variables renamed and/or",
		"complemented (made from their ID), so the table above is this student's, and the background below was",
		"written for the original table. Renaming: $ren. Original row -> this student's row: $map.",
		"Translate every expression, row, group and K-map position of the background through this renaming before",
		"you use it (the number of terms and literals, uniqueness and every other property stay the same).",
		"The rows named in the questions of answer.txt are already this student's rows.",
		$(if ($v.Expr) { "This student's starting expression (written in answer.txt): Y = $(Convert-Expr $v $v.Expr)  - the original was Y = $($v.Expr)." } else { "" }),
		"")
	$pl = @($p -split "`r?`n"); $po = @(); $done = $false; $inTable = $false
	foreach ($l in $pl) {
		if (-not $done -and $l -match '^\|') { if (-not $inTable) { $po += $md; $inTable = $true }; continue }
		if ($inTable) { $po += $note; $inTable = $false; $done = $true }
		$po += $l
	}
	[IO.File]::WriteAllText((Join-Path (Get-Location) "tools\tutor_personal.md"), ($po -join "`r`n"), $utf8)

	# --- answer.txt: the table goes in place of @TABLE@, rows named in the questions are renamed
	$a = [IO.File]::ReadAllLines((Join-Path (Get-Location) "answer.txt"), $utf8)
	if (-not ($a | Where-Object { $_ -match '@TABLE@|@EXPR@' })) { return $false }
	$ao = @()
	foreach ($l in $a) {
		if ($l -match '@TABLE@') { $ao += "#  (the table of ID $sid)"; $ao += @(Format-Table $v "#     " "  "); continue }
		if ($l -match '@EXPR@') { $ao += ($l -replace '@EXPR@', (Convert-Expr $v $v.Expr)) + "      (ID $sid)"; continue }
		if ($l -match '^#\s*\S') { $l = Convert-Text $v $l }
		$ao += $l
	}
	[IO.File]::WriteAllLines((Join-Path (Get-Location) "answer.txt"), $ao, $utf8)
	return $true
}

# Adds (or replaces) one code line in moodle.txt and keeps the others: "ex3: CODE" from run.bat,
# "ex3-Q2: CODE" from Q2_POS.bat. The student hands this file in on Moodle. Returns the code.
function Save-MoodleCode($sid, $proj, $label) {
	$utf8 = New-Object System.Text.UTF8Encoding($false)
	$f = Join-Path (Get-Location) "moodle.txt"
	$codes = [ordered]@{}
	if (Test-Path $f) {
		foreach ($l in [IO.File]::ReadAllLines($f, $utf8)) { if ($l -match '^\s*(ex\d+(?:-Q\d+)?):\s*(\S+)\s*$') { $codes[$Matches[1]] = $Matches[2] } }
	}
	$codes[$label] = Get-Code $sid $label
	$out = @("Exercise $($proj -replace '\D', '')", "ID: $sid") + @($codes.Keys | Sort-Object | ForEach-Object { "${_}: $($codes[$_])" })
	[IO.File]::WriteAllLines($f, $out, $utf8)
	return $codes[$label]
}
