import win32com.client, hashlib
from datetime import datetime, timedelta

def remove_timezone(dt):
    return dt.replace(tzinfo=None) if dt.tzinfo else dt

def convert_dtypes_to_strings(meetings):
    return [{str(k): str(v) for k,v in m.items()} for m in meetings]

def meetings_ahead(namespace, days_ahead=8, ring_before=0):
    now      = datetime.now()
    end_time = now + timedelta(days=days_ahead)
    meetings = []

    for account in namespace.Accounts:
        try:
            calendar = namespace.Folders(account.DisplayName).Folders("Calendar")
            items    = calendar.Items
            items.Sort("[Start]"); items.IncludeRecurrences = True

            for item in items:
                start = remove_timezone(item.Start)
                if not (now <= start <= end_time):
                    continue

                st = item.Subject + str(start) + str(item.End) + account.SmtpAddress
                meetings.append({
                    "subject": item.Subject,
                    "start":   start,
                    "end":     remove_timezone(item.End),
                    "account": account.SmtpAddress,
                    "ring_at": start - timedelta(minutes=ring_before),
                    "id":      hashlib.sha256(st.encode()).hexdigest()
                })
        except Exception as e:
            print(f"Error with {account.DisplayName}: {e}")

    return meetings