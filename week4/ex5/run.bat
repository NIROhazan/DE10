@echo off
rem ============================================================
rem  Exercise 5 - implicants, prime implicants, essential prime implicants
rem    1. Write your answers in answer.txt and save it.
rem    2. Double-click run.bat.
rem  Claude reads answer.txt, turns your expressions into Verilog
rem  (student_logic.v), writes feedback.txt, then Quartus puts
rem  your logic on the board.
rem    run.bat check    Claude + feedback only, no board
rem ============================================================
setlocal
cd /d "%~dp0"
powershell -NoProfile -ExecutionPolicy Bypass -File "tools\run.ps1" %1
echo.
pause
