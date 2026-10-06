@echo off
rem ============================================================
rem  Exercise 7 - question 2: MPOS
rem  Minimal POS of your segment: the fewest sums, then the f
rem  Type your answer in this window. It is checked at once and,
rem  when it is right, Quartus puts it on the board. A correct
rem  answer that is also what the question asks (canonical /
rem  minimal) gives a code in moodle.txt for Moodle.
rem ============================================================
setlocal
cd /d "%~dp0"
powershell -NoProfile -ExecutionPolicy Bypass -File "tools\ask.ps1" -Q Q2
echo.
pause
