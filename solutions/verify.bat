@echo off
rem Instructor: check the moodle.txt files of any exercise.  verify.bat <folder with the unzipped Moodle submissions>
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0verify.ps1" %*
pause
