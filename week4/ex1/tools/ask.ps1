# One question of the exercise, asked in the console: Q1_SOP.bat = ask.ps1 -Q Q1.
# The questions are the "// ASK" lines of tools/base_top.v. The student types the answer here; it is
# checked at once (equals Y on every row + the ONLY rules of check.ps1), then Quartus puts it on the board.
# The code for Moodle comes only when the GRADE rules hold too (canonical / minimal, as the question asks).
# The written questions in Hebrew stay in answer.txt (run.bat + Claude) - the console cannot show Hebrew.
# Kept ASCII so Windows PowerShell 5.1 reads it without a BOM.
param([Parameter(Mandatory = $true)][string]$Q)

$ErrorActionPreference = "Stop"
Set-Location (Split-Path $PSScriptRoot -Parent)
$proj = Split-Path -Leaf (Get-Location)
$utf8 = New-Object System.Text.UTF8Encoding($false)
. (Join-Path $PSScriptRoot "variant.ps1")
. (Join-Path $PSScriptRoot "check.ps1")

$qbin = @("C:\altera\13.0sp1\quartus\bin64", "C:\altera\13.0sp1\quartus\bin",
          "C:\altera\13.0\quartus\bin64", "C:\altera\13.0\quartus\bin") |
	Where-Object { Test-Path (Join-Path $_ "quartus_sh.exe") } | Select-Object -First 1

function Fail($t) { Write-Host $t -ForegroundColor Red; exit 1 }
function Log($t) {
	[IO.File]::AppendAllText((Join-Path (Get-Location) "results.txt"),
		"[$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')]  $sid  $proj $Q  $t`r`n", $utf8)
}
# The course folder (the one with locked\): the exercise sits one or two levels below it (week3\exN)
function Get-CourseRoot {
	$r = Split-Path (Get-Location) -Parent
	while ($r -and -not (Test-Path (Join-Path $r "locked"))) { $r = Split-Path $r -Parent }
	if ($r) { return $r } else { return (Split-Path (Get-Location) -Parent) }
}
# The board shows "Err" until this answer is right, so it never keeps an older design that looks correct
function Lock-Board {
	$sof = Join-Path (Get-CourseRoot) "locked\locked.sof"
	if (-not $qbin -or -not (Test-Path $sof)) { return }
	$ErrorActionPreference = "Continue"
	& (Join-Path $qbin "quartus_pgm.exe") -c USB-Blaster -m JTAG -o "p;$sof" > lock.log 2>&1
	$ErrorActionPreference = "Stop"
}

# ---------------------------------------------------------------- this student's exercise
$sid = Get-StudentId
try { $null = New-PersonalFiles $sid $proj } catch { Fail "Cannot make your truth table: $($_.Exception.Message)" }
$v = Get-Variant $sid $proj (Join-Path (Get-Location) "tools\base_top.v")
$board = Get-Board (Join-Path (Get-Location) "${proj}_top.v")
$ask = $board.Asks | Where-Object { $_.Id -eq $Q } | Select-Object -First 1
if (-not $ask) { Fail "There is no question $Q in this exercise." }
$names = @($board.Vars) + @($board.Signals.Keys)

Write-Host ""
Write-Host "=== $proj  $($ask.Id) $($ask.Title)          ID $sid ===" -ForegroundColor Cyan
if ($v.Story) {
	Write-Host "  Your story:"; Write-Host "     $($v.Story.En)"
} elseif ($v.Net.Count) {
	Write-Host "  Your circuit (each line is one gate):"; $v.Net | ForEach-Object { Write-Host "     $(Convert-Expr $v $_)" }
} elseif ($v.Expr) {
	Write-Host "  Your expression:   Y = $(Convert-Expr $v $v.Expr)"
} else {
	Write-Host "  Your truth table:"
	Format-Table $v "     " "  " | ForEach-Object { Write-Host $_ }
}
Write-Host ""
Write-Host "  $($ask.Text)" -ForegroundColor White
Write-Host "  Write:  A' (or NOT A)   AB or A*B (or A AND B)   A+B (or A OR B)   (...)' = NOT of the whole group   Q = stop"
if ($ask.Names.Count -gt 1) { Write-Host "  One line each for $($ask.Names -join ', ').  Enter on an empty line = the same as the line above." }
Lock-Board

