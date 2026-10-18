# Camera demo loader (week1\Demo\CAMERA_DEMO.bat). Loads sof\d5m_cam.sof onto the board with the D5M camera and
# ..\flicker_tx\sof\flicker_tx.sof onto a second board, if there is one. Which board is which is found out,
# not assumed: the camera design is loaded and asked (over the USB cable) whether the camera answered on I2C.
# A board without a camera cannot answer, so the order of the USB cables does not matter.
#   -Reverse  try the second cable first (to test the case where the first guess is the wrong board)
# ASCII only: Windows PowerShell 5.1 reads a .ps1 without BOM as ANSI.
param([switch]$Reverse)
$ErrorActionPreference = "Continue"          # Quartus tools write notes to stderr; failures are checked by hand
$here = Split-Path $PSScriptRoot -Parent
Set-Location $here
function Step($t) { Write-Host ""; Write-Host "=== $t ===" -ForegroundColor Cyan }
function Fail($t) { Write-Host $t -ForegroundColor Red; exit 1 }

$qbin = @("C:\altera_lite\25.1std\quartus\bin64", "C:\intelFPGA_lite\25.1std\quartus\bin64",
          "C:\intelFPGA_lite\24.1std\quartus\bin64", "C:\intelFPGA_lite\23.1std\quartus\bin64") |
	Where-Object { Test-Path (Join-Path $_ "quartus_pgm.exe") } | Select-Object -First 1
if (-not $qbin) { Fail "Quartus Prime Lite not found (looked in C:\altera_lite and C:\intelFPGA_lite)." }
$cam_sof = Join-Path $here "sof\d5m_cam.sof"
$tx_sof  = Join-Path (Split-Path $here -Parent) "flicker_tx\sof\flicker_tx.sof"
foreach ($f in $cam_sof, $tx_sof) { if (-not (Test-Path $f)) { Fail "Missing $f" } }

# ---- the boards on the USB cables ----
Step "Boards on the USB cables"
$cables = @(& (Join-Path $qbin "jtagconfig.exe") 2>$null | ForEach-Object {
	if ($_ -match '^\s*\d+\)\s+(USB-Blaster.*\])') { $Matches[1] } })
if ($cables.Count -eq 0) { Fail "No board found. Plug the DE10-Lite into USB (and check the USB-Blaster driver)." }
$cables | ForEach-Object { Write-Host "  $_" }
if ($Reverse -and $cables.Count -ge 2) { $cables = @($cables[1], $cables[0]) + @($cables | Select-Object -Skip 2) }

function Load($cable, $sof) {
	# Quartus is unreliable with Hebrew letters or spaces in a path: load a copy from a plain folder
	$plain = Join-Path $env:TEMP ("d5m_demo_" + (Split-Path $sof -Leaf))
	Copy-Item $sof $plain -Force
	$out = & (Join-Path $qbin "quartus_pgm.exe") -c "$cable" -m JTAG -o "p;$plain" 2>&1
	if (($out | Out-String) -notmatch "Programmer was successful") { $out | Select-Object -Last 5 | ForEach-Object { Write-Host $_ }; Fail "Loading $sof onto $cable failed." }
}

# reads the camera design's status over the cable: "ok" = camera configured, "nack" = no camera answered
$tcl = Join-Path $env:TEMP "d5m_demo_probe.tcl"
Set-Content -Path $tcl -Encoding ascii -Value @'
set hw [lindex $quartus(args) 0]
set dev [lindex [get_device_names -hardware_name $hw] 0]
start_insystem_source_probe -device_name $dev -hardware_name $hw
puts "P [read_probe_data -instance_index 0 -value_in_hex]"
end_insystem_source_probe
'@
function Camera-Status($cable) {
	Start-Sleep -Milliseconds 800                      # reset 2.6 ms + 17 register writes over I2C ~20 ms
	$p = & (Join-Path $qbin "quartus_stp.exe") -t $tcl "$cable" 2>$null | Select-String "^P ([0-9A-Fa-f]+)"
	if (-not $p) { return "unknown" }
	$v = [System.Numerics.BigInteger]::Parse("0" + $p.Matches[0].Groups[1].Value, [Globalization.NumberStyles]::AllowHexSpecifier)
	$nack = [int](($v -shr 68) -band 1); $done = [int](($v -shr 69) -band 1)
	if ($done -eq 1 -and $nack -eq 0) { return "ok" } elseif ($nack -eq 1) { return "nack" } else { return "unknown" }
}

# ---- find the camera board ----
$cam = $null
foreach ($c in $cables) {
	Step "Camera design -> $c"
	Load $c $cam_sof
	$s = Camera-Status $c
	if ($s -eq "ok") { Write-Host "  The camera answered: this is the camera board." -ForegroundColor Green; $cam = $c; break }
	Write-Host "  No camera on this board ($s)." -ForegroundColor Yellow
}
if (-not $cam) { Fail "No board answered with a camera. Check that the D5M sits on JP1 (the GPIO header) and press KEY0." }

# ---- the LED flicker board ----
$tx = @($cables | Where-Object { $_ -ne $cam }) | Select-Object -First 1
if ($tx) {
	Step "Flicker transmitter -> $tx"
	Load $tx $tx_sof
	Write-Host "  Loaded." -ForegroundColor Green
}

Step "Ready"
Write-Host "  Camera board ($cam):"
Write-Host "    all switches down     = camera picture (SW9..SW7 = exposure; KEY1 = white balance on white paper)"
Write-Host "    SW5 up                = event camera (KEY1 = sensitivity)"
Write-Host "    SW6 up                = flicker meter: Hz on HEX and on screen (KEY1 = exposure, SW5 = fast smoothing)"
if ($tx) {
	Write-Host "  LED board ($tx):"
	Write-Host "    SW9..SW0              = flicker frequency in Hz, binary (100 Hz = SW6 + SW5 + SW2)"
	Write-Host "    KEY0 held             = steady light (the meter should go to 0)"
	Write-Host "  Put a sheet of white paper 1-2 cm over the LED board, the camera 10 cm from it, room light off."
} else {
	Write-Host "  Only one board: the flicker meter can measure a room LED lamp (100 Hz on 50 Hz mains)."
}
Write-Host "  Both designs are lost when a board loses power: run week1\Demo\CAMERA_DEMO.bat again after unplugging."
