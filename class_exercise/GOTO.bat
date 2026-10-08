@echo off
rem ============================================================
rem  Go to a chosen moment of the lesson: write it in goto.txt
rem  (TOPIC 2, TOPIC 2 10 or MINUTE 45), save, then run this.
rem  Your progress is kept; LESSON.bat then goes on with this clock.
rem ============================================================
setlocal
cd /d "%~dp0"
powershell -NoProfile -ExecutionPolicy Bypass -File "tools\goto.ps1"
echo.
pause
