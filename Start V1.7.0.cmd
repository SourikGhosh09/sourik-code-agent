@echo off
cd /d "%~dp0"
python scripts\start_local_runtime.py
if errorlevel 1 (pause & exit /b 1)
pythonw -m local_agent
