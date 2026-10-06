@echo off
rem ============================================================
rem  Exercise 3 - question 4: MPOS
rem  Minimal POS - use the X rows where they help
rem  Type your answer in this window. It is checked at once and,
rem  when it is right, Quartus puts it on the board. A correct
rem  answer that is also what the question asks (canonical /
rem  minimal) gives a code in moodle.txt for Moodle.
rem  The written questions are in answer.txt - run.bat.
rem ============================================================
setlocal
cd /d "%~dp0"
powershell -NoProfile -ExecutionPolicy Bypass -File "tools\ask.ps1" -Q Q4
echo.
pause
