# Checks the moodle.txt files students handed in, for every exercise (instructor only).
# Usage: download all submissions of an assignment from Moodle, unzip, then:  verify.bat <folder>
# Reads every .txt under the folder: the "ID:" line and the code lines (ex0: "Q1: CODE" ...; exercises:
# "w3-ex3: CODE" from run.bat, "w3-ex3-Q2: CODE" from Q2_POS.bat, "w2-ex5-Q1: CODE" in week 2;
# class exercise: "ce-Q05: D6EA", the 4 hex digits the board showed).
# Prints a table and writes grades.csv. Kept ASCII so Windows PowerShell 5.1 reads it without a BOM.
param([string]$Dir = (Get-Location).Path)

$ErrorActionPreference = "Stop"
. "C:\DE10\week3\ex0_eq\tools\student.ps1"	# Get-Code - the same key as run.bat in every exercise

# Class exercise (C:\DE10\week3\class_exercise): "ce-Q05: D6EA" - the code the BOARD showed. Same as gen.py:
# login = MD5("DE10ce|ID"), secret = HMAC-SHA256(key.txt, "Q05|login"). Without steps: digits = secret, last digit =
# check digit. With steps ("| steps n" in questions.txt): the code of the last step n-1 = mix(secret, n-1) + check digit.
$ceKey = [Text.Encoding]::ASCII.GetBytes(([IO.File]::ReadAllText((Join-Path $PSScriptRoot "class_exercise\key.txt"))).Trim())
$ceMac = New-Object Security.Cryptography.HMACSHA256 (, $ceKey)
function Get-CeMac($m) { return $ceMac.ComputeHash([Text.Encoding]::ASCII.GetBytes($m)) }
$ceSteps = @{}
foreach ($l in [IO.File]::ReadAllLines("C:\DE10\week3\class_exercise\tools\questions.txt")) {
	if ($l -match '^\[(Q\d+)\].*\|\s*steps\s+(\d+)') { $ceSteps[$Matches[1]] = [int]$Matches[2] }
}
# week 2 class exercise (C:\DE10\week2\class_exercise): "w2ce-Q05: XXXX", the same scheme with the prefix "w2|"
$w2Steps = @{}
$w2q = "C:\DE10\week2\class_exercise\tools\questions.txt"
if (Test-Path $w2q) {
	foreach ($l in [IO.File]::ReadAllLines($w2q)) { if ($l -match '^\[(Q\d+)\].*\|\s*steps\s+(\d+)') { $w2Steps[$Matches[1]] = [int]$Matches[2] } }
}
# week 4 class exercise: "w4ce-Q05: XXXX", prefix "w4|"
$w4Steps = @{}
$w4q = "C:\DE10\week4\class_exercise\tools\questions.txt"
if (Test-Path $w4q) {
	foreach ($l in [IO.File]::ReadAllLines($w4q)) { if ($l -match '^\[(Q\d+)\].*\|\s*steps\s+(\d+)') { $w4Steps[$Matches[1]] = [int]$Matches[2] } }
}
# weeks 5-11 class exercises: "w<N>ce-Q05: XXXX", prefix "w<N>|" - one column "Weeks" (w5:20/20 w6:3/20 ...)
$wkSteps = @{}
foreach ($n in 5..11) {
	$f = "C:\DE10\week$n\class_exercise\tools\questions.txt"
	if (Test-Path $f) {
		$wkSteps[$n] = @{}
		foreach ($l in [IO.File]::ReadAllLines($f)) { if ($l -match '^\[(Q\d+)\].*\|\s*steps\s+(\d+)') { $wkSteps[$n][$Matches[1]] = [int]$Matches[2] } }
	}
}
function Get-CeCode($sid, $qid, $pre = "", $steps = $null) {
	if ($null -eq $steps) { $steps = $ceSteps }
	$b = [Security.Cryptography.MD5]::Create().ComputeHash([Text.Encoding]::ASCII.GetBytes("DE10ce|$sid"))
	$s = ($b[0] + 256 * $b[1]) % 1024
	$h = Get-CeMac "$pre$qid|$s"
	$k = 0
	if ($steps.ContainsKey($qid)) {
		$k = $steps[$qid] - 1
		$k1 = Get-CeMac "K1|$k"; $k2 = Get-CeMac "K2|$k"
		$x = (($h[0] * 256) + $h[1]) -bxor (($k1[0] * 256) + $k1[1])
		$x = ($x + ((($x -shl 5) -bor ($x -shr 11)) -band 0xFFFF)) -band 0xFFFF
		$x = $x -bxor ($x -shr 7)
		$c = (($x + ($k2[0] * 256) + $k2[1]) -band 0xFFFF) -shr 4
	} else {
		$c = (($h[0] * 256) + $h[1]) -shr 4
	}
	$d3 = $c -shr 8; $d2 = ($c -shr 4) -band 15; $d1 = $c -band 15
	$d0 = ($d3 + 3 * $d2 + 5 * $d1 + 7 + 9 * ($s -band 15) + 11 * (($s -shr 4) -band 15) + 13 * ($s -shr 8) + 15 * $k) % 16
	return ('{0:X}{1:X}{2:X}{3:X}' -f $d3, $d2, $d1, $d0)
}

