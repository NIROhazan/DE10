# Instructor: restart the lesson clock on THIS computer (progress stays). reset_time.bat [topic]
#   no topic  -> topic 1 starts now;   2 -> topic 2 starts now (as if topic 1 had just ended), ...
# Writes C:\DE10\week3\class_exercise\lesson_start.txt, which lesson.ps1 prefers over START (a personal clock).
# reset_lesson.bat deletes it again (back to the class clock, and the progress too).
param([int]$Topic = 1)
$ex = "C:\DE10\week3\class_exercise"
. (Join-Path $ex "tools\common.ps1")		# Write-Line: the topic names are Hebrew
$mins = @()
foreach ($l in [IO.File]::ReadAllLines((Join-Path $ex "tools\lesson.txt"), (New-Object System.Text.UTF8Encoding($false)))) {
	if ($l -match '^\s*TOPIC\s+([\d.]+)\s*\|\s*(.+?)\s*\|') { $mins += [pscustomobject]@{ Min = [double]$Matches[1]; Name = $Matches[2] } }
}
if ($Topic -lt 1 -or $Topic -gt $mins.Count) { Write-Host "There are $($mins.Count) topics - give 1 to $($mins.Count)." -ForegroundColor Red; exit 1 }
$before = 0
for ($i = 0; $i -lt $Topic - 1; $i++) { $before += $mins[$i].Min }
$start = (Get-Date).AddMinutes(-$before)
[IO.File]::WriteAllText((Join-Path $ex "lesson_start.txt"), $start.ToString("o"))
Write-Host ""
Write-Host "  The lesson clock on this computer starts again: topic $Topic begins now." -ForegroundColor Green
$t = $start
for ($i = 0; $i -lt $mins.Count; $i++) {
	$e = $t.AddMinutes($mins[$i].Min)
	if ($i -ge $Topic - 1) { Write-Line ("{0:HH:mm}-{1:HH:mm}     {2}" -f $t, $e, $mins[$i].Name) }
	$t = $e
}
Write-Host ""
Write-Host "  The progress (steps already passed) is kept. If LESSON.bat is open, close it and open it again."
Write-Host "  Back to the class clock: reset_lesson.bat (it also deletes the progress)."
