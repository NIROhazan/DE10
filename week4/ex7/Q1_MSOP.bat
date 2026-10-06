@echo off
rem ============================================================
rem  Exercise 7 - question 1: MSOP
rem  Minimal SOP of your segment: the fewest terms, then the 
rem  Type your answer in this window. It is checked at once and,
rem  when it is right, Quartus puts it on the board. A correct
rem  answer that is also what the question asks (canonical /
rem  minimal) gives a code in moodle.txt for Moodle.
rem ============================================================
setlocal
cd /d "%~dp0"
powershell -NoProfile -ExecutionPolicy Bypass -File "tools\ask.ps1" -Q Q1
echo.
pause
