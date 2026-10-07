@echo off
rem ============================================================
rem  Class lesson - runs the whole lesson by the clock (tools\lesson.txt):
rem  topic after topic, each with its questions from easy to hard.
rem  Double-click once at the start of the lesson and leave it open.
rem ============================================================
setlocal
cd /d "%~dp0"
powershell -NoProfile -ExecutionPolicy Bypass -File "tools\lesson.ps1"
echo.
pause
