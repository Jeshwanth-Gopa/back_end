@echo off
cd C:\Users\jkgopa\Desktop\Back_End
call venv\Scripts\activate.bat
cd C:\Users\jkgopa\Desktop\Back_End
set FLASK_APP=meeting_ahead_wsgi.py
set FLASK_DEBUG=True
flask run
