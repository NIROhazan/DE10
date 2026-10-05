@echo off
rem ============================================================
rem  Exercise 2 - question 2: POS
rem  Canonical POS: one maxterm for every row where Y = 0, e.
rem  Type your answer in this window. It is checked at once and,
rem  when it is right, Quartus puts it on the board. A correct
rem  answer that is also what the question asks (canonical /
rem  minimal) gives a code in moodle.txt for Moodle.
rem  The written questions are in answer.txt - run.bat.
rem ============================================================
setlocal
cd /d "%~dp0"
powershell -NoProfile -ExecutionPolicy Bypass -File "tools\ask.ps1" -Q Q2
echo.
pause
