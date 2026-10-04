@echo off
rem ============================================================
rem  Exercise 0 - your equation on the board
rem    1. Write an equation with A, B, C on the Y = line in
rem       equation.txt and save.
rem    2. Double-click run.bat.
rem  A = SW3..SW0 (HEX0), B = SW6..SW4 (HEX1),
rem  C = SW9..SW7 (HEX2), Y on HEX3.
rem ============================================================
setlocal
cd /d "%~dp0"
powershell -NoProfile -ExecutionPolicy Bypass -File "tools\run.ps1"
echo.
pause
