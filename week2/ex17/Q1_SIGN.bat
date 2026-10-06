@echo off
rem ============================================================
rem  Exercise 17 - sign-extension and zero-extension
rem  Q1: sign-extend 4 to 8 bits
rem  Programs the board, asks the question here with your own
rem  numbers, and checks your answer. A wrong answer gives NEW
rem  numbers. A right one gives a code in moodle.txt for Moodle.
rem ============================================================
setlocal
cd /d "%~dp0"
powershell -NoProfile -ExecutionPolicy Bypass -File "tools\run.ps1" -Only Q1
echo.
pause
