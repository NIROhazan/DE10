# Exercise 0 runner: PREDICT line in answer.txt -> history.txt -> Quartus -> board
# No prediction, no run. Each successful run clears the PREDICT line, so every run needs a new one.
# Kept ASCII so Windows PowerShell 5.1 reads it without a BOM.

$ErrorActionPreference = "Stop"
Set-Location (Split-Path $PSScriptRoot -Parent)
$proj = "ex0"
$utf8 = New-Object System.Text.UTF8Encoding($false)

function Step($t) { Write-Host ""; Write-Host "=== $t ===" -ForegroundColor Cyan }
function Fail($t) { Write-Host $t -ForegroundColor Red; exit 1 }

# ---------------------------------------------------------------- 1. Prediction
Step "1/3  Your prediction"
if (-not (Test-Path "answer.txt")) { Fail "answer.txt is missing." }
$lines = [IO.File]::ReadAllLines((Resolve-Path "answer.txt"), $utf8)
$idx = -1
for ($i = 0; $i -lt $lines.Count; $i++) { if ($lines[$i] -match '^\s*PREDICT:') { $idx = $i } }
if ($idx -lt 0) { Fail "answer.txt has no PREDICT: line. Put it back at the bottom of the file." }
$pred = ($lines[$idx] -replace '^\s*PREDICT:', '').Trim()
if ($pred -eq "") {
	Write-Host "  The PREDICT: line at the bottom of answer.txt is empty."
	Fail "  Write what you expect to see on the LEDs, save, and run again. No prediction - no run."
}

# The knobs as they are now in ex0_top.v
$knobs = (Get-Content "ex0_top.v" | Where-Object { $_ -match '^\s*localparam\s+(\w+)\s*=\s*([^;]+);' } |
	ForEach-Object { $null = $_ -match '^\s*localparam\s+(\w+)\s*=\s*([^;]+);'; "$($Matches[1])=$($Matches[2].Trim())" }) -join "  "
Write-Host "  Knobs:      $knobs"
Write-Host "  Prediction: $pred"
$stamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
[IO.File]::AppendAllText((Join-Path (Get-Location) "history.txt"),
	"[$stamp]  $knobs`r`n  PREDICT: $pred`r`n", $utf8)

# ---------------------------------------------------------------- 2. Quartus
Step "2/3  Quartus compiles (1-2 minutes)"
$qbin = @("C:\altera\13.0sp1\quartus\bin64", "C:\altera\13.0sp1\quartus\bin",
          "C:\altera\13.0\quartus\bin64", "C:\altera\13.0\quartus\bin") |
	Where-Object { Test-Path (Join-Path $_ "quartus_sh.exe") } | Select-Object -First 1
if (-not $qbin) { Fail "Quartus II 13.0sp1 not found under C:\altera." }

& (Join-Path $qbin "quartus_sh.exe") --flow compile $proj > compile.log 2>&1
if ($LASTEXITCODE -ne 0) {
	Select-String -Path compile.log -Pattern "^Error" | Select-Object -First 5 | ForEach-Object { Write-Host "  $($_.Line)" }
	[IO.File]::AppendAllText((Join-Path (Get-Location) "history.txt"), "  -> compile FAILED`r`n", $utf8)
	Fail "Compile FAILED - details in compile.log"
}
$fit = Get-Content "output_files\$proj.fit.summary"
$fit | Where-Object { $_ -match 'Total logic elements|Total registers' } | ForEach-Object { Write-Host "  $($_.Trim())" }
# Warnings worth reading: a number too big for its bits, and LEDs Quartus proved never change
Select-String -Path compile.log -Pattern 'truncated value|is stuck at' |
	ForEach-Object { Write-Host "  $($_.Line.Trim())" -ForegroundColor Yellow }

# ---------------------------------------------------------------- 3. Board
Step "3/3  Programming the board"
& (Join-Path $qbin "quartus_pgm.exe") -c USB-Blaster -m JTAG -o "p;output_files\$proj.sof" > program.log 2>&1
if ($LASTEXITCODE -ne 0) {
	Select-String -Path program.log -Pattern "Error" | Select-Object -First 3 | ForEach-Object { Write-Host "  $($_.Line)" }
	Fail "Programming FAILED. Is the board on, the USB cable in the BLASTER port, and the switch on RUN?"
}
Write-Host "  Board programmed - watch LEDR9..LEDR0." -ForegroundColor Green

# Used up: the next run needs a new prediction
$lines[$idx] = "PREDICT:"
[IO.File]::WriteAllLines((Resolve-Path "answer.txt"), $lines, $utf8)
Write-Host "  Was your prediction right? Write what you SAW in answer.txt (the PREDICT: line is now empty)."
