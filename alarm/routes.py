from flask import jsonify, request
from alarm import app
from alarm.views import meetings_ahead, convert_dtypes_to_strings
from alarm.config_handler import *
import win32com.client
import pythoncom

@app.route('/', methods=['GET'])
def home():
    return jsonify(status="success", message="Alarm API is running.")

@app.route('/get_meetings', methods=['GET'])
def get_meetings():
    try:
        pythoncom.CoInitialize()
        outlook = win32com.client.Dispatch("Outlook.Application")
        namespace = outlook.GetNamespace("MAPI")
        print(get_days_ahead(), get_ring_before())
        meetings = meetings_ahead(namespace, days_ahead=get_days_ahead(), ring_before=get_ring_before())
        return jsonify(status="success", meetings=convert_dtypes_to_strings(meetings[:5]))
    except Exception as e:
        return jsonify(status="error1", message=str(e))

@app.route('/next_meeting', methods=['GET'])
def next_meeting():
    try:
        _ = get_meetings()
        meetings = get_meetings_config()
        return jsonify(status="success", meeting=convert_dtypes_to_strings([meetings[0]]))
    except Exception as e:
        return jsonify(status="error1", message=str(e))
    
@app.route('/set_ring_before', methods=['POST'])
def set_ring_before_route():
    try:
        ring_before = int(request.json.get('ring_before', 5))
        set_ring_before(ring_before)
        set_meetings_config([])
        return jsonify(status="success", message="Ring before time updated.")
    except Exception as e:
        return jsonify(status="error1", message=str(e))

@app.route('/set_days_ahead', methods=['POST'])
def set_days_ahead_route():
    try:
        days_ahead = int(request.json.get('days_ahead', 10))
        set_days_ahead(days_ahead)
        return jsonify(status="success", message="Days ahead updated.")
    except Exception as e:
        return jsonify(status="error1", message=str(e))