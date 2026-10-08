@echo off
rem ============================================================
rem  The class lesson - the only way to the questions.
rem  goto.txt empty: the lesson by the class clock.
rem  goto.txt with TOPIC 2 or TOPIC 1 QUESTION 3: start there.
rem  Your progress is kept; closing and opening again goes on.
rem ============================================================
setlocal
cd /d "%~dp0"
powershell -NoProfile -ExecutionPolicy Bypass -File "tools\goto.ps1"
echo.
pause
