# Exercise 0 (equation) runner: equation.txt -> equation.v -> Quartus -> board
# The equation uses A, B, C and + * ~ ' ! ^ & | . ( ) 0 1 (parser in eq.ps1); bit by bit on 4 bits.
# Kept ASCII so Windows PowerShell 5.1 reads it without a BOM.

$ErrorActionPreference = "Stop"
Set-Location (Split-Path $PSScriptRoot -Parent)
$proj = "ex0_eq"
$utf8 = New-Object System.Text.UTF8Encoding($false)

function Step($t) { Write-Host ""; Write-Host "=== $t ===" -ForegroundColor Cyan }
function Fail($t) { Write-Host $t -ForegroundColor Red; exit 1 }

. (Join-Path $PSScriptRoot "eq.ps1")

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

try { $ver, $f = Read-Equation $text } catch { Fail "  Y = $text`n  $($_.Exception.Message)" }
Write-Host "  Y = $text"
Write-Host "  Verilog:  assign Y = $ver;"

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
