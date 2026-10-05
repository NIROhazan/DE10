# Exercise runner: answer.txt -> Claude -> student_logic.v + feedback.txt -> Quartus -> board
# Every student has their own truth table, made from their ID (variant.ps1); a correct, programmed exercise
# gives a code that goes into moodle.txt for Moodle.
# Kept ASCII so Windows PowerShell 5.1 reads it without a BOM.
param([string]$Mode = "")

$ErrorActionPreference = "Stop"
Set-Location (Split-Path $PSScriptRoot -Parent)
$proj = Split-Path -Leaf (Get-Location)   # ex1, ex2, ... = the .qpf name

$qbin = @("C:\altera\13.0sp1\quartus\bin64", "C:\altera\13.0sp1\quartus\bin",
          "C:\altera\13.0\quartus\bin64", "C:\altera\13.0\quartus\bin") |
	Where-Object { Test-Path (Join-Path $_ "quartus_sh.exe") } | Select-Object -First 1

function Step($t) { Write-Host ""; Write-Host "=== $t ===" -ForegroundColor Cyan }

# The course folder (the one with locked\): the exercise sits one or two levels below it (week3\exN)
function Get-CourseRoot {
	$r = Split-Path (Get-Location) -Parent
	while ($r -and -not (Test-Path (Join-Path $r "locked"))) { $r = Split-Path $r -Parent }
	if ($r) { return $r } else { return (Split-Path (Get-Location) -Parent) }
}
# Every stop locks the board: locked\locked.sof in the course folder shows "Err" with all LEDs off, so the board never
# keeps an older design that looks correct while the answers are empty or wrong.
function Lock-Board {
	$sof = Join-Path (Get-CourseRoot) "locked\locked.sof"
	if (-not $qbin -or -not (Test-Path $sof)) { return }
	$ErrorActionPreference = "Continue"
	& (Join-Path $qbin "quartus_pgm.exe") -c USB-Blaster -m JTAG -o "p;$sof" > lock.log 2>&1
	if ($LASTEXITCODE -eq 0) { Write-Host "  The board now shows Err - it shows your logic only when every answer is correct." -ForegroundColor Yellow }
}
function Fail($t, [switch]$NoLock) {
	Write-Host $t -ForegroundColor Red
	if (-not $NoLock) { Lock-Board }
	exit 1
}

# ---------------------------------------------------------------- 0. This student's table
if (-not (Test-Path "answer.txt")) { Fail "answer.txt is missing." }
. (Join-Path $PSScriptRoot "variant.ps1")
$sid = Get-StudentId
try { $fresh = New-PersonalFiles $sid $proj } catch { Fail "Cannot make your truth table: $($_.Exception.Message)" -NoLock }
if ($fresh) {
	Write-Host ""
	Write-Host "  ID $sid - your own truth table is now in answer.txt." -ForegroundColor Green
	Write-Host "  Open answer.txt, solve it for YOUR table, save, and run run.bat again."
	exit 0
}

# ---------------------------------------------------------------- 1. Claude
Step "1/3  Claude reads answer.txt   (ID $sid)"

# Empty answers stop here: no Claude, no compile, no board.
# Answer lines are "NAME =": expressions with an English name (SOP, POS, MIN, ...) and the
# questions, written in Hebrew as TAV + digit (shown as Q1..Q4 - the console cannot print Hebrew).
$sheet = @(Get-Content "answer.txt" -Encoding UTF8)
# A name counts as answered if it is filled in on any line (answers pasted at the top of the file are fine).
$names = [ordered]@{}
$where = @{}
$shown = @()
for ($i = 0; $i -lt $sheet.Count; $i++) {
	if ($sheet[$i] -notmatch '^\s*([A-Za-z]\w*|[\u05D0-\u05EA]+\s*\d+)\s*=\s*(.*)$') { continue }
	$n = $Matches[1] -replace '\s', ''
	$isQ = $n -match '^[\u05D0-\u05EA]+(\d+)$'
	if ($isQ) { $n = "Q" + $Matches[1] } else { $n = $n.ToUpper() }
	$null = $sheet[$i] -match '=\s*(.*)$'
	$filled = $Matches[1].Trim() -ne ""
	$names[$n] = [bool]$names[$n] -or $filled
	if (-not $filled) { $where[$n] = $i + 1 }
	if ($isQ) { $text = if ($filled) { "$n = (answered)" } else { "$n =" } } else { $text = $sheet[$i].Trim() }
	$shown += ("   line {0,3}:  {1}" -f ($i + 1), $text)
}
$empty = @($names.Keys | Where-Object { -not $names[$_] })
# Show exactly what was read, so a stale copy open in an editor is obvious.
Write-Host "  Reading $((Resolve-Path 'answer.txt').Path)  (saved $((Get-Item 'answer.txt').LastWriteTime.ToString('HH:mm:ss')))"
$shown | ForEach-Object { Write-Host $_ }
if ($names.Count -eq 0) { Fail "answer.txt has no answer lines (SOP = ...). Take a fresh copy of the file." }
if ($empty.Count -gt 0) {
	Write-Host "  Empty answers in answer.txt: $(($empty | ForEach-Object { "$_ (line $($where[$_]))" }) -join ', ')" -ForegroundColor Red
	Write-Host "  Fill in every answer on its own line, right after the = sign (expressions like  SOP = A'B + AB,"
	Write-Host "  the questions Q1..Q4 in your own words), save the file, and run again."
	Fail "  Nothing was checked - your logic was NOT put on the board."
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
"" | & $claude -p "Follow the instructions in tools/tutor_personal.md exactly. The student's answers are in answer.txt." `
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
# Every expression in student_logic.v is evaluated on every row of the table in <proj>_top.v (X rows are
# skipped), with the rules of its header - see tools/check.ps1. Only correct answers go on the board.
# (Quartus is not used for this: it does not always reduce a correct 4-variable answer to a constant.)
. (Join-Path $PSScriptRoot "check.ps1")
try { $board = Get-Board (Join-Path (Get-Location) "${proj}_top.v") } catch { Fail $_.Exception.Message }
$answers = [ordered]@{}
foreach ($line in (Get-Content "student_logic.v" | Where-Object { $_ -match '^\s*assign\s+(\w+)\s*=\s*(.+);' })) {
	$null = $line -match '^\s*assign\s+(\w+)\s*=\s*(.+);'
	$answers[$Matches[1]] = $Matches[2]
}
$wrong = Test-Answers $board $answers
if ($wrong -gt 0) {
	Write-Host ""
	Fail "  Your logic was NOT put on the board - only correct answers go there. Read feedback.txt, fix answer.txt, run again."
}
if ($Mode -eq "check") { exit 0 }

# ---------------------------------------------------------------- 2. Quartus
Step "2/3  Quartus compiles your logic"
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
	Fail "Programming FAILED. Is the board on, the USB cable in the BLASTER port, and the switch on RUN?" -NoLock
}
Write-Host "  Board programmed." -ForegroundColor Green
# Done: the code for Moodle (made from the ID, so a friend's code does not fit)
$code = Save-MoodleCode $sid $proj $proj
Write-Host "  Your code for ${proj}: $code   - hand in the file moodle.txt on Moodle." -ForegroundColor Green
# The switch / LED map is the "//   " block at the top of <proj>_top.v
Get-Content "${proj}_top.v" | Where-Object { $_ -match '^//   \S' } | ForEach-Object { Write-Host ("  " + $_.Substring(5)) }
