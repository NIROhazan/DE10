# Class exercise runner: Q05_MINTERM.bat = run.ps1 -Only Q05.
# Programs sof\Qnn.sof. The board holds the puzzle and judges every answer (KEY2 shows the code or Err);
# the student types the code here. The PC cannot check the answer - only the check digit (typos, wrong login,
# a code of another step).
# Questions with steps (questions.txt "| steps n"): one short screen per step, PASS / FAIL after every code,
# the next screen only after a PASS. Step 0 = the login (the board shows a receipt).
# Questions without steps: the whole question on one screen, one code.
# Kept ASCII so Windows PowerShell 5.1 reads it without a BOM.
param([Parameter(Mandatory = $true)][string]$Only)

$ErrorActionPreference = "Stop"
Set-Location (Split-Path $PSScriptRoot -Parent)
. (Join-Path $PSScriptRoot "common.ps1")

function Log($t) {
	[IO.File]::AppendAllText((Join-Path (Get-Location) "results.txt"),
		"[$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')]  $sid  $Only $t`r`n", $script:utf8)
}

$qs = Read-Questions
if (-not $qs.Contains($Only)) { Write-Host "There is no $Only in tools\questions.txt." -ForegroundColor Red; exit 1 }
$q = $qs[$Only]
$sid = Get-StudentId
$s = Get-Login $sid
$pub = Get-Pub $q.Id $s $q.NPub
$hex = '{0:X3}' -f $s
$bin = Get-Bin $s 10
$up = @(9..0 | Where-Object { $s -band (1 -shl $_) } | ForEach-Object { "SW$_" }) -join " "
if (-not $up) { $up = "(none)" }

# ---------------------------------------------------------------- the board
$qbin = @("C:\altera\13.0sp1\quartus\bin64", "C:\altera\13.0sp1\quartus\bin",
          "C:\altera\13.0\quartus\bin64", "C:\altera\13.0\quartus\bin") |
	Where-Object { Test-Path (Join-Path $_ "quartus_pgm.exe") } | Select-Object -First 1
$sof = Join-Path (Get-Location) "sof\$($q.Id).sof"
if (-not $qbin) { Write-Host "  Quartus II 13.0sp1 not found under C:\altera." -ForegroundColor Red; exit 1 }
if (-not (Test-Path $sof)) { Write-Host "  sof\$($q.Id).sof is missing." -ForegroundColor Red; exit 1 }
Write-Host ""
Write-Host "  Programming the board with $($q.Id)..."
$ErrorActionPreference = "Continue"
& (Join-Path $qbin "quartus_pgm.exe") -c USB-Blaster -m JTAG -o "p;$sof" > program.log 2>&1
if ($LASTEXITCODE -ne 0) {		# jtagd may still be starting: once more
	& (Join-Path $qbin "jtagconfig.exe") > $null 2>&1
	& (Join-Path $qbin "quartus_pgm.exe") -c USB-Blaster -m JTAG -o "p;$sof" > program.log 2>&1
}
$okPgm = ($LASTEXITCODE -eq 0)
$ErrorActionPreference = "Stop"
if (-not $okPgm) {
	Write-Host "  Programming FAILED. Is the board on, the USB cable in the BLASTER port, the switch on RUN?" -ForegroundColor Red
	Write-Host "  This question lives only in the board - it cannot be solved without it." -ForegroundColor Red
	exit 1
}

# Reads a code until it fits; $step = $null for a question without steps. Returns the code, or exits on Q.
function Read-Code($step, $failLines) {
	while ($true) {
		$ans = Read-Host "  Code"
		if ($null -eq $ans) { exit 0 }
		$ans = ($ans -replace '\s', '').ToUpper()
		if ($ans -eq 'Q') { Write-Host "  Stopped. Run $($q.Id) again to start over (you log in again)."; exit 0 }
		if ($ans -notmatch '^[0-9A-F]{4}$') { Write-Host "  4 digits (0-9, A-F), as on HEX3 HEX2 HEX1 HEX0." -ForegroundColor Yellow; continue }
		$fits = if ($null -eq $step) { Test-CodeDigits $ans $s } else { Test-CodeDigits $ans $s $step }
		if ($fits) { Log "step $step code $ans PASS"; return $ans }
		Log "step $step code $ans FAIL"
		Write-Host ""
		Write-Host "  FAIL" -ForegroundColor Red
		$failLines | ForEach-Object { Write-Host "  $_" -ForegroundColor Red }
		Write-Host ""
	}
}

