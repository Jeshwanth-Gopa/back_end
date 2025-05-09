from datetime import datetime, timedelta
from tkinter import Tk, Label, Button
from alarm.config_handler import get_meetings_config, set_meetings_config
import threading
import pygame
import json

with open("alarm/config.json") as f:
    config = json.load(f)

snooze_minutes = config.get("snooze_minutes", 5)
ringtone_file = config.get("ringtone_file", "alarm/ringtone.wav")

def play_ringtone():
    pygame.mixer.init()
    pygame.mixer.music.load(config['ringtone_file'])
    pygame.mixer.music.play()
    
def show_popup(scheduler, meeting):
    def snooze():
        print("Snoozed")
        pygame.mixer.music.stop()
        meeting["ring_at"] = (datetime.now() + timedelta(minutes=snooze_minutes)).isoformat()
        add_jobs(scheduler, [meeting])
        meetings = get_meetings_config()
        for m in meetings:
            if m["id"] == meeting["id"]:
                m["ring_at"] = meeting["ring_at"]
                break
        set_meetings_config(meetings)
        win.destroy()

    def dismiss():
        pygame.mixer.music.stop()
        win.destroy()

    win = Tk()
    win.title("Meeting Reminder")
    win.attributes("-topmost", True)
    win.lift()
    win.focus_force()  
    start_time = datetime.fromisoformat(meeting['start'])

    Label(win, text=f"Subject: {meeting['subject']}", font=("Arial", 14)).pack(pady=5)
    Label(win, text=f"Starts at: {start_time.strftime("%I:%M %p")}", font=("Arial", 12)).pack(pady=2)
    Label(win, text=f"Account: {meeting['account']}", font=("Arial", 10)).pack(pady=2)

    Button(win, text="Snooze 5 min", command=snooze, width=15).pack(pady=5)
    Button(win, text="Dismiss", command=dismiss, width=15).pack(pady=5)

    threading.Thread(target=play_ringtone).start()
    win.mainloop()

def add_jobs(scheduler, meetings):
    for meeting in meetings:
        ring_at = datetime.fromisoformat(meeting["ring_at"])
        scheduler.add_job(show_popup, 'date', run_date=ring_at, id=str(meeting["id"]), args=[scheduler, meeting])
        print(f"Scheduled to run at: {ring_at}")

def remove_all_jobs(scheduler):
    scheduler.remove_all_jobs()

def edit_job(scheduler, meeting_id, meeting):
    try:
        job = scheduler.get_job(meeting_id)
        if job:
            scheduler.remove_job(meeting_id)
            scheduler.add_job(show_popup, 'date', run_date=meeting['ring_at'], id=meeting_id, args=[scheduler, meeting])
            print("edited_job")
    except Exception as e:
        print("Error:", e)