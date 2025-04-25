import win32com.client
from views import meetings_ahead, convert_dtypes_to_strings

outlook = win32com.client.Dispatch("Outlook.Application")
namespace = outlook.GetNamespace("MAPI")

meetings = meetings_ahead(namespace, 10, 5)