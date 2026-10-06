# week 4 ex9 - glitches (lecture 4: "When a single input change causes an output to change multiple times").
# The board hides 8 functions Y of A B C, each built as a 2-term SOP from slow-motion gates. The student finds Y,
# the switch flip that makes Y glitch, its timing, and the term that removes it. The functions and the glitches
# are only hashes in secrets.txt; the gate delays of each puzzle are open (puzzles.txt).
# Kept ASCII so Windows PowerShell 5.1 reads it without a BOM.

$script:Title = "Exercise 9 - glitches"
$script:BoardHelp = @(
	"Board: A = SW0, B = SW1, C = SW2.  Puzzle = SW9..SW7 (0-7, in binary).  SW6 = the fix (keep it DOWN until Q4).",
	"Y (LEDG0) is a hidden 2-term SOP of A B C, built from NOT / AND / OR gates in slow motion (1 tick = 0.1 s).",
	"After you flip ONE switch: HEX3 HEX2 = ticks until the LAST change of Y, HEX1 HEX0 = until the FIRST,",
	"LEDR3..0 = how many times Y changed. Wait until the numbers stop before you read Y.")

$script:Delays = @{}
foreach ($l in [IO.File]::ReadAllLines((Join-Path $PSScriptRoot "puzzles.txt"))) {
	if ($l -match '^delay (\d+) (\d+) (\d+) (\d+)') { $script:Delays[[int]$Matches[1]] = @([int]$Matches[2], [int]$Matches[3], [int]$Matches[4]) }
}

function Get-QuestionList {
	@([pscustomobject]@{ Id = "Q1"; Name = "FUNCTION" }, [pscustomobject]@{ Id = "Q2"; Name = "GLITCH" },
	  [pscustomobject]@{ Id = "Q3"; Name = "TIMING" }, [pscustomobject]@{ Id = "Q4"; Name = "FIX" })
}

function Get-Question($sid, $qid, $k) {
	$p = Get-Num $sid $qid $k 8
	$d = $script:Delays[$p]
	$pz = "Puzzle $p (SW9..SW7 = $(Get-Bin $p 3))."
	switch ($qid) {
		"Q1" {
			return @{ Asked = "puzzle $p"; Format = "a minimal SOP of A B C, e.g. AB' + BC"
				Lines = @("$pz  Find Y: try all 8 rows of A B C (wait for Y to settle), draw the K-map,",
					"and type Y as a MINIMAL sum of products.")
				Checks = @(@{ Parts = "sop"; Vars = "ABC"; Secret = "sop$p" }) }
		}
		"Q2" {
			return @{ Asked = "puzzle $p"; Format = "the switch number, then A B C BEFORE the flip, e.g. 1 011  (A B C = SW0 SW1 SW2)"
				Lines = @("$pz  Exactly one flip of one switch makes Y glitch: Y should not change, but it goes wrong",
					"for a moment and comes back (LEDR shows 2 changes). Which switch, and what were A B C before the flip?",
					"Hint: on your K-map, look for two neighbouring 1s that are in different circles.")
				Checks = @(@{ Parts = "dec", "bin"; Secret = "glitch$p" }) }
		}
		"Q3" {
			return @{ Asked = "puzzle $p delays $($d -join ' ')"; Format = "three numbers of ticks: first last length, e.g. 5 9 4"
				Lines = @("$pz  Its gates: NOT = $($d[0]) ticks, AND = $($d[1]) ticks, OR = $($d[2]) ticks.",
					"For the glitch of this puzzle (find it as in Q2): after the flip, at which tick does Y go wrong (HEX1 HEX0),",
					"at which tick is it right again (HEX3 HEX2), and for how many ticks is it wrong?  Work it out from the",
					"gates on each path first, then check on the board.")
				Checks = @(@{ Parts = "dec", "dec", "dec"; Value = "$($d[1] + $d[2]) $($d[0] + $d[1] + $d[2]) $($d[0])" }) }
		}
		"Q4" {
			return @{ Asked = "puzzle $p"; Format = "one product term, e.g. AC'"
				Lines = @("$pz  Which ONE product term, added to Y, removes the glitch without changing Y?",
					"(Raise SW6: the board adds that term to its circuit - the glitch is gone. Which term is it?)")
				Checks = @(@{ Parts = "sop"; Vars = "ABC"; Secret = "fix$p" }) }
		}
	}
}
