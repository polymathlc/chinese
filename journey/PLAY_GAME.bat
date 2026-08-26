@echo off
setlocal
cd /d "%~dp0"
title Journey to the West - Local Game Server

set "GAME_PYTHON="
where py >nul 2>nul && set "GAME_PYTHON=py"
if not defined GAME_PYTHON where python >nul 2>nul && set "GAME_PYTHON=python"
if not defined GAME_PYTHON (
  echo Python was not found. Install Python or run: python -m http.server 8765
  pause
  exit /b 1
)

echo Starting Journey to the West at http://127.0.0.1:8765/index.html
echo Keep this window open while playing. Close it to stop the local server.
start "" powershell -NoProfile -WindowStyle Hidden -Command "Start-Sleep -Milliseconds 1200; Start-Process 'http://127.0.0.1:8765/index.html'"
%GAME_PYTHON% -m http.server 8765 --bind 127.0.0.1

endlocal
