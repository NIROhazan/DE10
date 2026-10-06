# Class exercise runner: Q05_MINTERM.bat = run.ps1 -Only Q05.
# Programs sof\Qnn.sof, prints the student's login number and the question. The board holds the puzzle and
# judges the answer (KEY2 shows the code or Err); the student types the code here and it goes to moodle.txt.
# The PC cannot check the answer - only the check digit (typos, wrong login). Kept ASCII for PowerShell 5.1.
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

# ---------------------------------------------------------------- the question
$bin = Get-Bin $s 10
$up = @(9..0 | Where-Object { $s -band (1 -shl $_) } | ForEach-Object { "SW$_" }) -join " "
if (-not $up) { $up = "(none)" }
Write-Host ""
Write-Host "=== Class exercise $($q.Id) - $($q.Title) ===          ID $sid" -ForegroundColor Cyan
Write-Host ""
Write-Host "  1. LOGIN  (HEX3 shows L, HEX2..HEX0 show the switches)" -ForegroundColor Yellow
Write-Host "     Your login number: $s  =  hex $('{0:X3}' -f $s)  =  SW9..SW0 $($bin.Substring(0,2)) $($bin.Substring(2,4)) $($bin.Substring(6,4))"
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
Write-Host "     Hold KEY1: HEX shows L and the login number the board took - it must be $('{0:X3}' -f $s)."
Write-Host ""

while ($true) {
	$ans = Read-Host "  Type the code (HEX3 HEX2 HEX1 HEX0), or Q to stop"
	if ($null -eq $ans) { exit 0 }
	$ans = ($ans -replace '\s', '').ToUpper()
	if ($ans -eq 'Q') { Write-Host "  Stopped. Run $($q.Id) again to continue (you log in again)."; exit 0 }
	if ($ans -notmatch '^[0-9A-F]{4}$') { Write-Host "  4 hex digits (0-9, A-F), as on HEX3..HEX0." -ForegroundColor Yellow; continue }
	if (-not (Test-CodeDigits $ans $s)) {
		Log "code $ans does not fit"
		Write-Host "  This code does not fit. A typo? Or the board took a wrong login number -" -ForegroundColor Red
		Write-Host "  hold KEY1 in ANSWER mode: it must show L $('{0:X3}' -f $s). If not, run $($q.Id) again." -ForegroundColor Red
		continue
	}
	Log "code $ans"
	Save-MoodleCode $sid $q.Id $ans
	Write-Host "  Saved in moodle.txt: ce-$($q.Id): $ans   - hand in moodle.txt on Moodle." -ForegroundColor Green
	break
}
