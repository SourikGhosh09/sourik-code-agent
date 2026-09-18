@echo off
cd /d "%~dp0"
python scripts\start_local_runtime.py
pythonw -m local_agent
