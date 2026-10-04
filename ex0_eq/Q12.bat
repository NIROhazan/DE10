@echo off
rem ============================================================
rem  Exercise 0 - question 12
rem  Programs the board with the equation of Q12, then asks the
rem  question here. Your tries are saved in results.txt.
rem ============================================================
setlocal
cd /d "%~dp0"
powershell -NoProfile -ExecutionPolicy Bypass -File "tools\run.ps1" -Only Q12
echo.
pause
