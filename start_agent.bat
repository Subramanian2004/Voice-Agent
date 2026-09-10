@echo off
cd /d "%~dp0"
call venv\Scripts\activate.bat
cd src
python main.py
pause