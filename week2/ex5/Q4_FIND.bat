@echo off
rem ============================================================
rem  Exercise 5 - mystery gates
rem  Q4: search the puzzles (needs the board)
rem  Programs the board, asks the question here with your own
rem  numbers, and checks your answer. A wrong answer gives NEW
rem  numbers. A right one gives a code in moodle.txt for Moodle.
rem ============================================================
setlocal
cd /d "%~dp0"
powershell -NoProfile -ExecutionPolicy Bypass -File "tools\run.ps1" -Only Q4
echo.
pause
