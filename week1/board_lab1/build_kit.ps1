# Builds every .sof that ../lab1_kit needs and copies them into ../lab1_kit/sof:
#   lab1.sof              the full board: warm-up, then SW9..SW7 pick the card (also flashed as .pof)
#   card1..6.sof, card8   the same design with one card fixed (parameter CARD) and no warm-up
#   game.sof, speeddial.sof
# The card variants compile in a temp copy, so the lab1 project here keeps its default.
#   pwsh -File build_kit.ps1              (takes ~15 min)
#   pwsh -File build_kit.ps1 -CardsOnly   (only the card variants)
param([switch]$CardsOnly)
$ErrorActionPreference = "Stop"
$qsh = @("C:\altera_lite\25.1std\quartus\bin64", "C:\altera_standard\25.1std\quartus\bin64", "C:\intelFPGA_lite\25.1std\quartus\bin64") |
	ForEach-Object { Join-Path $_ "quartus_sh.exe" } | Where-Object { Test-Path $_ } | Select-Object -First 1
$here = $PSScriptRoot
$out  = Join-Path $here "..\lab1_kit\sof"
New-Item -ItemType Directory -Force $out | Out-Null

function Build([string]$dir, [string]$proj, [string]$sofName) {
	Push-Location $dir
	try {
		& $qsh --flow compile $proj > "build.log" 2>&1
		if ($LASTEXITCODE -ne 0) { throw "$sofName failed, see $dir\build.log" }
		Copy-Item "output_files\$proj.sof" (Join-Path $out "$sofName.sof") -Force
		Write-Host "ok  $sofName.sof"
	} finally { Pop-Location }
}

if (-not $CardsOnly) {
	Build (Join-Path $here "lab1") "lab1" "lab1"
	Build (Join-Path $here "game") "game" "game"
	Build (Join-Path $here "speeddial") "speeddial" "speeddial"
}

# card number on the kit -> CARD (the SW9..SW7 code): cards 1-6 are 0-5, card 8 is 7 (card 7 is speeddial)
$cards = [ordered]@{ card1 = 0; card2 = 1; card3 = 2; card4 = 3; card5 = 4; card6 = 5; card8 = 7 }
$tmp = Join-Path $env:TEMP "lab1_cards"
foreach ($c in $cards.Keys) {
	$d = Join-Path $tmp $c
	Remove-Item -Recurse -Force $d -ErrorAction SilentlyContinue
	New-Item -ItemType Directory -Force $d | Out-Null
	Copy-Item (Join-Path $here "lab1\lab1_top.sv"), (Join-Path $here "lab1\lab1.qpf"),
	          (Join-Path $here "lab1\lab1.qsf"), (Join-Path $here "lab1\lab1.sdc") $d
	# leading newline: Quartus saves the .qsf without a final one, and the line would join the last line
	Add-Content (Join-Path $d "lab1.qsf") "`r`nset_parameter -name CARD $($cards[$c])"
	Build $d "lab1" $c
}
