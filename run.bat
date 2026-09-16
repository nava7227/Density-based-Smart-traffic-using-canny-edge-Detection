@echo off
cd /d "%~dp0"
if exist ".venv\Scripts\python.exe" (
  ".venv\Scripts\python.exe" Main.py
) else (
  python Main.py
)
if errorlevel 1 pause
