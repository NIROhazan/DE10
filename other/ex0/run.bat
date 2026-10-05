@echo off
rem ============================================================
rem  Exercise 0 - LED wave: change the numbers, predict, check
rem    1. Change a number in the KNOBS block of ex0_top.v.
rem    2. Write your prediction on the PREDICT: line at the
rem       bottom of answer.txt and save.
rem    3. Double-click run.bat.
rem  No prediction - no run. Every run is logged in history.txt.
rem ============================================================
setlocal
cd /d "%~dp0"
powershell -NoProfile -ExecutionPolicy Bypass -File "tools\run.ps1"
echo.
pause
