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

# Empty answers stop here: no Claude, no compile, no board.
# Expression lines are "NAME =" with an English name (SOP, POS, MIN, ...); the Hebrew question lines are not checked.
$sheet = Get-Content "answer.txt" -Encoding UTF8 | Where-Object { $_ -notmatch '^\s*#' }
$exprs = @($sheet | Where-Object { $_ -match '^\s*[A-Za-z]\w*\s*=' })
# A name counts as answered if it is filled in on any line (answers pasted at the top of the file are fine).
$names = [ordered]@{}
foreach ($l in $exprs) {
	$null = $l -match '^\s*([A-Za-z]\w*)\s*=\s*(.*)$'
	$n = $Matches[1].ToUpper()
	$names[$n] = [bool]$names[$n] -or ($Matches[2].Trim() -ne "")
}
$empty = @($names.Keys | Where-Object { -not $names[$_] })
if ($exprs.Count -eq 0) { Fail "answer.txt has no answer lines (SOP = ...). Take a fresh copy of the file." }
if ($empty.Count -gt 0) {
	Write-Host "  Empty answers in answer.txt: $($empty -join ', ')" -ForegroundColor Red
	Write-Host "  Write every expression after its = sign, save the file, and run again."
	Fail "  Nothing was checked and the board was NOT programmed."
}

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
# Empty stdin, and stderr only goes to the log: PowerShell 5.1 with "Stop" would treat a
# stderr warning from claude.exe as a fatal error.
$ErrorActionPreference = "Continue"
"" | & $claude -p "Follow the instructions in tools/tutor_prompt.md exactly. The student's answers are in answer.txt." `
	--restricted --strict-mcp-config --tools "Read,Write" --permission-mode acceptEdits `
	> claude.log 2>&1
$ErrorActionPreference = "Stop"
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

# ---------------------------------------------------------------- Truth-table check
# Every expression in student_logic.v is evaluated on every row of the table in <proj>_top.v
# (rows with dc = 1'b1 are X rows and are skipped). Only correct answers go on the board.
# (Quartus is not used for this: it does not always reduce a correct 4-variable answer to a constant.)
function Test-Expr([string]$expr, [hashtable]$val) {
	$script:tok = @([regex]::Matches($expr, "1'b[01]|[A-Za-z_]\w*|[~!&|^()]|\S") | ForEach-Object { $_.Value })
	$script:pos = 0
	function Peek { if ($script:pos -lt $script:tok.Count) { $script:tok[$script:pos] } else { "" } }
	function Next { $t = Peek; $script:pos++; $t }
	function POr  { $v = PXor; while ((Peek) -eq "|") { $null = Next; $v = $v -bor (PXor) }; $v }
	function PXor { $v = PAnd; while ((Peek) -eq "^") { $null = Next; $v = $v -bxor (PAnd) }; $v }
	function PAnd { $v = PNot; while ((Peek) -eq "&") { $null = Next; $v = $v -band (PNot) }; $v }
	function PNot {
		$t = Next
		if ($t -eq "~" -or $t -eq "!") { return 1 - (PNot) }
		if ($t -eq "(") { $v = POr; if ((Next) -ne ")") { throw "missing )" }; return $v }
		if ($t -eq "1'b0") { return 0 }
		if ($t -eq "1'b1") { return 1 }
		if ($val.ContainsKey($t)) { return $val[$t] }
		throw "cannot read '$t'"
	}
	$r = POr
	if ($script:pos -ne $script:tok.Count) { throw "cannot read '$(Peek)'" }
	$r
}

$top = Get-Content "${proj}_top.v" -Raw
if ($top -notmatch 'case\s*\(\{([^}]*)\}\)') { Fail "Cannot find the truth table in ${proj}_top.v." }
$vars = @($Matches[1] -split ',' | ForEach-Object { $_.Trim() })
$rows = @([regex]::Matches($top, "\d+'b([01]+):\s*(?:begin\s*)?Y\s*=\s*1'b([01]);(\s*dc\s*=\s*1'b1)?") |
	ForEach-Object { @{ bits = $_.Groups[1].Value; y = [int]$_.Groups[2].Value; dc = $_.Groups[3].Success } })
if ($rows.Count -ne [math]::Pow(2, $vars.Count)) { Fail "The truth table in ${proj}_top.v has $($rows.Count) rows - expected $([math]::Pow(2, $vars.Count))." }

$wrong = 0
foreach ($line in (Get-Content "student_logic.v" | Where-Object { $_ -match '^\s*assign\s+(\w+)\s*=\s*(.+);' })) {
	$null = $line -match '^\s*assign\s+(\w+)\s*=\s*(.+);'
	$name = $Matches[1]; $expr = $Matches[2]
	$bad = @()
	foreach ($r in $rows) {
		if ($r.dc) { continue }
		$val = @{}
		for ($i = 0; $i -lt $vars.Count; $i++) { $val[$vars[$i]] = [int]("" + $r.bits[$i]) }
		try { $v = Test-Expr $expr $val } catch { $bad = @("every row - run.bat could not read it ($($_.Exception.Message))"); break }
		if ($v -ne $r.y) { $bad += ($vars -join '') + "=" + $r.bits }
	}
	if ($bad.Count -gt 0) {
		$wrong++
		Write-Host "  $name : NOT equal to Y on  $($bad -join '  ')" -ForegroundColor Red
	} else {
		Write-Host "  $name : equals Y on every row" -ForegroundColor Green
	}
}
if ($wrong -gt 0) {
	Write-Host ""
	Fail "  The board was NOT programmed - only correct answers go on the board. Read feedback.txt, fix answer.txt, run again."
}
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

# Quartus simplifies the logic. When the alarm LEDR[9] ends up tied to GND the tool has proved it
# too (it does not always manage this, e.g. 4-variable parity, so it is only a bonus message).
if ((Get-Content "output_files\$proj.map.rpt" -Raw) -match 'Pin "LEDR\[9\]" is stuck at GND') {
	Write-Host "  Quartus proof as well: LEDR9 is stuck at GND." -ForegroundColor Green
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
