from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app, expose_headers=["Content-Type","Authorization"], supports_credentials=True)

from alarm.routes import *