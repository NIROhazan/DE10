@echo off
rem ============================================================
rem  Exercise 0 - question 5 of 20 (set 1: 1 = easiest, 10 = expert)
rem  Programs the board with the equation of Q5, then asks the
rem  question here. Your tries are saved in results.txt.
rem ============================================================
setlocal
cd /d "%~dp0"
powershell -NoProfile -ExecutionPolicy Bypass -File "tools\run.ps1" -Only Q5
echo.
pause
