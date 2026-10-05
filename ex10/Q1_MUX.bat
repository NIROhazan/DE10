@echo off
rem ============================================================
rem  Exercise 10 - question 1: MUX
rem  A 4:1 mux, selects A (high bit) and B: AB=00 -> D0 ... 1
rem  Type your answer in this window. It is checked at once and,
rem  when it is right, Quartus puts it on the board. A correct
rem  answer that is also what the question asks (canonical /
rem  minimal) gives a code in moodle.txt for Moodle.
rem  The written questions are in answer.txt - run.bat.
rem ============================================================
setlocal
cd /d "%~dp0"
powershell -NoProfile -ExecutionPolicy Bypass -File "tools\ask.ps1" -Q Q1
echo.
pause
