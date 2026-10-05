@echo off
rem ============================================================
rem  Exercise 0 - question 13 of 20 (set 2: 11 = easy, 20 = expert)
rem  Programs the board with the equation of Q13, then asks the
rem  question here. Your tries are saved in results.txt.
rem ============================================================
setlocal
cd /d "%~dp0"
powershell -NoProfile -ExecutionPolicy Bypass -File "tools\run.ps1" -Only Q13
echo.
pause
