@echo off
rem ============================================================
rem  Exercise 0 - question 1 of 10 (1 = easiest, 10 = expert)
rem  Programs the board with the equation of Q1, then asks the
rem  question here. Your tries are saved in results.txt.
rem ============================================================
setlocal
cd /d "%~dp0"
powershell -NoProfile -ExecutionPolicy Bypass -File "tools\run.ps1" -Only Q1
echo.
pause
