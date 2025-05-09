from flask import Flask
from flask_cors import CORS
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)
CORS(app, expose_headers=["Content-Type","Authorization"], supports_credentials=True)

scheduler = BackgroundScheduler()
scheduler.start()

from alarm.routes import *