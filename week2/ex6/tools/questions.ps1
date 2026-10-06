# week 2 ex6 - CMOS gates (lecture 2: nMOS / pMOS, pull-up and pull-down networks, NAND, NOR3, AND2 from transistors).
# The board hides one CMOS gate per puzzle; the student finds it from its truth table, then answers about
# its transistors. The right answers are only hashes in secrets.txt. Get-Question returns Lines, Format, Checks, Asked.
# Kept ASCII so Windows PowerShell 5.1 reads it without a BOM.

$script:Title = "Exercise 6 - CMOS gates"
$script:BoardHelp = @(
	"Board: A = SW0, B = SW1, C = SW2.  Puzzle number = SW9..SW6 in binary (shown on HEX0).",
	"Y of the puzzle's hidden CMOS gate: LEDG0 and HEX3.",
	"Gates: NOT  NAND2  NOR2  NAND3  NOR3  AND2  OR2   (a gate may use any of A B C)",
	"       AOI21: Y = NOT(x*y + z)    OAI21: Y = NOT((x + y)*z)    z = the 'lone' input")
$script:Synonyms = @{ "AND" = "AND2"; "OR" = "OR2"; "INV" = "NOT"; "INVERTER" = "NOT"
	"SERIAL" = "SERIES"; "PARALEL" = "PARALLEL"; "SW0" = "A"; "SW1" = "B"; "SW2" = "C" }

function Get-QuestionList {
	@([pscustomobject]@{ Id = "Q1"; Name = "NAME" }, [pscustomobject]@{ Id = "Q2"; Name = "COUNT" },
	  [pscustomobject]@{ Id = "Q3"; Name = "NETWORKS" }, [pscustomobject]@{ Id = "Q4"; Name = "INPUTS" },
	  [pscustomobject]@{ Id = "Q5"; Name = "AOI" })
}

function Get-Puzzles($sid, $tag, $k, $pool, $n) {
	$left = @($script:pools[$pool]); $out = @()
	for ($i = 0; $i -lt $n; $i++) {
		$it = Get-Pick $sid "$tag$i" $k $left
		$out += [int]($it -replace '\D', ''); $left = @($left | Where-Object { $_ -ne $it })
	}
	return $out
}

function Get-Question($sid, $qid, $k) {
	switch ($qid) {
		"Q1" {
			$p = Get-Puzzles $sid "Q1" $k "name" 2
			return @{ Asked = "puzzles $($p -join ' ')"; Format = "two gate names, e.g. NAND3 OR2"
				Lines = @("Which gates are puzzle $($p[0]) and puzzle $($p[1])?  (not AOI21 / OAI21)")
				Checks = @(@{ Parts = "word"; Secret = "name$($p[0])" }, @{ Parts = "word"; Secret = "name$($p[1])" }) }
		}
		"Q2" {
			$p = Get-Puzzles $sid "Q2" $k "count" 3
			return @{ Asked = "puzzles $($p -join ' ')"; Format = "three numbers, e.g. 4 6 2"
				Lines = @("How many transistors does each gate need in CMOS:  puzzle $($p[0]),  puzzle $($p[1]),  puzzle $($p[2])?",
					"(AND2 / OR2 = a NAND2 / NOR2 followed by a NOT, like in the lecture)")
				Checks = @(@{ Parts = "dec"; Secret = "count$($p[0])" }, @{ Parts = "dec"; Secret = "count$($p[1])" }, @{ Parts = "dec"; Secret = "count$($p[2])" }) }
		}
		"Q3" {
			$p = (Get-Puzzles $sid "Q3" $k "cmos" 1)[0]
			return @{ Asked = "puzzle $p"; Format = "gate, pull-up, pull-down, transistors, e.g. NOR2 SERIES PARALLEL 4"
				Lines = @("Puzzle $p is a NAND or a NOR. Which gate is it, are its pMOS (pull-up network) in SERIES or",
					"PARALLEL, are its nMOS (pull-down network) in SERIES or PARALLEL, and how many transistors?")
				Checks = @(@{ Parts = "word", "word", "word", "dec"; Secret = "cmos$p" }) }
		}
		"Q4" {
			$p = (Get-Puzzles $sid "Q4" $k "inputs" 1)[0]
			return @{ Asked = "puzzle $p"; Format = "the gate and its two inputs, e.g. NOR2 A C"
				Lines = @("Puzzle $p is a 2-input gate. Which gate, and which two of A B C are its inputs?",
					"(the third switch does not change Y at all)")
				Checks = @(@{ Parts = "word", "word", "word"; Secret = "inputs$p" }) }
		}
		"Q5" {
			$p = Get-Puzzles $sid "Q5" $k "aoi" 2
			return @{ Asked = "puzzles $($p -join ' ')"; Format = "for each puzzle the gate and its lone input, e.g. AOI21 B OAI21 A"
				Lines = @("Puzzles $($p[0]) and $($p[1]) are AOI21 or OAI21 gates.",
					"For each one: which gate, and which input is the lone one (z)?")
				Checks = @(@{ Parts = "word", "word"; Secret = "aoi$($p[0])" }, @{ Parts = "word", "word"; Secret = "aoi$($p[1])" }) }
		}
	}
}
