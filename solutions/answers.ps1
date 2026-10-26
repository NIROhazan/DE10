# A student's own exercise and its answers (instructor only). The name is the one in moodle.txt:
#   answers.bat w3-ex4 3160009489 -> week 3: the student's table, the answer key renamed for them, and
#                                    week3\exN\answer_filled_<ID>.txt (their sheet filled in - for testing run.bat)
#   answers.bat w4-ex5 3160009489 -> week 4 ex1..ex7 (Karnaugh maps), the same
#   answers.bat w4-ex9 3160009489 -> week 4 ex8..ex10: the student's questions, answers and codes (like week 2)
#   answers.bat ex0 3160009489    -> week3\ex0_eq: the 20 questions with answers and codes
#   answers.bat w2-ex5 3160009489 -> week 2: the student's questions, answers and codes
#   answers.bat ce 3160009489     -> class exercise (lecture 3): login number, every answer (switches) and code
#   answers.bat ce2 3160009489    -> the week 2 class exercise, the same (ce4 = week 4, ce5..ce11 = weeks 5-11)
# Kept ASCII so Windows PowerShell 5.1 reads it without a BOM.
param([Parameter(Mandatory = $true)][string]$Ex, [Parameter(Mandatory = $true)][string]$Sid, [string]$Template = "")
[Console]::OutputEncoding = [Text.Encoding]::UTF8
$ErrorActionPreference = "Stop"
$Ex = $Ex.ToLower()
if ($Ex -match '^ce(5|6|7|8|9|10|11)$') { & python (Join-Path $PSScriptRoot "week$($Matches[1])\class_exercise\gen_w$($Matches[1]).py") --id $Sid; exit }
if ($Ex -eq "ce4") { & python (Join-Path $PSScriptRoot "week4\class_exercise\gen_w4.py") --id $Sid; exit }
if ($Ex -eq "ce2") { & python (Join-Path $PSScriptRoot "week2\class_exercise\gen_w2.py") --id $Sid; exit }
if ($Ex -eq "ce") { & python (Join-Path $PSScriptRoot "class_exercise\gen.py") --id $Sid; exit }
if ($Ex -eq "ex0" -or $Ex -eq "w3-ex0") { & (Join-Path $PSScriptRoot "week3\ex0_eq\answers.ps1") $Sid; exit }
if ($Ex -match '^w2-(ex[1-6])$') { & (Join-Path $PSScriptRoot "week2\answers.ps1") $Matches[1] $Sid; exit }
if ($Ex -match '^w4-(ex(8|9|10))$') { & (Join-Path $PSScriptRoot "week4\answers.ps1") $Matches[1] $Sid; exit }
if ($Ex -match '^w3-(ex([1-9]|10))$') { $week = "week3"; $name = $Matches[1] }
elseif ($Ex -match '^w4-(ex[1-7])$') { $week = "week4"; $name = $Matches[1] }
else { Write-Host "Usage: answers.bat w2-ex1..w2-ex6 | ce | ce2 | ce4..ce11 | ex0 | w3-ex1..w3-ex10 | w4-ex1..w4-ex10  <ID>"; exit 1 }

$repo = "C:\DE10\$week\$name"		# $Ex is the label of the codes (w3-ex4, ex5) and seeds the table
$sol = Join-Path $PSScriptRoot "$week\$name"
$rel = "$week/$name"
. (Join-Path $repo "tools\variant.ps1")
. (Join-Path $repo "tools\check.ps1")
$v = Get-Variant $Sid $Ex (Join-Path $repo "tools\base_top.v")
$n = $v.Vars.Count
$utf8 = New-Object System.Text.UTF8Encoding($false)

