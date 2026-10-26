# Instructor test: a real LESSON run in its own window for a class-exercise folder, then restore the student files.
#   powershell -File test_lesson.ps1 -Dir C:\DE10\week5\class_exercise -Goto "TOPIC 1 QUESTION 5"
param([string]$Dir, [string]$Goto = "TOPIC 1", [int]$Wait = 35)
$sp = Join-Path $PSScriptRoot "test_tmp"
New-Item -ItemType Directory -Force $sp | Out-Null
$keep = "goto.txt", "lesson_start.txt", "lesson_pos.txt", "goto_applied.txt", "progress.txt", "moodle.txt"
foreach ($f in $keep) { Remove-Item "$sp\bak_$f" -ErrorAction SilentlyContinue; if (Test-Path "$Dir\$f") { Copy-Item "$Dir\$f" "$sp\bak_$f" -Force } }
$Goto | Set-Content "$Dir\goto.txt" -Encoding ASCII
$w = "$sp\run.ps1"
"Start-Transcript -Path '$sp\tr.txt' -Force | Out-Null; & '$Dir\tools\goto.ps1'" | Set-Content $w -Encoding ASCII
$p = Start-Process powershell -ArgumentList '-NoProfile', '-ExecutionPolicy', 'Bypass', '-File', $w -PassThru
Start-Sleep $Wait
if (-not $p.HasExited) { Stop-Process -Id $p.Id -Force }
Get-Process quartus_stp -ErrorAction SilentlyContinue | Stop-Process -Force
"board state: " + $(if (Test-Path "$Dir\link_state.txt") { (Get-Content "$Dir\link_state.txt" -Raw).Trim() } else { "(none)" })
$tr = Get-Content "$sp\tr.txt" -Encoding UTF8
"errors: " + @($tr | Where-Object { $_ -match 'Exception|is not recognized|ParserError|CategoryInfo' }).Count + "     questions shown: " +
	((@($tr | Select-String -Pattern 'Q\d\d' -AllMatches | ForEach-Object { $_.Matches.Value }) | Sort-Object -Unique) -join " ")
foreach ($f in $keep) { if (Test-Path "$sp\bak_$f") { Copy-Item "$sp\bak_$f" "$Dir\$f" -Force } else { Remove-Item "$Dir\$f" -ErrorAction SilentlyContinue } }
Remove-Item "$Dir\link_state.txt", "$Dir\program.log" -ErrorAction SilentlyContinue
