# Equation parser shared by run.ps1 and check.ps1 (dot-source it).
# Read-Equation "A + B*C" returns @(verilog, scriptblock); the scriptblock takes A B C and returns Y (0-15).
# Every operation is bit by bit on 4 bits.
#   or  := xor (('+' | '|') xor)*
#   xor := and ('^' and)*
#   and := not (('*' | '&' | '.')? not)*      AB = A*B
#   not := ('~' | '!') not | atom "'"*
#   atom:= A | B | C | 0 | 1 | '(' or ')'
# Kept ASCII so Windows PowerShell 5.1 reads it without a BOM.

$script:tok = @()
$script:pos = 0
function Peek { if ($script:pos -lt $script:tok.Count) { $script:tok[$script:pos] } else { "" } }
function Oops($t) { throw "$t (at character $($script:pos + 1) of '$($script:tok -join '')')" }
function ParseOr {
	$l = ParseXor
	while ((Peek) -eq "+" -or (Peek) -eq "|") {
		$script:pos++; $r = ParseXor
		$l = @("($($l[0]) | $($r[0]))", "($($l[1]) -bor $($r[1]))")
	}
	return $l
}
function ParseXor {
	$l = ParseAnd
	while ((Peek) -eq "^") {
		$script:pos++; $r = ParseAnd
		$l = @("($($l[0]) ^ $($r[0]))", "($($l[1]) -bxor $($r[1]))")
	}
	return $l
}
function ParseAnd {
	$l = ParseNot
	while ($true) {
		$p = Peek
		if ($p -eq "*" -or $p -eq "&" -or $p -eq ".") { $script:pos++ }
		elseif (-not ($p -match "^[ABC01(~!]$")) { break }
		$r = ParseNot
		$l = @("($($l[0]) & $($r[0]))", "($($l[1]) -band $($r[1]))")
	}
	return $l
}
function ParseNot {
	$p = Peek
	if ($p -eq "~" -or $p -eq "!") {
		$script:pos++; $x = ParseNot
		return @("(~$($x[0]))", "((-bnot $($x[1])) -band 15)")
	}
	$x = ParseAtom
	while ((Peek) -eq "'") {
		$script:pos++
		$x = @("(~$($x[0]))", "((-bnot $($x[1])) -band 15)")
	}
	return $x
}
function ParseAtom {
	$p = Peek
	switch -CaseSensitive ($p) {
		"A" { $script:pos++; return @("A", '$A') }
		"B" { $script:pos++; return @("B", '$B') }
		"C" { $script:pos++; return @("C", '$C') }
		"0" { $script:pos++; return @("4'h0", "0") }
		"1" { $script:pos++; return @("4'hF", "15") }
		"(" {
			$script:pos++; $x = ParseOr
			if ((Peek) -ne ")") { Oops "missing )" }
			$script:pos++
			return @("($($x[0]))", "($($x[1]))")
		}
		""  { Oops "the equation ends too early" }
		default { Oops "expected A, B, C, 0, 1, ( or ~ but found '$p'" }
	}
}

function Read-Equation($text) {
	$script:tok = @()
	foreach ($ch in $text.ToCharArray()) {
		$s = ([string]$ch).ToUpper()
		if ($s -match '\s') { continue }
		if ($s -notmatch "^[ABC01+*.&|^~!'()]$") { throw "'$s' is not allowed. Use A B C 0 1 + * ~ ' ! ^ ( )" }
		$script:tok += $s
	}
	$script:pos = 0
	$e = ParseOr
	if ($script:pos -lt $script:tok.Count) { Oops "unexpected '$(Peek)'" }
	$ver = $e[0]
	if ($ver.StartsWith("(") -and $ver.EndsWith(")")) { $ver = $ver.Substring(1, $ver.Length - 2) }
	$f = [scriptblock]::Create("param(`$A, `$B, `$C) ($($e[1])) -band 15")
	return @($ver, $f)
}

# The four digits the board shows, left to right (HEX3 HEX2 HEX1 HEX0 = Y C B A), for a set of raised switches
function Get-Display($f, [int[]]$sw) {
	$v = 0; foreach ($n in $sw) { $v = $v -bor (1 -shl $n) }
	$A = $v -band 15; $B = ($v -shr 4) -band 7; $C = ($v -shr 7) -band 7
	$Y = & $f $A $B $C
	return ("{0:X}{1:X}{2:X}{3:X}" -f $Y, $C, $B, $A)
}
