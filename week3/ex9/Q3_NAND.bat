@echo off
rem ============================================================
rem  Exercise 9 - question 3: NAND
rem  Y with NAND gates only, built from your SOP. A NAND is w
rem  Type your answer in this window. It is checked at once and,
rem  when it is right, Quartus puts it on the board. A correct
rem  answer that is also what the question asks (canonical /
rem  minimal) gives a code in moodle.txt for Moodle.
rem  The written questions are in answer.txt - run.bat.
rem ============================================================
setlocal
cd /d "%~dp0"
powershell -NoProfile -ExecutionPolicy Bypass -File "tools\ask.ps1" -Q Q3
echo.
pause
