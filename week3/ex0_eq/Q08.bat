@echo off
rem ============================================================
rem  Exercise 0 - question 8 of 20 (set 1: 1 = easiest, 10 = expert)
rem  Programs the board with the equation of Q8, then asks the
rem  question here. Your tries are saved in results.txt.
rem ============================================================
setlocal
cd /d "%~dp0"
powershell -NoProfile -ExecutionPolicy Bypass -File "tools\run.ps1" -Only Q8
echo.
pause
