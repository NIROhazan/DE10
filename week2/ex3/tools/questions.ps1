# week 2 ex3 - signed numbers (lecture 2: sign/magnitude, two's complement, subtraction, overflow, ranges).
# Get-Question returns Lines (what the student reads), Format, Checks (see common.ps1) and Asked (for results.txt).
# Kept ASCII so Windows PowerShell 5.1 reads it without a BOM.

$script:Title = "Exercise 3 - signed numbers"
$script:BoardHelp = @(
	"Board: a 4-bit adder.  X = SW3..SW0 (HEX0)   Y = SW7..SW4 (HEX1)   S = X + Y on HEX3 and LEDG3..LEDG0.",
	"LEDG6 = carry out, LEDG7 = SIGNED overflow (two's complement). The HEX show bit patterns, not signed values.")
$script:Synonyms = @{ "YES" = "1"; "ON" = "1"; "NO" = "0"; "OFF" = "0" }

function Get-QuestionList {
	@([pscustomobject]@{ Id = "Q1"; Name = "TWOS" }, [pscustomobject]@{ Id = "Q2"; Name = "SIGNMAG" },
	  [pscustomobject]@{ Id = "Q3"; Name = "READ" }, [pscustomobject]@{ Id = "Q4"; Name = "SUB" },
	  [pscustomobject]@{ Id = "Q5"; Name = "OVERFLOW" }, [pscustomobject]@{ Id = "Q6"; Name = "RANGE" })
}

function Get-Question($sid, $qid, $k) {
	switch ($qid) {
		"Q1" {
			$d = 1 + (Get-Num $sid "Q1" $k 8)
			return @{ Asked = "-$d"; Format = "the switch numbers you raised, e.g. 3 1 0"
				Lines = @("Put -$d on X (SW3..SW0) as a 4-bit TWO'S COMPLEMENT number.",
					"Which switches are up?")
				Checks = @(@{ Parts = "sw"; Value = (Get-Switches ((16 - $d) % 16)) }) }
		}
		"Q2" {
			$d = 1 + (Get-Num $sid "Q2" $k 7)
			return @{ Asked = "-$d"; Format = "the switch numbers you raised, e.g. 3 1 0"
				Lines = @("Put -$d on X (SW3..SW0) as a 4-bit SIGN/MAGNITUDE number.",
					"Which switches are up?")
				Checks = @(@{ Parts = "sw"; Value = (Get-Switches (8 + $d)) }) }
		}
		"Q3" {
			$b = 129 + (Get-Num $sid "Q3" $k 127)
			return @{ Asked = (Get-Bin $b 8); Format = "three decimal numbers, e.g. 200 -72 -56"
				Lines = @("The 8 bits  $(Get-Bin $b 8)  - what number are they, read as:",
					"  unsigned,  sign/magnitude,  two's complement?  (decimal)")
				Checks = @(@{ Parts = "dec", "dec", "dec"; Value = "$b $(-($b - 128)) $($b - 256)" }) }
		}
		"Q4" {
			$a = (Get-Num $sid "Q4a" $k 16) - 8; $b = (Get-Num $sid "Q4b" $k 15) - 7		# b in -7..7, so -b fits
			$x = ($a + 16) % 16; $y = (16 - $b) % 16
			$s = ($x + $y) % 16
			$v = [int](($x -band 8) -eq ($y -band 8) -and ($s -band 8) -ne ($x -band 8))
			$sv = if ($s -ge 8) { $s - 16 } else { $s }
			return @{ Asked = "$a - ($b)"; Format = "S in hex, the overflow 0 or 1, S as a signed decimal, e.g. E 0 -2"
				Lines = @("Compute  $a - ($b)  on the board: X = $a, and Y = the NEGATIVE of $b (reverse the sign: invert, add 1).",
					"What does HEX3 show, is LEDG7 (signed overflow) on, and what signed number is S?")
				Checks = @(@{ Parts = "hex", "word", "dec"; Value = "$($s.ToString('X')) $v $sv" }) }
		}
		"Q5" {
			$a = 1 + (Get-Num $sid "Q5" $k 7)
			return @{ Asked = "X = $a / X = -$a"; Format = "two signed decimal numbers, e.g. 3 -5"
				Lines = @("X = ${a}: what is the SMALLEST positive Y that lights LEDG7 (signed overflow)?",
					"X = -${a}: what is the MOST NEGATIVE Y that does NOT light it?")
				Checks = @(@{ Parts = "dec", "dec"; Value = "$(8 - $a) $($a - 8)" }) }
		}
		"Q6" {
			$n = 5 + (Get-Num $sid "Q6" $k 12)
			$h = [long][Math]::Pow(2, $n - 1)
			return @{ Asked = "$n bits"; Format = "five decimal numbers, e.g. 255 -127 127 -128 127"
				Lines = @("Numbers with $n bits. Type:",
					"  the largest unsigned,  sign/magnitude min and max,  two's complement min and max.")
				Checks = @(@{ Parts = "dec", "dec", "dec", "dec", "dec"; Value = "$(2 * $h - 1) $(-($h - 1)) $($h - 1) $(-$h) $($h - 1)" }) }
		}
	}
}
