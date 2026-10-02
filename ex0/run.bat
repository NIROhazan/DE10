@echo off
rem ============================================================
rem  Exercise 0 - LED wave demo (no answers, just watch it run)
rem  Compiles ex0 with Quartus II 13.0sp1 and puts it on the board.
rem ============================================================
setlocal
cd /d "%~dp0"
set QBIN=C:\altera\13.0sp1\quartus\bin64
echo Compiling ex0 (1-2 minutes)...
"%QBIN%\quartus_sh.exe" --flow compile ex0 > compile.log 2>&1
if errorlevel 1 ( echo Compile FAILED - see compile.log & goto end )
echo Programming the board...
"%QBIN%\quartus_pgm.exe" -c USB-Blaster -m JTAG -o "p;output_files\ex0.sof" > program.log 2>&1
if errorlevel 1 ( echo Programming FAILED. Is the board on, the USB cable in the BLASTER port, and the switch on RUN? & goto end )
echo Done - watch LEDR9..LEDR0.
:end
echo.
pause
