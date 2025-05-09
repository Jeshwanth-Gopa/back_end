from datetime import datetime, timedelta
from tkinter import Tk, Label, Button
import threading
import pygame

SNOOZE_MINUTES = 5
RINGTONE_FILE = "ringtone.wav"  # Path to your ringtone file

def play_ringtone():
    pygame.mixer.init()
    pygame.mixer.music.load(RINGTONE_FILE)  # Or .wav file
    pygame.mixer.music.play()

def show_popup(meeting):
    def snooze():
        meeting["ring_at"] = (datetime.now() + timedelta(minutes=SNOOZE_MINUTES)).isoformat()
        print(meeting)
        win.destroy()

    def dismiss():
        win.destroy()

    win = Tk()
    win.title("Meeting Reminder")

    Label(win, text=f"Subject: {meeting['subject']}", font=("Arial", 14)).pack(pady=5)
    Label(win, text=f"Starts at: {meeting['start']}", font=("Arial", 12)).pack(pady=2)
    Label(win, text=f"Account: {meeting['account']}", font=("Arial", 10)).pack(pady=2)

    Button(win, text="Snooze 5 min", command=snooze, width=15).pack(pady=5)
    Button(win, text="Dismiss", command=dismiss, width=15).pack(pady=5)

    threading.Thread(target=play_ringtone).start()
    win.mainloop()