@echo off
rem ============================================================
rem  Exercise 0 - free mode: your own equation
rem  Write it on the Y = line of equation.txt, save, double-click.
rem ============================================================
setlocal
cd /d "%~dp0"
powershell -NoProfile -ExecutionPolicy Bypass -File "tools\free.ps1"
echo.
pause
