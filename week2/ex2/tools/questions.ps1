# week 2 ex2 - binary addition and overflow (lecture 2: addition, overflow, fixed number of bits).
# Get-Question returns Lines (what the student reads), Format, Checks (see common.ps1) and Asked (for results.txt).
# Kept ASCII so Windows PowerShell 5.1 reads it without a BOM.

$script:Title = "Exercise 2 - binary addition and overflow"
$script:BoardHelp = @(
	"Board: a 4-bit adder.  A = SW3..SW0 (HEX0)   B = SW7..SW4 (HEX1)   hold KEY0 = carry in (LEDG4).",
	"S = A + B (+1) on HEX3 and LEDG3..LEDG0, carry out (overflow) on LEDG7.")
$script:Synonyms = @{ "YES" = "1"; "ON" = "1"; "NO" = "0"; "OFF" = "0" }

function Get-QuestionList {
	@([pscustomobject]@{ Id = "Q1"; Name = "ADD" }, [pscustomobject]@{ Id = "Q2"; Name = "LIMIT" },
	  [pscustomobject]@{ Id = "Q3"; Name = "BACK" }, [pscustomobject]@{ Id = "Q4"; Name = "CARRYIN" },
	  [pscustomobject]@{ Id = "Q5"; Name = "BYTE" })
}

function Get-Question($sid, $qid, $k) {
	switch ($qid) {
		"Q1" {
			$a = 1 + (Get-Num $sid "Q1a" $k 15); $b = 1 + (Get-Num $sid "Q1b" $k 15)
			$t = $a + $b
			return @{ Asked = "$a + $b"; Format = "S as 4 bits, then the carry 0 or 1, e.g. 0110 1"
				Lines = @("Add $a + $b (decimal) in 4 bits. Work it out on paper first, then set A and B and check.",
					"What are the 4 bits of S, and the carry out?")
				Checks = @(@{ Parts = "bin", "word"; Value = "$(Get-Bin ($t % 16) 4) $([int]($t -ge 16))" }) }
		}
		"Q2" {
			$a = 2 + (Get-Num $sid "Q2" $k 14)
			return @{ Asked = "A = $a"; Format = "two decimal numbers, e.g. 9 8"
				Lines = @("A = $a (decimal).",
					"What is the SMALLEST B that lights the overflow LED (LEDG7), and the LARGEST B that does not?")
				Checks = @(@{ Parts = "dec", "dec"; Value = "$(16 - $a) $(15 - $a)" }) }
		}
		"Q3" {
			$a = 2 + (Get-Num $sid "Q3a" $k 14)
			$b = (16 - $a) + (Get-Num $sid "Q3b" $k $a)		# a + b >= 16, b <= 15
			$s = ($a + $b) % 16
			return @{ Asked = "A = $a, S = $($s.ToString('X')), carry 1"; Format = "a decimal number, e.g. 13"
				Lines = @("A = $a (decimal). The board shows S = $($s.ToString('X')) on HEX3, and LEDG7 (overflow) is ON.",
					"What is B (decimal)?")
				Checks = @(@{ Parts = "dec"; Value = "$b" }) }
		}
		"Q4" {
			$a = Get-Num $sid "Q4a" $k 16; $t = Get-Num $sid "Q4t" $k 16
			$b = ($t - $a - 1 + 32) % 16
			$c = [int](($a + $b + 1) -ge 16)
			return @{ Asked = "A = $a, S = $($t.ToString('X')) with KEY0"; Format = "B in decimal, then the carry 0 or 1, e.g. 7 0"
				Lines = @("A = $a (decimal), and you HOLD KEY0 (carry in = 1).",
					"Which B makes HEX3 show  $($t.ToString('X'))?  And is LEDG7 (carry out) on then?")
				Checks = @(@{ Parts = "dec", "word"; Value = "$b $c" }) }
		}
		"Q5" {
			$x = 16 + (Get-Num $sid "Q5x" $k 240); $y = 16 + (Get-Num $sid "Q5y" $k 240)
			$t = $x + $y
			return @{ Asked = "$($x.ToString('X2')) + $($y.ToString('X2'))"; Format = "the 8-bit sum in hex, then the final carry 0 or 1, e.g. 3C 1"
				Lines = @("Add two 8-bit numbers on the 4-bit board:  $($x.ToString('X2')) + $($y.ToString('X2'))  (hex).",
					"1) low nibbles: A = $($x.ToString('X2')[1]), B = $($y.ToString('X2')[1])  -> low digit of the sum, and a carry?",
					"2) high nibbles: A = $($x.ToString('X2')[0]), B = $($y.ToString('X2')[0]), and HOLD KEY0 if step 1 had a carry.",
					"Type the 8-bit sum in hex and the final carry out.")
				Checks = @(@{ Parts = "hex", "word"; Value = "$(($t % 256).ToString('X')) $([int]($t -ge 256))" }) }
		}
	}
}
