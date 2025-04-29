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
        return jsonify(status="success", meetings=convert_dtypes_to_strings(meetings[:get_num()]))
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

@app.route('/set_num_meetings', methods=['POST'])
def set_num_meetings_route():
    try:
        num = request.json.get("num", 5)
        set_num(num)
        meetings = get_meetings_config()
        return jsonify(status="success", meeting=meetings)
    except Exception as e:
        return jsonify(status="error1", message=str(e))

@app.route('/get_ring_before', methods=['GET'])
def get_ring_before_route():
    try:
        ring_before = get_ring_before()
        return jsonify(status="success", ring_before=ring_before)
    except Exception as e:
        return jsonify(status="error1", message=str(e))

@app.route('/set_ring_before', methods=['POST'])
def set_ring_before_route():
    try:
        ring_before = int(request.json.get('ring_before', 5))
        set_ring_before(ring_before)
        set_meetings_config([])
        _ = get_meetings()
        return jsonify(status="success", message="Ring before time updated.")
    except Exception as e:
        return jsonify(status="error", message=str(e))

@app.route('/get_days_ahead', methods=['GET'])
def get_days_ahead_route():
    try:
        days_ahead = get_days_ahead()
        return jsonify(status="success", days_ahead=days_ahead)
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

@app.route('/set_alarm_particular_meeting', methods=['POST'])
def set_alarm_particular_meeting_route():
    try:
        meeting_id = request.json.get('id')
        ring_at = request.json.get('ring_at')
        meetings = get_meetings_config()
        for m in meetings:
            if m["id"] == meeting_id:
                m["ring_at"] = ring_at
                break
        set_meetings_config(meetings)
        return jsonify(status="success", message="Alarm set for the particular meeting.")
    except Exception as e:
        return jsonify(status="error1", message=str(e))