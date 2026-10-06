@echo off
rem ============================================================
rem  Exercise 4 - written question 4 (question 4 in answer.txt)
rem  The question is shown here; Notepad opens for your answer
rem  (Hebrew or English). Save and close Notepad - Claude checks
rem  it and opens the feedback. A right answer gives a code in
rem  moodle.txt for Moodle.
rem ============================================================
setlocal
cd /d "%~dp0"
powershell -NoProfile -ExecutionPolicy Bypass -File "tools\text.ps1" -Q Q7
echo.
pause
