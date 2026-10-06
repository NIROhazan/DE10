@echo off
rem ============================================================
rem  Exercise 4 - question 2: MSOP
rem  Minimal SOP of your story: the fewest terms, then the fe
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
