# week 2 ex4 - extension (lecture 2: sign-extension, zero-extension, increasing bit width).
# Get-Question returns Lines (what the student reads), Format, Checks (see common.ps1) and Asked (for results.txt).
# Kept ASCII so Windows PowerShell 5.1 reads it without a BOM.

$script:Title = "Exercise 4 - sign-extension and zero-extension"
$script:BoardHelp = @(
	"Board: X = SW3..SW0 (4 bits, HEX0). HEX3 HEX2 and LEDG7..LEDG0 = X extended to 8 bits:",
	"SW9 down = sign-extension, SW9 up = zero-extension. The HEX show bit patterns, not signed values.")

function Get-QuestionList {
	@([pscustomobject]@{ Id = "Q1"; Name = "SIGN" }, [pscustomobject]@{ Id = "Q2"; Name = "ZERO" },
	  [pscustomobject]@{ Id = "Q3"; Name = "WIDE" }, [pscustomobject]@{ Id = "Q4"; Name = "MAKE" },
	  [pscustomobject]@{ Id = "Q5"; Name = "MIX" })
}

function Get-Question($sid, $qid, $k) {
	switch ($qid) {
		"Q1" {
			$x = 8 + (Get-Num $sid "Q1" $k 8)
			return @{ Asked = (Get-Bin $x 4); Format = "the 8 bits in hex, then the two's complement value in decimal, e.g. FB -5"
				Lines = @("X = $(Get-Bin $x 4) (4-bit two's complement).",
					"Sign-extend it to 8 bits: what is it in hex, and what number is it (decimal)?")
				Checks = @(@{ Parts = "hex", "dec"; Value = "$((240 + $x).ToString('X')) $($x - 16)" }) }
		}
		"Q2" {
			$x = 8 + (Get-Num $sid "Q2" $k 8)
			return @{ Asked = (Get-Bin $x 4); Format = "the 8 bits in hex, then the value of the 8 bits in decimal (two's complement), e.g. 0B 11"
				Lines = @("X = $(Get-Bin $x 4). Zero-extend it to 8 bits.",
					"What is it in hex, and what number are the 8 bits as two's complement (decimal)?",
					"Was X (as a 4-bit two's complement number) the same number?  Think about it - not typed.")
				Checks = @(@{ Parts = "hex", "dec"; Value = "$($x.ToString('X')) $x" }) }
		}
		"Q3" {
			$b = 128 + (Get-Num $sid "Q3" $k 128)
			return @{ Asked = $b.ToString("X2"); Format = "two 16-bit hex numbers: sign-extended, then zero-extended, e.g. FF9C 009C"
				Lines = @("The byte  $($b.ToString('X2'))  (hex). Extend it to 16 bits:",
					"  sign-extended (hex),  zero-extended (hex)?")
				Checks = @(@{ Parts = "hex", "hex"; Value = "$((65280 + $b).ToString('X')) $($b.ToString('X'))" }) }
		}
		"Q4" {
			$d = Get-Pick $sid "Q4" $k @(-8..-1 + 1..7)
			return @{ Asked = "$d"; Format = "the switch numbers you raised, e.g. 3 1 0"
				Lines = @("With SW9 down, make HEX3 HEX2 show the 8-bit two's complement form of $d (decimal).",
					"Which switches are up?")
				Checks = @(@{ Parts = "sw"; Value = (Get-Switches (($d + 16) % 16)) }) }
		}
		"Q5" {
			$x = 8 + (Get-Num $sid "Q5x" $k 8); $y = Get-Num $sid "Q5y" $k 256
			$xs = 240 + $x
			$s = ($xs + $y) % 256
			$sv = if ($s -ge 128) { $s - 256 } else { $s }
			return @{ Asked = "$(Get-Bin $x 4) + $($y.ToString('X2'))"; Format = "the 8-bit sum in hex, then its two's complement value in decimal, e.g. 7A 122"
				Lines = @("Add the 4-bit two's complement X = $(Get-Bin $x 4) to the 8-bit two's complement Y = $($y.ToString('X2')) (hex).",
					"Extend X to 8 bits first (use the board). The 8-bit sum in hex, and its value in decimal?")
				Checks = @(@{ Parts = "hex", "dec"; Value = "$($s.ToString('X')) $sv" }) }
		}
	}
}
