# Lab 1 runner (LAB1.bat). Shows tools\steps.txt one step at a time, programs the board with the step's design
# (sof\<design>.sof over the USB cable, on entering every step: forward, back or jump) and saves the student's answers to answers_<ID>.txt.
# ASCII only: Windows PowerShell 5.1 reads a .ps1 without BOM as ANSI; the Hebrew lives in steps.txt and ui.txt.
$utf8 = New-Object System.Text.UTF8Encoding($false)
try { [Console]::OutputEncoding = $utf8; [Console]::InputEncoding = $utf8 } catch { }
$kit = Split-Path $PSScriptRoot -Parent
Set-Location $kit

# ---- Hebrew in the console (same as week5 class_exercise/tools/common.ps1): the console writes left to right,
# so a Hebrew line is turned into visual order and aligned right. Lines without Hebrew are written as they are.
function ConvertTo-Visual([string]$s) {
	# "-64" stays one piece, so the minus stays on the left of its number after the line is turned
	$tok = [regex]::Matches($s, "(?<![A-Za-z0-9])-[0-9][0-9.]*|[A-Za-z0-9][A-Za-z0-9_.+'=/:-]*|.")
	$out = New-Object System.Text.StringBuilder
	for ($i = $tok.Count - 1; $i -ge 0; $i--) {
		$t = $tok[$i].Value
		switch ($t) { '(' { $t = ')' } ')' { $t = '(' } '[' { $t = ']' } ']' { $t = '[' } '<' { $t = '>' } '>' { $t = '<' } }
		[void]$out.Append($t)
	}
	return $out.ToString()
}
function Write-Line([string]$s, [string]$color = "Gray") {
	if ($s -match '[\u0590-\u05FF]') {
		$w = 100
		try { $w = [Math]::Max(60, $Host.UI.RawUI.WindowSize.Width - 2) } catch { }
		$v = (ConvertTo-Visual $s.Trim())
		Write-Host ($v.PadLeft([Math]::Max($v.Length, $w))) -ForegroundColor $color
	} else {
		Write-Host "  $s" -ForegroundColor $color
	}
}

$UI = @{}
foreach ($l in [IO.File]::ReadAllLines((Join-Path $PSScriptRoot "ui.txt"), $utf8)) {
	if ($l -match '^\s*([A-Za-z_]+)\s*=\s?(.*)$') { $UI[$Matches[1]] = $Matches[2] }
}
function U([string]$k) { if ($UI.ContainsKey($k)) { return $UI[$k] } else { return $k } }

# ---- answers are typed in a small window, not the console: the console can only type left to right, so Hebrew
# came out backwards. The text box is right to left. LAB1_TEST=1 reads from stdin instead (for testing).
Add-Type -AssemblyName System.Windows.Forms, System.Drawing
function Read-Answer([string]$question) {
	if ($env:LAB1_TEST) { return (Read-Host) }
	$f = New-Object Windows.Forms.Form
	$f.Text = "Lab 1"
	$f.RightToLeft = 'Yes'; $f.RightToLeftLayout = $true
	$f.Width = 760; $f.Height = 300; $f.StartPosition = 'CenterScreen'; $f.TopMost = $true
	$f.Font = New-Object Drawing.Font('Segoe UI', 13)
	$t = New-Object Windows.Forms.TextBox
	$t.Multiline = $true; $t.Dock = 'Fill'; $t.RightToLeft = 'Yes'; $t.ScrollBars = 'Vertical'; $t.WordWrap = $true
	$l = New-Object Windows.Forms.Label
	$l.Text = $question; $l.Dock = 'Top'; $l.Height = 70; $l.Padding = New-Object Windows.Forms.Padding(8)
	$b = New-Object Windows.Forms.Button
	$b.Text = (U "save_btn"); $b.Dock = 'Bottom'; $b.Height = 45; $b.DialogResult = 'OK'
	$f.AcceptButton = $b                     # Enter saves (the box does not take Enter as a new line)
	$f.Controls.Add($t); $f.Controls.Add($l); $f.Controls.Add($b)
	$f.Add_Shown({ $f.Activate(); $t.Focus() })
	[void]$f.ShowDialog()
	$a = $t.Text.Trim()
	$f.Dispose()
	return $a
}

# ---- steps.txt: "== id | design | title", then > shown, ! shown as is, ? asked, @ math
$steps = New-Object System.Collections.ArrayList
$cur = $null
foreach ($l in [IO.File]::ReadAllLines((Join-Path $PSScriptRoot "steps.txt"), $utf8)) {
	if ($l -match '^==\s*(\S+)\s*\|\s*(\S+)\s*\|\s*(.*)$') {
		$cur = [pscustomobject]@{ Id = $Matches[1]; Design = $Matches[2]; Title = $Matches[3].Trim(); Lines = (New-Object System.Collections.ArrayList) }
		[void]$steps.Add($cur)
	} elseif ($cur -and $l -match '^([>!?@])\s?(.*)$') {
		[void]$cur.Lines.Add(@($Matches[1], $Matches[2]))
	}
}

# ---- the board
$qbin = @("C:\altera_lite\25.1std\quartus\bin64", "C:\altera_standard\25.1std\quartus\bin64", "C:\intelFPGA_lite\25.1std\quartus\bin64",
          "C:\intelFPGA_lite\24.1std\quartus\bin64", "C:\intelFPGA_lite\23.1std\quartus\bin64") |
	Where-Object { Test-Path (Join-Path $_ "quartus_pgm.exe") } | Select-Object -First 1

