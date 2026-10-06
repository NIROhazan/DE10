# week 4 ex10 - combinational logic with always / case / casez (lecture 4, Harris ch. 4: casez, ? = don't care,
# default). The board holds 16 casez blocks (tools/puzzles.txt, the same code); the student reads the code,
# predicts, and checks on the board. Answers are computed here from the code.
# Kept ASCII so Windows PowerShell 5.1 reads it without a BOM.

$script:Title = "Exercise 10 - case and casez"
$script:BoardHelp = @(
	"Board: puzzle = SW9..SW6 (shown on HEX1), a = SW3..SW0 (shown on HEX0), y = LEDG3..LEDG0 and HEX3 (hex).",
	"Every puzzle is one always block:  always @(*) casez (a) ... default: y = 4'h0; endcase")

$script:Puz = @{}; $script:Bits = @{}
foreach ($l in [IO.File]::ReadAllLines((Join-Path $PSScriptRoot "puzzles.txt"))) {
	if ($l -match '^puzzle (\d+) (.+)$') {
		$script:Puz[[int]$Matches[1]] = @($Matches[2].Trim() -split '\s+' | ForEach-Object { $x = $_ -split '='; [pscustomobject]@{ Pat = $x[0]; Val = [Convert]::ToInt32($x[1], 16) } })
	} elseif ($l -match '^bit (\d+) (\d) (\S+ \S+)') { $script:Bits["$($Matches[1]) $($Matches[2])"] = $Matches[3] }
}

function Get-QuestionList {
	@([pscustomobject]@{ Id = "Q1"; Name = "VALUE" }, [pscustomobject]@{ Id = "Q2"; Name = "DEFAULT" },
	  [pscustomobject]@{ Id = "Q3"; Name = "NEVER" }, [pscustomobject]@{ Id = "Q4"; Name = "BIT_SOP" })
}

function Test-Pat($pat, $a) {
	for ($i = 0; $i -lt 4; $i++) {
		$c = $pat[$i]
		if ($c -ne '?' -and [int]("" + $c) -ne (($a -shr (3 - $i)) -band 1)) { return $false }
	}
	return $true
}
# The line that gives y for a (1..n), 0 = default
function Get-Line($lines, $a) {
	for ($i = 0; $i -lt $lines.Count; $i++) { if (Test-Pat $lines[$i].Pat $a) { return $i + 1 } }
	return 0
}
function Format-Code($p) {
	$l = @("Puzzle $p (SW9..SW6 = $(Get-Bin $p 4)):", "    always @(*)", "      casez (a)")
	$i = 0
	foreach ($x in $script:Puz[$p]) { $i++; $l += "        4'b$($x.Pat): y = 4'h$($x.Val.ToString('X'));      // line $i" }
	$l += "        default: y = 4'h0;"
	$l += "      endcase"
	return $l
}

function Get-Question($sid, $qid, $k) {
	$p = Get-Num $sid $qid $k 16
	$lines = $script:Puz[$p]
	switch ($qid) {
		"Q1" {
			$a = Get-Num $sid "Q1a" $k 16
			$n = Get-Line $lines $a
			$y = if ($n) { $lines[$n - 1].Val } else { 0 }
			return @{ Asked = "puzzle $p a = $(Get-Bin $a 4)"; Format = "y in hex, e.g. B"
				Lines = @(Format-Code $p) + @("Read the code (not the board): what is y when a = 4'b$(Get-Bin $a 4)?  Then check it on the board.")
				Checks = @(@{ Parts = "hex"; Value = $y.ToString("X") }) }
		}
		"Q2" {
			$n = @(0..15 | Where-Object { (Get-Line $lines $_) -eq 0 }).Count
			return @{ Asked = "puzzle $p"; Format = "one number, e.g. 3"
				Lines = @(Format-Code $p) + @("For how many of the 16 values of a does the default line give y?",
					"(If that default line were deleted, these are exactly the values for which y would keep its old value - a latch.)")
				Checks = @(@{ Parts = "dec"; Value = "$n" }) }
		}
		"Q3" {
			$never = @(1..$lines.Count | Where-Object { $i = $_; -not @(0..15 | Where-Object { (Get-Line $lines $_) -eq $i }).Count })
			return @{ Asked = "puzzle $p"; Format = "a line number, e.g. 2"
				Lines = @(Format-Code $p) + @("One line of this casez NEVER gives y, for any a. Which line, and (for yourself) why?",
					"Remember: casez takes the FIRST line that matches.")
				Checks = @(@{ Parts = "dec"; Value = "$($never[0])" }) }
		}
		"Q4" {
			$b = Get-Num $sid "Q4b" $k 4
			return @{ Asked = "puzzle $p y[$b]"; Format = "a minimal SOP of A B C D, e.g. AB' + C'D"
				Lines = @(Format-Code $p) + @("Bit y[$b] is a function of the 4 bits of a:  A = a[3] (SW3), B = a[2], C = a[1], D = a[0] (SW0).",
					"Write the truth table of y[$b] (16 rows), draw the K-map, and type y[$b] as a MINIMAL sum of products.")
				Checks = @(@{ Parts = "sop"; Vars = "ABCD"; Value = $script:Bits["$p $b"] }) }
		}
	}
}
