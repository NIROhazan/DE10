@echo off
rem ============================================================
rem  Exercise 0 - question 11
rem  Programs the board with the equation of Q11, then asks the
rem  question here. Your tries are saved in results.txt.
rem ============================================================
setlocal
cd /d "%~dp0"
powershell -NoProfile -ExecutionPolicy Bypass -File "tools\run.ps1" -Only Q11
echo.
pause
