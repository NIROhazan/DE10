@echo off
rem ============================================================
rem  D5M camera demo - loads the boards, no compile needed
rem    Board with the camera on JP1  -> d5m_camera\sof\d5m_cam.sof
rem    Second DE10-Lite (if plugged) -> flicker_tx\sof\flicker_tx.sof
rem  It finds out which board has the camera by itself,
rem  so the USB ports can be in any order.
rem  Run it again after a board was unplugged.
rem  Details: d5m_camera\README.md
rem ============================================================
setlocal
cd /d "%~dp0"
powershell -NoProfile -ExecutionPolicy Bypass -File "d5m_camera\tools\demo.ps1" %*
echo.
pause
