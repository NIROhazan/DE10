# LESSON.bat = goto.ps1, the students' only way in. Reads goto.txt:
#   no line                     -> the lesson by the class clock (START in lesson.txt), like before
#   TOPIC n / TOPIC n QUESTION k -> a NEW line: topic n starts now with its full time (lesson_start.txt, which lesson.ps1
#                                  prefers over START) and its k-th question opens first (lesson.ps1 -First).
#                                  The same line as last time (goto_applied.txt): just go on - no new jump, the clock runs on.
# No choosing of minutes. The progress stays. Kept ASCII for PowerShell 5.1.
$ErrorActionPreference = "Stop"
Set-Location (Split-Path $PSScriptRoot -Parent)
. (Join-Path $PSScriptRoot "common.ps1")		# Write-Line, U (the Hebrew screen texts)

$topics = @()
foreach ($l in [IO.File]::ReadAllLines((Join-Path $PSScriptRoot "lesson.txt"))) {
	if ($l -match '^\s*TOPIC\s+([\d.]+)\s*\|\s*(.+?)\s*\|\s*(.+?)\s*$') {
		$topics += [pscustomobject]@{ Min = [double]$Matches[1]; Name = $Matches[2]; Qs = @($Matches[3] -split '\s+' | Where-Object { $_ }) }
	}
}

function Fail($lines) {
	Write-Host ""
	@($lines) | ForEach-Object { Write-Line $_ Red }
	Write-Host ""
	for ($i = 0; $i -lt $topics.Count; $i++) { Write-Line ((U "goto_list") -f ($i + 1), $topics[$i].Name, $topics[$i].Qs.Count) }
	Write-Host ""
	Write-Line (U "goto_fix") Yellow
	Write-Line (U "goto_fix_en") Yellow
	exit 1
}

$f = Join-Path (Get-Location) "goto.txt"
if (-not (Test-Path $f)) { Fail @((U "goto_bad"), (U "goto_bad_en")) }
# every non-comment line together: "TOPIC 1 QUESTION 3" on one line, or TOPIC 1 and QUESTION 3 on two lines
$line = (@([IO.File]::ReadAllLines($f) | Where-Object { $_ -notmatch '^\s*(#|$)' } | ForEach-Object { $_.Trim() }) -join " ")
$applied = Join-Path (Get-Location) "goto_applied.txt"
$lesson = Join-Path $PSScriptRoot "lesson.ps1"
if (-not $line) {				# nothing chosen: the lesson by the class clock
	Remove-Item $applied, (Join-Path (Get-Location) "lesson_start.txt") -ErrorAction SilentlyContinue
	& $lesson
	exit $LASTEXITCODE
}
if ((Test-Path $applied) -and (([IO.File]::ReadAllText($applied)).Trim() -eq $line.Trim())) {
	& $lesson				# the same choice as last time: go on where you are
	exit $LASTEXITCODE
}
if ($line -notmatch '^\s*TOPIC\s+(\d+)(?:\s+QUESTION\s+(\d+))?\s*$') {
	Fail @((U "goto_bad"), (U "goto_bad_en"))
}
$n = [int]$Matches[1]
$k = if ($Matches[2]) { [int]$Matches[2] } else { 1 }
if ($n -lt 1 -or $n -gt $topics.Count) { Fail ((U "goto_no_topic") -f $topics.Count) }
$tp = $topics[$n - 1]
if ($k -lt 1 -or $k -gt $tp.Qs.Count) { Fail ((U "goto_no_q") -f $n, $tp.Qs.Count) }
$first = $tp.Qs[$k - 1]

$offset = 0
for ($i = 0; $i -lt $n - 1; $i++) { $offset += $topics[$i].Min }
$start = (Get-Date).AddMinutes(-$offset)
[IO.File]::WriteAllText((Join-Path (Get-Location) "lesson_start.txt"), $start.ToString("o"))
[IO.File]::WriteAllText($applied, $line.Trim())
Write-Host ""
Write-Line ((U "goto_jump") -f $n, $k, $tp.Qs.Count) Green
Start-Sleep -Seconds 2
& $lesson -First $first
exit $LASTEXITCODE
