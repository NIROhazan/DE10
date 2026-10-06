# week 2 ex5 - mystery gates (lecture 2: NOT, BUF, AND, OR, NAND, NOR, XOR, XNOR, multi-input gates).
# The board hides 8 gates per puzzle; the student finds them from truth tables made with the switches.
# The right answers are only hashes in secrets.txt. Get-Question returns Lines, Format, Checks, Asked.
# Kept ASCII so Windows PowerShell 5.1 reads it without a BOM.

$script:Title = "Exercise 5 - mystery gates"
$script:BoardHelp = @(
	"Board: A = SW0, B = SW1, C = SW2.  Puzzle number = SW9..SW6 in binary (shown on HEX0).",
	"LEDG7..LEDG0 = eight hidden gates of that puzzle. Try every input row and write the truth tables.",
	"Gate names: BUF NOT AND OR NAND NOR XOR XNOR (inputs A B; BUF and NOT use only A)",
	"            AND3 OR3 NAND3 NOR3 XOR3 XNOR3 (inputs A B C)")
$script:Synonyms = @{ "AND2" = "AND"; "OR2" = "OR"; "NAND2" = "NAND"; "NOR2" = "NOR"; "XOR2" = "XOR"; "XNOR2" = "XNOR"
	"INV" = "NOT"; "INVERTER" = "NOT"; "BUFFER" = "BUF" }

function Get-QuestionList {
	@([pscustomobject]@{ Id = "Q1"; Name = "TWO" }, [pscustomobject]@{ Id = "Q2"; Name = "THREE" },
	  [pscustomobject]@{ Id = "Q3"; Name = "PAIR" }, [pscustomobject]@{ Id = "Q4"; Name = "FIND" },
	  [pscustomobject]@{ Id = "Q5"; Name = "ALL" })
}

# pXkY -> puzzle X, LED Y
function Split-Item($it) { if ($it -match '^p(\d+)k(\d+)$') { return [int]$Matches[1], [int]$Matches[2] } }

function Get-Question($sid, $qid, $k) {
	switch ($qid) {
		"Q1" {
			$p = Get-Num $sid "Q1p" $k 16
			$leds = @($script:pools["two"] | Where-Object { $_ -like "p${p}k*" })
			$i1 = Get-Pick $sid "Q1a" $k $leds
			$i2 = Get-Pick $sid "Q1b" $k @($leds | Where-Object { $_ -ne $i1 })
			$l1 = (Split-Item $i1)[1]; $l2 = (Split-Item $i2)[1]
			return @{ Asked = "puzzle $p LEDG$l1 LEDG$l2"; Format = "two gate names, e.g. NAND XOR"
				Lines = @("Puzzle $p.  Which gates drive LEDG$l1 and LEDG${l2}?  (both use only A and B)")
				Checks = @(@{ Parts = "word"; Secret = $i1 }, @{ Parts = "word"; Secret = $i2 }) }
		}
		"Q2" {
			$i1 = Get-Pick $sid "Q2a" $k $script:pools["three"]
			$p = (Split-Item $i1)[0]
			$i2 = Get-Pick $sid "Q2b" $k @($script:pools["two"] | Where-Object { $_ -like "p${p}k*" })
			$l1 = (Split-Item $i1)[1]; $l2 = (Split-Item $i2)[1]
			return @{ Asked = "puzzle $p LEDG$l1 LEDG$l2"; Format = "two gate names, e.g. NOR3 XNOR"
				Lines = @("Puzzle $p.  LEDG$l1 is a 3-input gate (A B C), LEDG$l2 is not.  Which gates are they?",
					"Use all 8 rows of A B C - a 2-input gate does not change when only C changes.")
				Checks = @(@{ Parts = "word"; Secret = $i1 }, @{ Parts = "word"; Secret = $i2 }) }
		}
		"Q3" {
			$p = [int]((Get-Pick $sid "Q3" $k $script:pools["pair"]) -replace '\D', '')
			return @{ Asked = "puzzle $p"; Format = "two LED numbers, then their two gate names, e.g. 2 6 AND NAND"
				Lines = @("Puzzle $p.  Exactly two of its LEDs ALWAYS show opposite values (one is the NOT of the other).",
					"Which two LEDs, and which gates are they?")
				Checks = @(@{ Parts = "dec", "dec", "word", "word"; Secret = "pair$p" }) }
		}
		"Q4" {
			$f1 = Get-Pick $sid "Q4a" $k $script:pools["find"]
			$f2 = Get-Pick $sid "Q4b" $k @($script:pools["find"] | Where-Object { $_ -ne $f1 -and ($_ -split '@')[1] -ne ($f1 -split '@')[1] })
			$g1, $k1 = $f1 -split '@'; $g2, $k2 = $f2 -split '@'
			return @{ Asked = "$f1 $f2"; Format = "two puzzle numbers (decimal), e.g. 5 12"
				Lines = @("Only ONE puzzle has $g1 on LEDG$k1, and only ONE puzzle has $g2 on LEDG$k2.",
					"Which puzzles?  (search the puzzles 0..15 on the board)")
				Checks = @(@{ Parts = "dec"; Secret = "find$f1" }, @{ Parts = "dec"; Secret = "find$f2" }) }
		}
		"Q5" {
			$p = [int]((Get-Pick $sid "Q5" $k $script:pools["all"]) -replace '\D', '')
			return @{ Asked = "puzzle $p"; Format = "eight gate names, LEDG7 first, e.g. OR NOT XOR3 AND NOR3 XNOR BUF NAND"
				Lines = @("Puzzle $p.  Name ALL eight gates, from LEDG7 down to LEDG0.")
				Checks = @(@{ Parts = "word", "word", "word", "word", "word", "word", "word", "word"; Secret = "all$p" }) }
		}
	}
}
