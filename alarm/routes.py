from flask import jsonify
from alarm import app
from alarm.views import meetings_ahead, convert_dtypes_to_strings
from alarm.config_handler import get_days_ahead, get_ring_before, get_meetings_config
import win32com.client
import pythoncom

@app.route('/get_meetings', methods=['GET'])
def get_meetings():
    try:
        pythoncom.CoInitialize()
        outlook = win32com.client.Dispatch("Outlook.Application")
        namespace = outlook.GetNamespace("MAPI")
        # print(get_days_ahead(), get_ring_before())
        meetings = meetings_ahead(namespace, days_ahead=get_days_ahead(), ring_before=get_ring_before())
        # meetings = meetings_ahead(namespace, days_ahead=10, ring_before=10)
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