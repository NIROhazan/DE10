@echo off
rem ============================================================
rem  Exercise 0 - check your answers in answer.txt
rem  Says OK / wrong / empty for each question.
rem  It does not program the board - use run.bat for that.
rem ============================================================
setlocal
cd /d "%~dp0"
powershell -NoProfile -ExecutionPolicy Bypass -File "tools\check.ps1"
echo.
pause
