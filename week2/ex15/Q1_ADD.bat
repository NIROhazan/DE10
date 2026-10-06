@echo off
rem ============================================================
rem  Exercise 15 - binary addition and overflow
rem  Q1: add two 4-bit numbers
rem  Programs the board, asks the question here with your own
rem  numbers, and checks your answer. A wrong answer gives NEW
rem  numbers. A right one gives a code in moodle.txt for Moodle.
rem ============================================================
setlocal
cd /d "%~dp0"
powershell -NoProfile -ExecutionPolicy Bypass -File "tools\run.ps1" -Only Q1
echo.
pause
