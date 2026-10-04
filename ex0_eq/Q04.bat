@echo off
rem ============================================================
rem  Exercise 0 - question 4
rem  Programs the board with the equation of Q4, then asks the
rem  question here. Your tries are saved in results.txt.
rem ============================================================
setlocal
cd /d "%~dp0"
powershell -NoProfile -ExecutionPolicy Bypass -File "tools\run.ps1" -Only Q4
echo.
pause
