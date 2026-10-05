# Board helpers shared by run.ps1 and free.ps1 (dot-source after eq.ps1).
# Get-Sof "A + B*C" returns the .sof for that equation: sof/<hash>.sof, compiled once and then reused.
# Kept ASCII so Windows PowerShell 5.1 reads it without a BOM.

$script:qbin = @("C:\altera\13.0sp1\quartus\bin64", "C:\altera\13.0sp1\quartus\bin",
                 "C:\altera\13.0\quartus\bin64", "C:\altera\13.0\quartus\bin") |
	Where-Object { Test-Path (Join-Path $_ "quartus_sh.exe") } | Select-Object -First 1

function Get-Sof($text) {
	$ver, $null = Read-Equation $text
	$md5 = [Security.Cryptography.MD5]::Create().ComputeHash([Text.Encoding]::ASCII.GetBytes($ver))
	$key = (($md5[0..4] | ForEach-Object { $_.ToString("x2") }) -join "")
	$sof = Join-Path (Get-Location) "sof\$key.sof"
	if (Test-Path $sof) { return $sof }

	if (-not $script:qbin) { throw "Quartus II 13.0sp1 not found under C:\altera." }
	Write-Host "  First time for Y = $text - compiling (about a minute)..."
	$v = @(
		"// Written by run.bat - do not edit.",
		"//   Y = $text",
		"module equation(",
		"	input  [3:0] A,",
		"	input  [3:0] B,",
		"	input  [3:0] C,",
		"	output [3:0] Y",
		"	);",
		"	assign Y = $ver;",
		"endmodule"
	)
	[IO.File]::WriteAllLines((Join-Path (Get-Location) "equation.v"), $v, (New-Object System.Text.UTF8Encoding($false)))
	& (Join-Path $script:qbin "quartus_sh.exe") --flow compile ex0_eq > compile.log 2>&1
	if ($LASTEXITCODE -ne 0) { throw "Compile FAILED - details in compile.log" }
	$null = New-Item -ItemType Directory -Force "sof"
	Copy-Item "output_files\ex0_eq.sof" $sof
	return $sof
}

function Send-Sof($sof) {
	if (-not $script:qbin) { throw "Quartus II 13.0sp1 not found under C:\altera." }
	& (Join-Path $script:qbin "quartus_pgm.exe") -c USB-Blaster -m JTAG -o "p;$sof" > program.log 2>&1
	if ($LASTEXITCODE -ne 0) {
		throw "Programming FAILED. Is the board on, the USB cable in the BLASTER port, and the switch on RUN?"
	}
}
