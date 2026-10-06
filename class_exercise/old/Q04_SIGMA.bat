@echo off
rem ============================================================
rem  Class exercise - Q04: Minterms: write F as a sum of products, F = SIGMA(...)
rem  Programs the board with this question, tells you your login
rem  number and the question. The board checks your answer and
rem  shows a code - type it here, it goes into moodle.txt.
rem ============================================================
setlocal
cd /d "%~dp0"
powershell -NoProfile -ExecutionPolicy Bypass -File "tools\run.ps1" -Only Q04
echo.
pause
