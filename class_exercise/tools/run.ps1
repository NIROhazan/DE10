# Class exercise runner: Q01_GATE.bat = run.ps1 -Only Q01.
# Programs sof\Qnn.sof and talks to the board over the USB cable (tools\link.tcl in quartus_stp): it writes the
# student's login number and the step to start from into the board, and reads the board's step and code.
# So the student only flips switches and presses KEY2; the screen moves on by itself, and the code at the end
# goes into moodle.txt by itself. The board alone knows the answers and the codes.
# progress.txt keeps the last step passed: a closed window goes on from there, never from the start.
# Kept ASCII so Windows PowerShell 5.1 reads it without a BOM.
param([Parameter(Mandatory = $true)][string]$Only)

$ErrorActionPreference = "Stop"
Set-Location (Split-Path $PSScriptRoot -Parent)
. (Join-Path $PSScriptRoot "common.ps1")

$qs = Read-Questions
if (-not $qs.Contains($Only)) { Write-Host "There is no $Only in tools\questions.txt." -ForegroundColor Red; exit 1 }
$q = $qs[$Only]
$sid = Get-StudentId
$s = Get-Login $sid
$pub = Get-Pub $q.Id $s $q.NPub
$last = $q.NS - 1

$done = Get-Progress $sid $q.Id
if ($done -ge $last) {
	Write-Host ""
	Write-Host "  $($q.Id) is already done. Your code is in moodle.txt:  ce-$($q.Id): $(Get-SavedCode $q.Id)" -ForegroundColor Green
	exit 0
}
$from = $done + 1

# ---------------------------------------------------------------- program the board
$qbin = @("C:\altera\13.0sp1\quartus\bin64", "C:\altera\13.0sp1\quartus\bin") |
	Where-Object { Test-Path (Join-Path $_ "quartus_pgm.exe") } | Select-Object -First 1
$sof = Join-Path (Get-Location) "sof\$($q.Id).sof"
if (-not $qbin) { Write-Host "  Quartus II 13.0sp1 not found under C:\altera." -ForegroundColor Red; exit 1 }
Get-Process quartus_stp -ErrorAction SilentlyContinue | Stop-Process -Force		# an old link from a closed window
Write-Host ""
Write-Host "  Preparing the board..."
$ErrorActionPreference = "Continue"
& (Join-Path $qbin "quartus_pgm.exe") -c USB-Blaster -m JTAG -o "p;$sof" > program.log 2>&1
if ($LASTEXITCODE -ne 0) {		# jtagd may still be starting: once more
	& (Join-Path $qbin "jtagconfig.exe") > $null 2>&1
	& (Join-Path $qbin "quartus_pgm.exe") -c USB-Blaster -m JTAG -o "p;$sof" > program.log 2>&1
}
$okPgm = ($LASTEXITCODE -eq 0)
$ErrorActionPreference = "Stop"
if (-not $okPgm) {
	Write-Host "  The board did not answer. Is it on, the USB cable in the BLASTER port, the switch on RUN?" -ForegroundColor Red
	exit 1
}

# ---------------------------------------------------------------- the link: login + start step in, step + code out
$srcHex = '{0:X4}' -f ((1 -shl 13) -bor ($from -shl 10) -bor $s)
$psi = New-Object System.Diagnostics.ProcessStartInfo
$psi.FileName = Join-Path $qbin "quartus_stp.exe"
$psi.Arguments = "-t `"$(Join-Path $PSScriptRoot 'link.tcl')`" $srcHex"
$psi.UseShellExecute = $false
$psi.RedirectStandardOutput = $true
$psi.RedirectStandardInput = $true		# the link must not share the console input
$psi.CreateNoWindow = $true
$link = [System.Diagnostics.Process]::Start($psi)

function Show-Step($k) {
	Clear-Host
	Write-Host ""
	Write-Host "  $($q.Id) - $($q.Title)          step $k of $last" -ForegroundColor Cyan
	Write-Host ""
	$q.B | ForEach-Object { Write-Host "  $_" -ForegroundColor DarkGray }
	if ($q.P.ContainsKey($pub)) { $q.P[$pub] | ForEach-Object { Write-Host "  $_" } }
	Write-Host ""
	$q.S[$k] | ForEach-Object { if ($_ -match '^(GOAL|ANSWER)') { Write-Host "  $_" -ForegroundColor Yellow } else { Write-Host "  $_" } }
	Write-Host ""
	Write-Host "  Put the answer on the switches and press KEY2." -ForegroundColor Green
	Write-Host "  The board shows PASS (this screen moves on by itself) or Err (try again)." -ForegroundColor DarkGray
}

try {
	$cur = 0
	while ($true) {
		$line = $link.StandardOutput.ReadLine()
		if ($null -eq $line -or $line -eq "X") {
			Write-Host ""
			Write-Host "  The link to the board stopped (USB cable? board off?). Run $($q.Id) again - your progress is saved." -ForegroundColor Red
			exit 1
		}
		if ($line -notmatch '^P\s+([0-9A-Fa-f]+)') { continue }
		$v = [Convert]::ToInt32($Matches[1], 16)
		$fin = ($v -shr 19) -band 1
		$step = ($v -shr 16) -band 7
		if ($cur -eq 0) {
			if ($step -lt $from) { continue }		# the board is still starting
			$cur = $step; Show-Step $cur; continue
		}
		while ($cur -lt $step) {			# a step passed on the board
			Save-Progress $sid $q.Id $cur
			Write-Host ""
			Write-Host "  PASS - well done!" -ForegroundColor Green
			Start-Sleep -Milliseconds 1500
			$cur++
			Show-Step $cur
		}
		if ($fin) {
			$code = '{0:X4}' -f ($v -band 0xFFFF)
			Save-Progress $sid $q.Id $last
			Save-MoodleCode $sid $q.Id $code
			Write-Host ""
			Write-Host "  PASS - $($q.Id) is done!  Your code ce-$($q.Id): $code is saved in moodle.txt." -ForegroundColor Green
			break
		}
	}
} finally {
	if (-not $link.HasExited) { $link.Kill() }
}
