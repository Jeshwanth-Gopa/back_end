from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import json, time
from notify import show_popup

with open("alarm/config.json") as f:
    config = json.load(f)

meetings = config["meetings"]

def add_jobs(scheduler, meetings):
    for meeting in meetings:
        ring_at = datetime.fromisoformat(meeting["ring_at"])
        scheduler.add_job(show_popup, 'date', run_date=ring_at, id=str(meeting["id"]), args=[meeting])
        print(f"Scheduled to run at: {ring_at}")

scheduler = BackgroundScheduler()

add_jobs(scheduler, meetings)
jobs = scheduler.get_jobs()
for job in jobs:
    print(job, job.id)
    
scheduler.start()
print("Scheduler started")

try:
    while True:
        time.sleep(1)
except (KeyboardInterrupt, SystemExit):
    scheduler.shutdown()
    print("Scheduler shut down")