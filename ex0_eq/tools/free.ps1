# Exercise 0 free mode: programs the board with the equation on the Y = line of equation.txt.
# Kept ASCII so Windows PowerShell 5.1 reads it without a BOM.

$ErrorActionPreference = "Stop"
Set-Location (Split-Path $PSScriptRoot -Parent)
$utf8 = New-Object System.Text.UTF8Encoding($false)
. (Join-Path $PSScriptRoot "eq.ps1")
. (Join-Path $PSScriptRoot "board.ps1")

function Fail($t) { Write-Host $t -ForegroundColor Red; exit 1 }

if (-not (Test-Path "equation.txt")) { Fail "equation.txt is missing." }
$lines = @([IO.File]::ReadAllLines((Resolve-Path "equation.txt"), $utf8) |
	Where-Object { $_ -match '^\s*[Yy]\s*=' })
if ($lines.Count -eq 0) { Fail "equation.txt has no Y = line. Example:  Y = A + B*C" }
$text = ($lines[-1] -replace '^\s*[Yy]\s*=', '').Trim().TrimEnd(';')
if ($text -eq "") { Fail "The Y = line in equation.txt is empty. Example:  Y = A + B*C" }

try {
	$ver, $null = Read-Equation $text
	Write-Host "  Y = $text"
	Write-Host "  Verilog:  assign Y = $ver;"
	Send-Sof (Get-Sof $text)
} catch { Fail "  $($_.Exception.Message)" }
Write-Host "  Board programmed. A on HEX0, B on HEX1, C on HEX2, Y = $text on HEX3." -ForegroundColor Green
