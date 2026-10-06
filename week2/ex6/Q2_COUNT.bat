@echo off
rem ============================================================
rem  Exercise 6 - CMOS gates
rem  Q2: how many transistors (needs the board)
rem  Programs the board, asks the question here with your own
rem  numbers, and checks your answer. A wrong answer gives NEW
rem  numbers. A right one gives a code in moodle.txt for Moodle.
rem ============================================================
setlocal
cd /d "%~dp0"
powershell -NoProfile -ExecutionPolicy Bypass -File "tools\run.ps1" -Only Q2
echo.
pause
