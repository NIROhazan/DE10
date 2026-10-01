# Exercise runner: answer.txt -> Claude -> student_logic.v + feedback.txt -> Quartus -> board
# Kept ASCII so Windows PowerShell 5.1 reads it without a BOM.
param([string]$Mode = "")

$ErrorActionPreference = "Stop"
Set-Location (Split-Path $PSScriptRoot -Parent)
$proj = Split-Path -Leaf (Get-Location)   # ex1, ex2, ... = the .qpf name

function Step($t) { Write-Host ""; Write-Host "=== $t ===" -ForegroundColor Cyan }
function Fail($t) { Write-Host $t -ForegroundColor Red; exit 1 }

# ---------------------------------------------------------------- 1. Claude
Step "1/3  Claude reads answer.txt"
if (-not (Test-Path "answer.txt")) { Fail "answer.txt is missing." }

$claude = (Get-Command claude -ErrorAction SilentlyContinue).Source
if (-not $claude) {
	$c = Join-Path $env:USERPROFILE ".local\bin\claude.exe"
	if (Test-Path $c) { $claude = $c }
}
if (-not $claude) { Fail "Claude Code is not installed on this computer (claude.exe not found)." }

$before = (Get-FileHash "student_logic.v").Hash
if (Test-Path "feedback.txt") { Remove-Item "feedback.txt" }

Write-Host "  Claude is checking your answers - about a minute..."
# --restricted: no shell, file tools confined to this folder. Only Read and Write exist.
& $claude -p "Follow the instructions in tools/tutor_prompt.md exactly. The student's answers are in answer.txt." `
	--restricted --strict-mcp-config --tools "Read,Write" --permission-mode acceptEdits `
	> claude.log 2>&1
if ($LASTEXITCODE -ne 0) {
	Get-Content claude.log | Select-Object -Last 5
	Fail "Claude failed. Is it logged in? Open a command prompt, run  claude  once and log in."
}
if (-not (Test-Path "feedback.txt")) { Fail "Claude did not write feedback.txt - see claude.log" }
$after = (Get-FileHash "student_logic.v").Hash
if ($after -eq $before) { Write-Host "  (student_logic.v unchanged - same answers as last time?)" -ForegroundColor Yellow }

Write-Host "  Your expressions as Claude read them:"
Get-Content "student_logic.v" | Where-Object { $_ -match '^\s*assign' } | ForEach-Object { Write-Host "   $_" }
Start-Process notepad.exe "feedback.txt"
Write-Host "  Feedback opened in Notepad (feedback.txt)."
if ($Mode -eq "check") { exit 0 }

# ---------------------------------------------------------------- 2. Quartus
Step "2/3  Quartus compiles your logic"
$qbin = @("C:\altera\13.0sp1\quartus\bin64", "C:\altera\13.0sp1\quartus\bin",
          "C:\altera\13.0\quartus\bin64", "C:\altera\13.0\quartus\bin") |
	Where-Object { Test-Path (Join-Path $_ "quartus_sh.exe") } | Select-Object -First 1
if (-not $qbin) { Fail "Quartus II 13.0sp1 not found under C:\altera." }

& (Join-Path $qbin "quartus_sh.exe") --flow compile $proj > compile.log 2>&1
if ($LASTEXITCODE -ne 0) {
	Select-String -Path compile.log -Pattern "^Error" | Select-Object -First 5 | ForEach-Object { Write-Host "  $($_.Line)" }
	Fail "Compile FAILED - details in compile.log"
}

# Quartus simplifies the logic. If the alarm LEDR[9] ends up tied to GND, the tool has
# proved that every answer equals Y on every row, not just the ones you tried.
$map = Get-Content "output_files\$proj.map.rpt" -Raw
if ($map -match 'Pin "LEDR\[9\]" is stuck at GND') {
	Write-Host "  Quartus proof: LEDR9 is stuck at GND - all your answers equal Y on every row." -ForegroundColor Green
} else {
	Write-Host "  LEDR9 is real logic - at least one answer differs from Y on some row. Find it with the switches." -ForegroundColor Yellow
}

# ---------------------------------------------------------------- 3. Board
Step "3/3  Programming the board"
& (Join-Path $qbin "quartus_pgm.exe") -c USB-Blaster -m JTAG -o "p;output_files\$proj.sof" > program.log 2>&1
if ($LASTEXITCODE -ne 0) {
	Select-String -Path program.log -Pattern "Error" | Select-Object -First 3 | ForEach-Object { Write-Host "  $($_.Line)" }
	Fail "Programming FAILED. Is the board on, the USB cable in the BLASTER port, and the switch on RUN?"
}
Write-Host "  Board programmed." -ForegroundColor Green
# The switch / LED map is the "//   " block at the top of <proj>_top.v
Get-Content "${proj}_top.v" | Where-Object { $_ -match '^//   \S' } | ForEach-Object { Write-Host ("  " + $_.Substring(5)) }
