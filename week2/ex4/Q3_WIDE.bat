@echo off
rem ============================================================
rem  Exercise 4 - sign-extension and zero-extension
rem  Q3: extend 8 to 16 bits
rem  Programs the board, asks the question here with your own
rem  numbers, and checks your answer. A wrong answer gives NEW
rem  numbers. A right one gives a code in moodle.txt for Moodle.
rem ============================================================
setlocal
cd /d "%~dp0"
powershell -NoProfile -ExecutionPolicy Bypass -File "tools\run.ps1" -Only Q3
echo.
pause
