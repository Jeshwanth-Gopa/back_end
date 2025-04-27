import datetime, pywintypes

def convert_pywindtypes_to_dtypes(meetings):
    for m in meetings:
        for k, v in m.items():
            if type(v) is pywintypes.TimeType:
                m[k] = datetime.combine(v.date(), v.time())
    return meetings