function Set-Board([string]$design) {
	if (-not $qbin) { Write-Line (U "no_quartus") Red; return $false }
	$sof = Join-Path $kit "sof\$design.sof"
	if (-not (Test-Path $sof)) { Write-Line (U "no_sof") Red; Write-Host "  $sof" -ForegroundColor Red; return $false }
	while ($true) {
		Write-Line (U "programming") Yellow
		# empty stdin: quartus_pgm would otherwise read (and swallow) what the students type next
		$null | & (Join-Path $qbin "quartus_pgm.exe") -c USB-Blaster -m JTAG -o "p;$sof" > (Join-Path $kit "program.log") 2>&1
		if ($LASTEXITCODE -eq 0) { Write-Line (U "programmed") Green; return $true }
		Write-Line (U "program_failed") Red
		if ((Read-Host) -eq 's') { return $false }
	}
}

# ---- the lesson: one student per PC, one answers file per student ID
Clear-Host
do {
	Write-Line (U "id") Cyan
	$sid = (Read-Host).Trim()
} until ($sid -match '^\d{5,10}$')
# progress_<ID>.txt keeps the step the student is on (saved on entering every step), so leaving the lab
# (q, or closing the window) and starting LAB1.bat again with the same ID goes back to that step
$progress = Join-Path $kit "progress_$sid.txt"
$i = 0
$name = ""
if (Test-Path $progress) {
	foreach ($l in [IO.File]::ReadAllLines($progress, $utf8)) {
		if ($l -match '^step=(\d+)$') { $i = [Math]::Min($steps.Count - 1, [int]$Matches[1]) }
		elseif ($l -match '^name=(.*)$') { $name = $Matches[1] }
	}
}
if (-not $name) {
	Write-Line (U "name") Cyan
	$name = Read-Answer (U "name")
}
function Save-Progress { [IO.File]::WriteAllText($progress, "step=$i`r`nname=$name`r`n", $utf8) }
$answers = Join-Path $kit "answers_$sid.txt"
$resumed = if ($i -gt 0) { "   (resume, step $($i + 1))" } else { "" }
[IO.File]::AppendAllText($answers, "`r`n=== $sid   $name   $(Get-Date -Format 'yyyy-MM-dd HH:mm')$resumed`r`n", $utf8)
if ($i -gt 0) {
	Write-Host ""
	Write-Line ("{0} {1}" -f (U "resume"), ($i + 1)) Green
	Write-Line (U "resume_enter") DarkGray
	[void](Read-Host)
}

$redo = $false                               # r: the step starts again (board reprogrammed, questions asked again)
while ($i -lt $steps.Count) {
	$s = $steps[$i]
	Save-Progress
	Clear-Host
	Write-Line ("{0} {1}/{2}:  {3}" -f (U "step"), ($i + 1), $steps.Count, $s.Title) Cyan
	Write-Host ""
	# every step programs its own design on entry, forward, back or jump: the board is always that step
	if ($s.Design -ne '-') {
		if ((Set-Board $s.Design) -and $s.Design -eq 'lab1' -and $s.Id -ne 'warmup') { Write-Line (U "leave_warmup") Yellow }
		Write-Host ""
	}
	foreach ($ln in $s.Lines) {
		switch ($ln[0]) {
			'>' { Write-Line $ln[1] White }
			'!' { Write-Host "  $($ln[1])" -ForegroundColor Green }
			'@' {
				Write-Host ""
				Write-Host ("  0.1 + 0.2 == 0.3     ->  {0}" -f ((0.1 + 0.2) -eq 0.3)) -ForegroundColor Green
				Write-Host ("  0.5 + 0.25 == 0.75   ->  {0}" -f ((0.5 + 0.25) -eq 0.75)) -ForegroundColor Green
				Write-Host ("  0.1 + 0.2            =   {0}" -f (0.1 + 0.2).ToString("R")) -ForegroundColor Green
				Write-Host ""
			}
			'?' {
				Write-Host ""
				Write-Line $ln[1] Cyan
				Write-Line (U "answer") DarkGray
				$a = Read-Answer $ln[1]
				Write-Line $a Yellow                 # echoed in visual order, so it reads right in the console too
				$tag = if ($redo) { "[$($s.Id) redo]" } else { "[$($s.Id)]" }   # a redo replaces the answers above it
				[IO.File]::AppendAllText($answers, "$tag $($ln[1])`r`n    $a`r`n", $utf8)
			}
		}
	}
	Write-Host ""
	Write-Line (U "nav") DarkGray
	$c = Read-Host
	$redo = ($c -eq 'r')
	if ($c -eq 'q') { break }
	elseif ($c -eq 'r') { }                  # same step again, from the top
	elseif ($c -eq 'b') { $i = [Math]::Max(0, $i - 1) }
	elseif ($c -match '^\d+$') { $i = [Math]::Min($steps.Count - 1, [Math]::Max(0, [int]$c - 1)) }
	else { $i++ }
}

# ---- hand-in: show the file and open it, to upload to Moodle
Write-Host ""
Write-Line (U "done_file") Cyan
Write-Host "  $answers" -ForegroundColor Green
Write-Line (U "upload") Cyan
if (-not $env:LAB1_TEST) { Start-Process notepad.exe -ArgumentList "`"$answers`"" }
