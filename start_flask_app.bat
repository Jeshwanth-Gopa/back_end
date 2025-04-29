@echo off
cd /d %~dp0
call venv\Scripts\activate.bat
set FLASK_APP=meeting_ahead_wsgi.py
set FLASK_DEBUG=True
flask run