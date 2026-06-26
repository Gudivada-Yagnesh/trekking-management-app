from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime


def archive_completed_treks():

    print(
        f"[SCHEDULER] Running cleanup at {datetime.now()}"
    )


def start_scheduler():

    scheduler = BackgroundScheduler()

    # Every 12 hours
    scheduler.add_job(
        archive_completed_treks,
        'interval',
        hours=12
    )

    scheduler.start()

    print("Scheduler started")