# ---------------------------------------------------------------- ask until it is right
while ($true) {
	$answers = [ordered]@{}; $typed = [ordered]@{}; $last = ""
	foreach ($n in $ask.Names) {
		while ($true) {
			$t = Read-Host "  $n ="
			if ($null -eq $t) { exit 0 }	# input closed
			$t = $t.Trim()
			if ($t -match '^[Qq]$') { Write-Host "  Stopped."; exit 0 }
			if ($t -eq "" -and $last) { $t = $last; Write-Host "     (same as above: $t)" }
			try { $answers[$n] = ConvertTo-Verilog $t $names; $typed[$n] = $t; $last = $t; break }
			catch { Write-Host "  Cannot read that: $($_.Exception.Message). Type it again." -ForegroundColor Yellow }
		}
	}
	Write-Host ""
	$wrong = Test-Answers $board $answers -Grade
	$said = ($typed.Keys | ForEach-Object { "$_ = $($typed[$_])" }) -join "   "
	if ($wrong -eq 0) {
		$note = if ($script:gradeFail.Count) { "   (no code: " + ($script:gradeFail -join "; ") + ")" } else { "" }
		Log "OK      $said$note"; break
	}
	Log "wrong   $said"
	Write-Host "  Not yet - your answer did NOT go on the board. Look at the rows above, fix it and type it again." -ForegroundColor Red
	Write-Host ""
}

# ---------------------------------------------------------------- the board: your answer + the target
# The outputs this question does not ask for get the canonical SOP of Y, so the alarm LED shows only yours.
$top = [IO.File]::ReadAllText((Join-Path (Get-Location) "${proj}_top.v"))
$null = $top -match 'student_logic\s+\w+\s*\(([^;]*)\);'
$ports = @([regex]::Matches($Matches[1], '\.(\w+)\s*\(') | ForEach-Object { $_.Groups[1].Value })
$inputs = @($ports | Where-Object { $names -contains $_ })
$outs = @($ports | Where-Object { $names -notcontains $_ })
$sl = @("// Written by $($ask.Id).bat from the answer typed in the console - do not edit.", "module student_logic(")
$sl += @($inputs | ForEach-Object { "`tinput  $_," })
$sl += (@($outs | ForEach-Object { "`toutput $_" }) -join ",`r`n")
$sl += "`t);"
$sl += @($outs | ForEach-Object { "`tassign $_ = $(if ($answers.Contains($_)) { $answers[$_] } else { Get-CanonVerilog $board $_ });" })
$sl += "endmodule"
[IO.File]::WriteAllLines((Join-Path (Get-Location) "student_logic.v"), $sl, $utf8)

Write-Host ""
if ($env:DE10_NOBOARD -eq "1") { Write-Host "  (DE10_NOBOARD=1: instructor test run - Quartus and the board are skipped)" -ForegroundColor DarkGray }
else {
Write-Host "=== Quartus puts your answer on the board (about a minute) ===" -ForegroundColor Cyan
if (-not $qbin) { Fail "Quartus II 13.0sp1 not found under C:\altera." }
& (Join-Path $qbin "quartus_sh.exe") --flow compile $proj > compile.log 2>&1
if ($LASTEXITCODE -ne 0) {
	Select-String -Path compile.log -Pattern "^Error" | Select-Object -First 5 | ForEach-Object { Write-Host "  $($_.Line)" }
	Fail "Compile FAILED - details in compile.log"
}
& (Join-Path $qbin "quartus_pgm.exe") -c USB-Blaster -m JTAG -o "p;output_files\$proj.sof" > program.log 2>&1
if ($LASTEXITCODE -ne 0) {
	Select-String -Path program.log -Pattern "Error" | Select-Object -First 3 | ForEach-Object { Write-Host "  $($_.Line)" }
	Fail "Programming FAILED. Is the board on, the USB cable in the BLASTER port, and the switch on RUN?"
}
Write-Host "  Board programmed - move the switches and compare your LED with LEDG0." -ForegroundColor Green
Get-Content "${proj}_top.v" | Where-Object { $_ -match '^//   \S' } | ForEach-Object { Write-Host ("  " + $_.Substring(5)) }
}

# ---------------------------------------------------------------- the code for Moodle
Write-Host ""
if ($script:gradeFail.Count) {
	Write-Host "  Correct, but no code yet - the question asks for more:" -ForegroundColor Yellow
	$script:gradeFail | ForEach-Object { Write-Host "    $_" -ForegroundColor Yellow }
	Write-Host "  Run $($ask.Id) again with a better answer to get the code."
	exit 0
}
$code = Save-MoodleCode $sid $proj "$(Get-ExLabel)-$($ask.Id)"
Write-Host "  Your code for $proj $($ask.Id): $code   - it is saved in moodle.txt, hand that file in on Moodle." -ForegroundColor Green
