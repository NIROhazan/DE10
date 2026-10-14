@echo off
rem ============================================================
rem  Lab 1 - play with the board, guess, write it down.
rem  Programs the board by itself at each step (USB cable).
rem  Answers go to answers_ID.txt here; upload it to Moodle.
rem ============================================================
setlocal
cd /d "%~dp0"
powershell -NoProfile -ExecutionPolicy Bypass -File "tools\lab1.ps1"
echo.
pause
