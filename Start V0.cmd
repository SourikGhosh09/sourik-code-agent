@echo off
cd /d "%~dp0"
python scripts\start_local_runtime.py
if errorlevel 1 (pause & exit /b 1)
cd /d "%~dp0releases\v0-462a311"
pythonw -m local_agent