$rows = @()
foreach ($file in Get-ChildItem $Dir -Recurse -Filter *.txt) {
	$text = [IO.File]::ReadAllText($file.FullName)
	if ($text -notmatch '(?m)^\s*ID:\s*(\d{6,10})\s*$') { continue }
	$sid = $Matches[1]
	$ok = @(); $bad = @()
	foreach ($m in [regex]::Matches($text, '(?m)^\s*(Q\d+|(?:w\d+-)?ex\d+(?:-Q\d+)?):\s*([A-Z0-9]{5})\s*$')) {
		$label = $m.Groups[1].Value
		if ($m.Groups[2].Value -eq (Get-Code $sid $label)) { $ok += $label } else { $bad += $label }
	}
	$ce = @()
	foreach ($m in [regex]::Matches($text, '(?m)^\s*ce-(Q\d+):\s*([0-9A-Fa-f]{4})\s*$')) {
		if ($m.Groups[2].Value.ToUpper() -eq (Get-CeCode $sid $m.Groups[1].Value)) { $ce += $m.Groups[1].Value } else { $bad += "ce-$($m.Groups[1].Value)" }
	}
	$ce = @($ce | Sort-Object -Unique)
	$w2 = @()
	foreach ($m in [regex]::Matches($text, '(?m)^\s*w2ce-(Q\d+):\s*([0-9A-Fa-f]{4})\s*$')) {
		if ($m.Groups[2].Value.ToUpper() -eq (Get-CeCode $sid $m.Groups[1].Value "w2|" $w2Steps)) { $w2 += $m.Groups[1].Value } else { $bad += "w2ce-$($m.Groups[1].Value)" }
	}
	$w2 = @($w2 | Sort-Object -Unique)
	$w4 = @()
	foreach ($m in [regex]::Matches($text, '(?m)^\s*w4ce-(Q\d+):\s*([0-9A-Fa-f]{4})\s*$')) {
		if ($m.Groups[2].Value.ToUpper() -eq (Get-CeCode $sid $m.Groups[1].Value "w4|" $w4Steps)) { $w4 += $m.Groups[1].Value } else { $bad += "w4ce-$($m.Groups[1].Value)" }
	}
	$w4 = @($w4 | Sort-Object -Unique)
	$wk = @()
	foreach ($n in ($wkSteps.Keys | Sort-Object)) {
		$got = @()
		foreach ($m in [regex]::Matches($text, "(?m)^\s*w$($n)ce-(Q\d+):\s*([0-9A-Fa-f]{4})\s*$")) {
			if ($m.Groups[2].Value.ToUpper() -eq (Get-CeCode $sid $m.Groups[1].Value "w$n|" $wkSteps[$n])) { $got += $m.Groups[1].Value } else { $bad += "w$($n)ce-$($m.Groups[1].Value)" }
		}
		$got = @($got | Sort-Object -Unique)
		if ($got.Count) { $wk += "w$($n):$($got.Count)/$($wkSteps[$n].Count)" }
	}
	$ok = @($ok | Sort-Object -Unique)
	$q = @($ok | Where-Object { $_ -like "Q*" })
	$ex = @($ok | Where-Object { $_ -notlike "Q*" })
	# The Moodle folder name carries the student's name - compare it with the ID by eye
	$rows += [pscustomobject]@{
		ID = $sid
		Ex0 = $(if ($q.Count) { "$($q.Count)/20" } else { "" })
		Exercises = ($ex -join " ")
		Class = $(if ($ce.Count) { "$($ce.Count)/$($ceSteps.Count)" } else { "" })
		Week2 = $(if ($w2.Count) { "$($w2.Count)/$($w2Steps.Count)" } else { "" })
		Week4 = $(if ($w4.Count) { "$($w4.Count)/$($w4Steps.Count)" } else { "" })
		Weeks = ($wk -join " ")
		Bad = ($bad -join " "); From = $file.Directory.Name }
}
if ($rows.Count -eq 0) { Write-Host "No moodle.txt files (with an ID: line) under $Dir"; exit 1 }

# The same ID handed in twice for the same exercise = someone used a friend's ID
$dup = @($rows | Group-Object { "$($_.ID)|$($_.Exercises)|$($_.Ex0 -ne '')|$($_.Class -ne '')|$($_.Week2 -ne '')|$($_.Week4 -ne '')|$($_.Weeks)" } | Where-Object { $_.Count -gt 1 } | ForEach-Object { $_.Group } | ForEach-Object { $_.From })
foreach ($r in $rows) {
	$r | Add-Member Note ($(if ($r.Bad) { "BAD CODES: $($r.Bad)  " } else { "" }) + $(if ($dup -contains $r.From) { "SAME ID IN 2 FILES" } else { "" }))
}
$rows | Sort-Object ID | Format-Table ID, Ex0, Exercises, Class, Week2, Week4, Weeks, Note, From -AutoSize
$rows | Sort-Object ID | Select-Object ID, Ex0, Exercises, Class, Week2, Week4, Weeks, Note, From |
	Export-Csv (Join-Path $Dir "grades.csv") -NoTypeInformation -Encoding UTF8
Write-Host "grades.csv written to $Dir"
