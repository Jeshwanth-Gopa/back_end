from flask import jsonify
from alarm import app
from alarm.views import meetings_ahead, convert_dtypes_to_strings
import win32com.client
import pythoncom

@app.route('/get_meetings', methods=['GET'])
def get_meetings():
    # print(namespace)
    try:
        pythoncom.CoInitialize()
        outlook = win32com.client.Dispatch("Outlook.Application")
        namespace = outlook.GetNamespace("MAPI")
        meetings = meetings_ahead(namespace, days_ahead=10, ring_before=5)
        return jsonify(status="success", meetings=convert_dtypes_to_strings(meetings[:5]))
    except Exception as e:
        return jsonify(status="error", message=str(e))