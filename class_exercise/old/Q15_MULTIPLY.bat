@echo off
rem ============================================================
rem  Class exercise - Q15: Multiplying out (SOP) and factoring (POS)
rem  Programs the board with this question, tells you your login
rem  number and the question. The board checks your answer and
rem  shows a code - type it here, it goes into moodle.txt.
rem ============================================================
setlocal
cd /d "%~dp0"
powershell -NoProfile -ExecutionPolicy Bypass -File "tools\run.ps1" -Only Q15
echo.
pause
