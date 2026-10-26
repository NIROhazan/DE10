@echo off
rem ============================================================
rem  Instructor: restart the lesson clock on THIS computer.
rem    reset_time.bat      topic 1 starts now
rem    reset_time.bat 2    topic 2 starts now (topic 1 counted as over)
rem  The progress stays. Close and reopen LESSON.bat afterwards.
rem ============================================================
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0reset_time.ps1" %1
pause