# ================================================================ with steps: one short screen per step
if ($q.NS -gt 0) {
	$last = $q.NS - 1
	function Show-Top($k) {
		Clear-Host
		Write-Host ""
		Write-Host "  $($q.Id) - $($q.Title)" -ForegroundColor Cyan
		Write-Host "  Step $k of $last" -ForegroundColor Cyan
		Write-Host ""
		if ($k -gt 0) {
			$q.B | ForEach-Object { Write-Host "  $_" -ForegroundColor DarkGray }
			if ($q.P.ContainsKey($pub)) { $q.P[$pub] | ForEach-Object { Write-Host "  $_" } }
			Write-Host ""
		}
	}

	# step 0: the login - the board shows a receipt that only the right login number gives
	Show-Top 0
	Write-Host "  LOG IN - the board builds YOUR puzzle from your login number." -ForegroundColor Yellow
	Write-Host ""
	Write-Host "  Switches UP: $up   (all the others down; HEX shows L $hex)"
	Write-Host "  Press KEY3. The board shows 4 digits - type them."
	Write-Host ""
	$null = Read-Code 0 @("That is not your receipt. Hold KEY1: if HEX does not show the 4 digits again,",
	                      "close this window, run $($q.Id) again and raise exactly: $up")
	Write-Host "  PASS - you are logged in." -ForegroundColor Green
	$null = Read-Host "  Enter = next step"

	for ($k = 1; $k -le $last; $k++) {
		Show-Top $k
		$q.S[$k] | ForEach-Object { Write-Host "  $_" -ForegroundColor Yellow }
		Write-Host ""
		Write-Host "  Answer: KEY3 (LEDG7 on, LEDG2..0 = $k) - set the switches - HOLD KEY2 - type the 4 digits." -ForegroundColor DarkGray
		Write-Host "  Err = not right yet, change the switches.  KEY3 again = back to the lights." -ForegroundColor DarkGray
		Write-Host ""
		$code = Read-Code $k @("That is not the code of step $k. LEDG2..0 must show $k in answer mode.",
		                       "Hold KEY1 to see the last code the board gave, and check for a typo.")
		if ($k -lt $last) {
			Write-Host "  PASS" -ForegroundColor Green
			$null = Read-Host "  Enter = next step"
		} else {
			Save-MoodleCode $sid $q.Id $code
			Write-Host "  PASS - $($q.Id) is done. Saved in moodle.txt: ce-$($q.Id): $code" -ForegroundColor Green
		}
	}
	exit 0
}

# ================================================================ without steps: the whole question at once
Write-Host ""
Write-Host "=== Class exercise $($q.Id) - $($q.Title) ===          ID $sid" -ForegroundColor Cyan
Write-Host ""
Write-Host "  1. LOGIN  (HEX3 shows L, HEX2..HEX0 show the switches)" -ForegroundColor Yellow
Write-Host "     Your login number: $s  =  hex $hex  =  SW9..SW0 $($bin.Substring(0,2)) $($bin.Substring(2,4)) $($bin.Substring(6,4))"
Write-Host "     Switches UP: $up.   Then press KEY3."
Write-Host ""
Write-Host "  2. PLAY  - find the answer on the board" -ForegroundColor Yellow
$q.B | ForEach-Object { Write-Host "     $_" }
Write-Host ""
$q.L | ForEach-Object { Write-Host "     $_" }
if ($q.P.ContainsKey($pub)) { $q.P[$pub] | ForEach-Object { Write-Host "     $_" -ForegroundColor White } }
Write-Host ""
Write-Host "  3. ANSWER  - press KEY3 (LEDG7 lights; KEY3 again = back to PLAY)" -ForegroundColor Yellow
$q.F | ForEach-Object { Write-Host "     $_" }
Write-Host "     Other switches do not matter. HEX shows A and your switches in hex."
Write-Host "     Hold KEY2: HEX3..HEX0 show your CODE if the answer is right, Err if not."
Write-Host "     Hold KEY1: HEX shows L and the login number the board took - it must be $hex."
Write-Host ""
$code = Read-Code $null @("This code does not fit. A typo? Or the board took a wrong login number -",
                          "hold KEY1 in ANSWER mode: it must show L $hex. If not, run $($q.Id) again.")
Save-MoodleCode $sid $q.Id $code
Write-Host "  Saved in moodle.txt: ce-$($q.Id): $code   - hand in moodle.txt on Moodle." -ForegroundColor Green
