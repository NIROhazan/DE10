@echo off
rem ============================================================
rem  The class lesson - the only way to the questions.
rem  Your progress is kept; closing and opening again goes on.
rem ============================================================
setlocal
cd /d "%~dp0"
powershell -NoProfile -ExecutionPolicy Bypass -File "..\tools\lesson.ps1"
echo.
pause
