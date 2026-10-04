# Exercise 0 (equation) runner: equation.txt -> equation.v -> Quartus -> board
# The equation uses A, B, C and + * ~ ' ! ^ & | . ( ) 0 1; every operation is bit by bit on 4 bits.
# Kept ASCII so Windows PowerShell 5.1 reads it without a BOM.

$ErrorActionPreference = "Stop"
Set-Location (Split-Path $PSScriptRoot -Parent)
$proj = "ex0_eq"
$utf8 = New-Object System.Text.UTF8Encoding($false)

function Step($t) { Write-Host ""; Write-Host "=== $t ===" -ForegroundColor Cyan }
function Fail($t) { Write-Host $t -ForegroundColor Red; exit 1 }

# ---------------------------------------------------------------- parser
# Each Parse* returns @(verilog, powershell) for the same expression.
#   or  := xor (('+' | '|') xor)*
#   xor := and ('^' and)*
#   and := not (('*' | '&' | '.')? not)*      AB = A*B
#   not := ('~' | '!') not | atom "'"*
#   atom:= A | B | C | 0 | 1 | '(' or ')'
$script:tok = @()
$script:pos = 0
function Peek { if ($script:pos -lt $script:tok.Count) { $script:tok[$script:pos] } else { "" } }
function Oops($t) {
	$where = $script:pos
	throw "$t (at character $($where + 1) of '$($script:tok -join '')')"
}
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

# ---------------------------------------------------------------- 1. Equation
Step "1/3  Your equation"
if (-not (Test-Path "equation.txt")) { Fail "equation.txt is missing." }
$lines = [IO.File]::ReadAllLines((Resolve-Path "equation.txt"), $utf8) |
	Where-Object { $_.Trim() -ne "" -and -not $_.TrimStart().StartsWith("#") }
if (-not $lines) { Fail "equation.txt has no equation. Write one on a line like:  Y = A + B*C" }
$yline = @($lines | Where-Object { $_ -match '^\s*[Yy]\s*=' })
$text = if ($yline.Count) { $yline[-1] } else { @($lines)[-1] }
$text = ($text -replace '^\s*[Yy]\s*=', '').Trim().TrimEnd(';')
if ($text -eq "") { Fail "The Y = line in equation.txt is empty. Example:  Y = A + B*C" }

$script:tok = @()
foreach ($ch in $text.ToCharArray()) {
	$s = ([string]$ch).ToUpper()
	if ($s -match '\s') { continue }
	if ($s -notmatch "^[ABC01+*.&|^~!'()]$") { Fail "  Y = $text`n  '$s' is not allowed. Use A B C 0 1 + * ~ ' ! ^ ( )" }
	$script:tok += $s
}
$script:pos = 0
try {
	$e = ParseOr
	if ($script:pos -lt $script:tok.Count) { Oops "unexpected '$(Peek)'" }
} catch {
	Fail "  Y = $text`n  $($_.Exception.Message)"
}
$ver = $e[0]; if ($ver.StartsWith("(") -and $ver.EndsWith(")")) { $ver = $ver.Substring(1, $ver.Length - 2) }
Write-Host "  Y = $text"
Write-Host "  Verilog:  assign Y = $ver;"

# A few switch settings to check the board against
$f = [scriptblock]::Create("param(`$A, `$B, `$C) ($($e[1])) -band 15")
Write-Host ""
Write-Host "  Try these on the switches:   A B C -> Y   (HEX0 HEX1 HEX2 -> HEX3)"
foreach ($t in @(@(0,0,0), @(15,7,7), @(5,3,6), @(12,5,1), @(9,2,4))) {
	$y = & $f $t[0] $t[1] $t[2]
	Write-Host ("                                {0:X} {1:X} {2:X} -> {3:X}" -f $t[0], $t[1], $t[2], $y)
}

$v = @(
	"// Written by run.bat from equation.txt - edit equation.txt, not this file.",
	"//   Y = $text",
	"module equation(",
	"	input  [3:0] A,",
	"	input  [3:0] B,",
	"	input  [3:0] C,",
	"	output [3:0] Y",
	"	);",
	"	assign Y = $ver;",
	"endmodule"
)
[IO.File]::WriteAllLines((Join-Path (Get-Location) "equation.v"), $v, $utf8)

# ---------------------------------------------------------------- 2. Quartus
Step "2/3  Quartus compiles (about a minute)"
$qbin = @("C:\altera\13.0sp1\quartus\bin64", "C:\altera\13.0sp1\quartus\bin",
          "C:\altera\13.0\quartus\bin64", "C:\altera\13.0\quartus\bin") |
	Where-Object { Test-Path (Join-Path $_ "quartus_sh.exe") } | Select-Object -First 1
if (-not $qbin) { Fail "Quartus II 13.0sp1 not found under C:\altera." }

& (Join-Path $qbin "quartus_sh.exe") --flow compile $proj > compile.log 2>&1
if ($LASTEXITCODE -ne 0) {
	Select-String -Path compile.log -Pattern "^Error" | Select-Object -First 5 | ForEach-Object { Write-Host "  $($_.Line)" }
	Fail "Compile FAILED - details in compile.log"
}
Get-Content "output_files\$proj.fit.summary" | Where-Object { $_ -match 'Total logic elements' } |
	ForEach-Object { Write-Host "  $($_.Trim())" }
# Bits of Y that never change (e.g. Y = A*A' is always 0)
Select-String -Path compile.log -Pattern 'LEDG\[[0-3]\].*stuck at' |
	ForEach-Object { Write-Host "  $($_.Line.Trim())" -ForegroundColor Yellow }

# ---------------------------------------------------------------- 3. Board
Step "3/3  Programming the board"
& (Join-Path $qbin "quartus_pgm.exe") -c USB-Blaster -m JTAG -o "p;output_files\$proj.sof" > program.log 2>&1
if ($LASTEXITCODE -ne 0) {
	Select-String -Path program.log -Pattern "Error" | Select-Object -First 3 | ForEach-Object { Write-Host "  $($_.Line)" }
	Fail "Programming FAILED. Is the board on, the USB cable in the BLASTER port, and the switch on RUN?"
}
Write-Host "  Board programmed. A on HEX0, B on HEX1, C on HEX2, Y = $text on HEX3." -ForegroundColor Green
