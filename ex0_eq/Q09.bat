@echo off
rem ============================================================
rem  Exercise 0 - question 9
rem  Programs the board with the equation of Q9, then asks the
rem  question here. Your tries are saved in results.txt.
rem ============================================================
setlocal
cd /d "%~dp0"
powershell -NoProfile -ExecutionPolicy Bypass -File "tools\run.ps1" -Only Q9
echo.
pause
