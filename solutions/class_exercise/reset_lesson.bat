@echo off
rem ============================================================
rem  Instructor: reset the class exercise on THIS computer -
rem  every question starts again from step 1.
rem  Deletes progress.txt (steps passed), moodle.txt (codes),
rem  results.txt and the link files in C:\DE10\week3\class_exercise.
rem  The student ID (C:\DE10\student.txt) stays; add  ID  to
rem  delete it too:   reset_lesson.bat ID
rem ============================================================
setlocal
set EX=C:\DE10\week3\class_exercise
taskkill /F /IM quartus_stp.exe >nul 2>&1
for %%f in (progress.txt moodle.txt results.txt lesson_start.txt lesson_pos.txt goto_applied.txt link_state.txt link_state.txt.tmp program.log) do (
	if exist "%EX%\%%f" del /q "%EX%\%%f"
)
if /i "%1"=="ID" if exist "C:\DE10\student.txt" del /q "C:\DE10\student.txt"
echo The class exercise on this computer is reset.
if /i "%1"=="ID" echo The student ID was deleted too - the next run asks for it again.
pause
