@echo off
rem ============================================================
rem  Instructor: open ONE class-exercise question directly, without
rem  LESSON.bat (students cannot - their questions open only through
rem  the lesson).   question.bat Q05
rem  Uses the progress of this computer (progress.txt) like the lesson.
rem ============================================================
setlocal
if "%1"=="" (
	echo Usage: question.bat Q05
	pause
	exit /b 1
)
set CE_LESSON=1
cd /d C:\DE10\week3\class_exercise
powershell -NoProfile -ExecutionPolicy Bypass -File "tools\run.ps1" -Only %1
echo.
pause
