@echo off
title School Website Installation
cd /d "%~dp0"
py -m venv venv
call venv\Scripts\activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python seed.py
echo.
echo INSTALLATION COMPLETE
echo Website: http://127.0.0.1:5000
echo Admin: http://127.0.0.1:5000/admin/login
echo Username: admin
echo Password: admin123
pause