Write-Host "$Ex   ID $Sid"
Write-Host ("renaming: " + (@(0..($n - 1) | ForEach-Object { "$($v.Vars[$_]) -> $($v.Vars[$v.P[$_]])$(if ($v.M[$_]) { "'" })" }) -join ", "))
if ($v.Story) { Write-Host "story: $($v.Story.En)" }
if ($v.Net.Count) { Write-Host ("circuit: " + (@($v.Net | ForEach-Object { Convert-Expr $v $_ }) -join ";  ")) }
Format-Table $v "   " " " | ForEach-Object { Write-Host $_ }
Write-Host "   code: $(Get-Code $Sid $Ex)"
Write-Host ""

# The key: expression lines renamed; other lines (row lists, notes) shown as written for the original
$key = [IO.File]::ReadAllLines((Join-Path $sol "ANSWERS.md"), $utf8)
$fill = @{}
foreach ($l in $key) {
	if ($l -match '^- ([A-Z][A-Z0-9]*)\s*(?:\([^)]*\))?\s*=\s*(.+?)(\s{2,}(?=[^\s\[]).*)?$') {
		$name = $Matches[1]; $e = $Matches[2].Trim()
		if ($e -match '^the same as (\w+)') { $e = $fill[$Matches[1]] }
		elseif ($e -match '^@MUX(\d)$') {
			# a 4:1 mux with selects A B: the two rows of this AB decide D
			$k = [int]$Matches[1]; $sr = Get-StudentRows $v
			$y0 = $sr[2 * $k].Y; $y1 = $sr[2 * $k + 1].Y
			$e = @("0", "C", "C'", "1")[2 * $y0 + $y1]
		}
		elseif ($e -match '^@(CSOP|MSOP|MPOS)$') {
			# computed from this student's own table (the column of this output when there are several)
			$kind = $Matches[1]
			$col = [array]::IndexOf(@($v.Targets), $name)
			$sr = @(Get-StudentRows $v | ForEach-Object { [pscustomobject]@{ Bits = $_.Bits; Y = $(if ($col -ge 0) { [int]("" + $_.Y[$col]) } else { $_.Y }); Dc = $_.Dc } })
			if ($kind -eq "CSOP") {
				$e = (@($sr | Where-Object { $_.Y -eq 1 -and -not $_.Dc } | ForEach-Object { $b = $_.Bits
					-join (0..($v.Vars.Count - 1) | ForEach-Object { $v.Vars[$_] + $(if ($b[$_] -eq '0') { "'" }) }) }) -join " + ")
			} else { $e = Get-MinExpr $sr $v.Vars ($kind -eq "MPOS") }
		}
		elseif ($e -eq '@DEC') {
			$sr = Get-StudentRows $v
			$e = (@(0..($sr.Count - 1) | Where-Object { $sr[$_].Y -eq 1 -and -not $sr[$_].Dc } | ForEach-Object { "y$_" }) -join " + ")
		}
		else {
			# the expression is renamed; a [theorem] after it is kept as written
			$tag = ""
			if ($e -match '^(.*?)\s*(\[.*\])\s*$') { $e = $Matches[1]; $tag = "   " + $Matches[2] }
			$e = (Convert-Expr $v $e) + $tag
		}
		$fill[$name] = $e
		Write-Host "$name = $e"
	} elseif ($l -match '^- Q(\d)\s*(?:\([^)]*\))?:\s*(.+)$') {
		$fill["Q" + $Matches[1]] = Convert-Text $v $Matches[2]
		Write-Host "Q$($Matches[1]): $(Convert-Text $v $Matches[2])"
	}
}

# The student's sheet, filled - from the committed template, so local test edits do not leak in
$tpl = if ($Template) { [IO.File]::ReadAllText($Template, $utf8) } else { try { $ErrorActionPreference = "Continue"; (& git -C "C:\DE10" show "HEAD:$rel/answer.txt" 2>$null) -join "`n" } catch { "" } finally { $ErrorActionPreference = "Stop" } }
if ($tpl -notmatch '@TABLE@|@EXPR@') { $tpl = [IO.File]::ReadAllText((Join-Path $repo "answer.txt"), $utf8) }	# not committed yet
$out = @()
foreach ($l in ($tpl -split "`n")) {
	if ($l -match '@TABLE@') { $out += "#  (the table of ID $Sid)"; $out += @(Format-Table $v "#     " "  "); continue }
	if ($l -match '@EXPR@') { $out += ($l -replace '@EXPR@', (Convert-Expr $v $v.Expr)) + "      (ID $Sid)"; continue }
	if ($l -match '^#\s*\S') { $l = Convert-Text $v $l }
	if ($l -match '^([A-Z][A-Z0-9]*)\s*=\s*$' -and $fill[$Matches[1]]) { $l = "$($Matches[1]) = $($fill[$Matches[1]])" }
	if ($l -match '^[\u05D0-\u05EA]+(\d)\s*=\s*$' -and $fill["Q" + $Matches[1]]) { $l = $l.TrimEnd() + " " + $fill["Q" + $Matches[1]] }
	$out += $l
}
$path = Join-Path $sol "answer_filled_$Sid.txt"
[IO.File]::WriteAllLines($path, $out, $utf8)
Write-Host ""
Write-Host "Filled sheet: $path"
