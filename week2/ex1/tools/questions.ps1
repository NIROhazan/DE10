# week 2 ex1 - binary, decimal, hex (lecture 2: number systems, bits / nibbles / bytes, powers of two).
# Get-Question returns Lines (what the student reads), Format, Checks (see common.ps1) and Asked (for results.txt).
# Kept ASCII so Windows PowerShell 5.1 reads it without a BOM.

$script:Title = "Exercise 1 - binary, decimal and hex"
$script:BoardHelp = @(
	"Board: N = SW9..SW0 (10 bits), shown on LEDR9..LEDR0 and in HEX on HEX2 HEX1 HEX0.",
	"Hold KEY3: the HEX go '-' and LEDG7..LEDG0 show the secret byte of puzzle SW5..SW0.")
$script:Synonyms = @{ "KILO" = "K"; "THOUSAND" = "K"; "MEGA" = "M"; "MILLION" = "M"; "GIGA" = "G"; "BILLION" = "G"; "TERA" = "T" }

function Get-QuestionList {
	@([pscustomobject]@{ Id = "Q1"; Name = "DEC" }, [pscustomobject]@{ Id = "Q2"; Name = "HEX" },
	  [pscustomobject]@{ Id = "Q3"; Name = "BIN" }, [pscustomobject]@{ Id = "Q4"; Name = "SECRET" },
	  [pscustomobject]@{ Id = "Q5"; Name = "BITS" }, [pscustomobject]@{ Id = "Q6"; Name = "POWERS" })
}

function Get-Question($sid, $qid, $k) {
	switch ($qid) {
		"Q1" {
			$d = 100 + (Get-Num $sid "Q1" $k 924)
			return @{ Asked = "$d"; Format = "the switch numbers you raised, e.g. 9 6 2 0"
				Lines = @("Make N = $d (decimal): raise the switches of its binary value.",
					"The board shows N in HEX, not in decimal - convert, then check the HEX digits yourself.")
				Checks = @(@{ Parts = "sw"; Value = (Get-Switches $d) }) }
		}
		"Q2" {
			$h = 256 + (Get-Num $sid "Q2" $k 768)
			return @{ Asked = $h.ToString("X3"); Format = "a decimal number, e.g. 683"
				Lines = @("Raise switches until HEX2 HEX1 HEX0 show  $($h.ToString('X3')).",
					"What is N in decimal?")
				Checks = @(@{ Parts = "dec"; Value = "$h" }) }
		}
		"Q3" {
			$v = 512 + (Get-Num $sid "Q3" $k 512)
			$sw = Get-Switches $v
			return @{ Asked = $sw; Format = "the hex number, then the decimal number, e.g. 2B7 695"
				Lines = @("Raise ONLY these switches: $(($sw -split ' ' | Sort-Object { -[int]$_ } | ForEach-Object { "SW$_" }) -join ' ')",
					"What is N in hex, and in decimal?")
				Checks = @(@{ Parts = "hex", "dec"; Value = "$($v.ToString('X')) $v" }) }
		}
		"Q4" {
			$item = Get-Pick $sid "Q4" $k $script:pools["Q4"]
			$p = [int]($item -replace '\D', '')
			return @{ Asked = "puzzle $p"; Format = "the byte in hex, then in decimal, e.g. 3C 60"
				Lines = @("Your puzzle number is $p (decimal). Put it in binary on SW5..SW0 (SW9..SW6 down).",
					"Hold KEY3: LEDG7..LEDG0 show a secret byte (LEDG0 = bit 0, lit = 1).",
					"Type the byte in hex and in decimal.")
				Checks = @(@{ Parts = "hex", "dec"; Secret = $item }) }
		}
		"Q5" {
			$d = 300 + (Get-Num $sid "Q5" $k 59700)
			$bits = [Convert]::ToString($d, 2).Length
			$hexd = [Math]::Ceiling($bits / 4)
			$max = [long][Math]::Pow(2, $bits) - 1
			return @{ Asked = "$d"; Format = "three decimal numbers, e.g. 12 3 4095"
				Lines = @("The number $d (decimal), written as an unsigned binary number:",
					"  how many bits does it need (at least)?",
					"  how many hex digits (nibbles) does it take?",
					"  what is the largest number those bits can hold (decimal)?")
				Checks = @(@{ Parts = "dec", "dec", "dec"; Value = "$bits $hexd $max" }) }
		}
		"Q6" {
			$e = @(11..39 | Where-Object { $_ % 10 -ne 0 })
			$n = Get-Pick $sid "Q6" $k $e
			$unit = @("", "K", "M", "G")[[Math]::Floor($n / 10)]
			$pre = [long][Math]::Pow(2, $n % 10)
			return @{ Asked = "2^$n"; Format = "a number and K / M / G, e.g. 16 M"
				Lines = @("Estimate 2^$n the way the lecture does (2^24 = 2^4 x 2^20 = about 16 M).",
					"K = 2^10 (kilo), M = 2^20 (mega), G = 2^30 (giga).")
				Checks = @(@{ Parts = "dec", "word"; Value = "$pre $unit" }) }
		}
	}
}
