# One written question of the exercise: Q5_TEXT1.bat = text.ps1 -Q Q5.
# The questions are the "// TEXT Qn k:" lines of tools/base_top.v (k = the question number in answer.txt).
# The console shows the question in English (it cannot show Hebrew); Notepad opens for the answer, with the
# Hebrew question on top. Claude judges the answer (tools/judge.md) and writes verdict.txt; OK gives the code.
# Kept ASCII so Windows PowerShell 5.1 reads it without a BOM.
param([Parameter(Mandatory = $true)][string]$Q)

$ErrorActionPreference = "Stop"
Set-Location (Split-Path $PSScriptRoot -Parent)
$proj = Split-Path -Leaf (Get-Location)
$utf8 = New-Object System.Text.UTF8Encoding($false)
. (Join-Path $PSScriptRoot "variant.ps1")

function Fail($t) { Write-Host $t -ForegroundColor Red; exit 1 }
function Log($t) {
	[IO.File]::AppendAllText((Join-Path (Get-Location) "results.txt"),
		"[$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')]  $sid  $proj $Q  $t`r`n", $utf8)
}

$sid = Get-StudentId
try { $null = New-PersonalFiles $sid $proj } catch { Fail "Cannot make your truth table: $($_.Exception.Message)" }
$v = Get-Variant $sid $proj (Join-Path (Get-Location) "tools\base_top.v")
$m = [regex]::Match($v.Text, "(?m)^//\s*TEXT\s+$Q\s+(\d+):\s*(.+?)\s*$")
if (-not $m.Success) { Fail "There is no written question $Q in this exercise." }
$k = $m.Groups[1].Value
$english = Convert-Text $v $m.Groups[2].Value
# The Hebrew question as it is in this student's answer.txt (rows already theirs)
$hebrew = @([IO.File]::ReadAllLines((Join-Path (Get-Location) "answer.txt"), $utf8) | Where-Object { $_ -match "^#\s*ש$k\." }) | Select-Object -First 1
if (-not $hebrew) { $hebrew = "" }

Write-Host ""
Write-Host "=== $proj  $Q  written question $k          ID $sid ===" -ForegroundColor Cyan
if ($v.Story) { Write-Host "  Your story:"; Write-Host "     $($v.Story.En)" }
elseif ($v.Net.Count) { Write-Host "  Your circuit:"; $v.Net | ForEach-Object { Write-Host "     $(Convert-Expr $v $_)" } }
elseif ($v.Expr) { Write-Host "  Your expression:   Y = $(Convert-Expr $v $v.Expr)" }
else { Write-Host "  Your truth table:"; Format-Table $v "     " "  " | ForEach-Object { Write-Host $_ } }
Write-Host ""
Write-Host "  $english" -ForegroundColor White
Write-Host ""
Write-Host "  Notepad opens now: write your answer under the question (Hebrew or English),"
Write-Host "  then SAVE and CLOSE Notepad. Claude checks it - about half a minute."

# The answer file keeps the last answer, so a second try starts from it
$dir = Join-Path (Get-Location) "answers"
$null = New-Item -ItemType Directory -Force $dir
$file = Join-Path $dir "$Q.txt"
if (-not (Test-Path $file)) {
	[IO.File]::WriteAllLines($file, @($hebrew, "# $english", "# Write your answer below these lines, save, and close Notepad.", ""), $utf8)
}
# DE10_TEXTANSWER (instructor test runs) is the answer instead of Notepad
if ($env:DE10_TEXTANSWER) { [IO.File]::AppendAllText($file, $env:DE10_TEXTANSWER + "`r`n", $utf8) }
else { Start-Process notepad.exe $file -Wait }
$answer = (@([IO.File]::ReadAllLines($file, $utf8) | Where-Object { $_ -notmatch '^\s*#' -and $_.Trim() }) -join "`r`n").Trim()
if (-not $answer) { Fail "  No answer was written - nothing was checked. Run $Q again." }

$claude = (Get-Command claude -ErrorAction SilentlyContinue).Source
if (-not $claude) {
	$c = Join-Path $env:USERPROFILE ".local\bin\claude.exe"
	if (Test-Path $c) { $claude = $c }
}
if (-not $claude) { Fail "Claude Code is not installed on this computer (claude.exe not found)." }

[IO.File]::WriteAllText((Join-Path (Get-Location) "judge_input.txt"),
	"Exercise $proj, written question $k`r`n`r`nThe question (Hebrew): $hebrew`r`nThe question (English): $english`r`n`r`nThe student's answer:`r`n$answer`r`n", $utf8)
if (Test-Path "verdict.txt") { Remove-Item "verdict.txt" }
Write-Host "  Claude is reading your answer..."
$ErrorActionPreference = "Continue"
"" | & $claude -p "Follow the instructions in tools/judge.md exactly." `
	--restricted --strict-mcp-config --tools "Read,Write" --permission-mode acceptEdits > claude.log 2>&1
$ErrorActionPreference = "Stop"
if ($LASTEXITCODE -ne 0 -or -not (Test-Path "verdict.txt")) {
	Get-Content claude.log -ErrorAction SilentlyContinue | Select-Object -Last 5
	Fail "Claude could not check the answer. Is it logged in? Open a command prompt, run  claude  once and log in."
}
$verdict = ([IO.File]::ReadAllLines((Join-Path (Get-Location) "verdict.txt"), $utf8) | Select-Object -First 1).Trim().ToUpper()
Copy-Item "verdict.txt" (Join-Path $dir "$Q.feedback.txt") -Force
if (-not $env:DE10_TEXTANSWER) { Start-Process notepad.exe (Join-Path $dir "$Q.feedback.txt") }
Log "$verdict   $($answer -replace '\s+', ' ')"

Write-Host ""
if ($verdict -eq "OK") {
	$code = Save-MoodleCode $sid $proj "$proj-$Q"
	Write-Host "  Correct!  Your code for $proj ${Q}: $code   - saved in moodle.txt (hand it in on Moodle)." -ForegroundColor Green
} elseif ($verdict -eq "PARTIAL") {
	Write-Host "  Partly right - read the feedback (it opened in Notepad), improve the answer, and run $Q again." -ForegroundColor Yellow
} else {
	Write-Host "  Not right yet - read the feedback (it opened in Notepad), fix the answer, and run $Q again." -ForegroundColor Red
}
