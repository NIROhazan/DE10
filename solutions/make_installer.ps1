# Wraps a student kit (labN_kit.zip, as attached on Moodle) into ONE file: labN_kit_install.bat.
# The student double-clicks it (from Downloads): the kit goes to F:\labN_kit (the personal drive; another student's
# files never get in) and weekN\LESSON.bat opens. Running it again replaces only the kit's files - progress.txt,
# moodle.txt, student.txt and the lesson files stay.
#   powershell -File make_installer.ps1 -Zip C:\path\lab3_kit.zip [-Out C:\path\lab3_kit_install.bat] [-Drive F:]
# Kept ASCII for PowerShell 5.1.
param([Parameter(Mandatory = $true)][string]$Zip, [string]$Out = "", [string]$Drive = "F:")

$ErrorActionPreference = "Stop"
Add-Type -AssemblyName System.IO.Compression.FileSystem
$Zip = (Resolve-Path $Zip).Path

# the kit's top folder (labN_kit) and its week folder (weekN), from the zip itself
$names = @([IO.Compression.ZipFile]::OpenRead($Zip).Entries | ForEach-Object { $_.FullName })
$kit = @($names | ForEach-Object { ($_ -split '/')[0] } | Sort-Object -Unique)
if ($kit.Count -ne 1) { throw "The zip must hold one top folder (labN_kit), found: $($kit -join ', ')" }
$kit = $kit[0]
$week = @($names | Where-Object { $_ -match "^$kit/(week\d+)/LESSON\.bat$" } | ForEach-Object { ($_ -split '/')[1] })
if ($week.Count -ne 1) { throw "No single $kit/weekN/LESSON.bat in the zip." }
$week = $week[0]
if (-not $Out) { $Out = Join-Path (Split-Path $Zip -Parent) "${kit}_install.bat" }

$b64 = [Convert]::ToBase64String([IO.File]::ReadAllBytes($Zip), [Base64FormattingOptions]::InsertLineBreaks)
$bat = @"
@echo off
rem ============================================================
rem  Installs $kit into $Drive\$kit (your personal drive) and opens the lesson.
rem  Run it again any time: only the kit's files are replaced, your progress stays.
rem ============================================================
setlocal
set "KIT=$kit"
set "DEST=$Drive\$kit"
set "TMPX=%TEMP%\%KIT%_install"
if not exist $Drive\ (
	echo.
	echo   Drive $Drive was not found. Log in to the college computer with your own user, then run this again.
	echo.
	pause
	exit /b 1
)
echo.
echo   Installing %KIT% into %DEST% ...
set "SELF=%~f0"
powershell -NoProfile -ExecutionPolicy Bypass -Command "`$ErrorActionPreference='Stop'; `$t=[IO.File]::ReadAllText(`$env:SELF); `$b=`$t.Substring(`$t.IndexOf('::ZIP'+'::')+7) -replace '\s',''; `$z=`$env:TMPX+'.zip'; [IO.File]::WriteAllBytes(`$z,[Convert]::FromBase64String(`$b)); if(Test-Path `$env:TMPX){Remove-Item `$env:TMPX -Recurse -Force}; Add-Type -AssemblyName System.IO.Compression.FileSystem; [IO.Compression.ZipFile]::ExtractToDirectory(`$z,`$env:TMPX); Remove-Item `$z"
if errorlevel 1 goto fail
robocopy "%TMPX%\%KIT%" "%DEST%" /E /R:1 /W:1 /NFL /NDL /NJH /NJS /NP >nul
if errorlevel 8 goto fail
rmdir /s /q "%TMPX%"
echo   Done. The kit is in %DEST% - opening the lesson.
start "" /d "%DEST%\$week" "%DEST%\$week\LESSON.bat"
exit /b 0
:fail
echo.
echo   The install failed - show this window to the lecturer.
echo.
pause
exit /b 1
::ZIP::
$b64
"@
[IO.File]::WriteAllText($Out, ($bat -replace "`r?`n", "`r`n"), (New-Object System.Text.UTF8Encoding($false)))
Write-Host "ok  $Out  ($kit, $week, $([Math]::Round((Get-Item $Out).Length / 1MB, 1)) MB)"
