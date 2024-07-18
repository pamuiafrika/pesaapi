# myapp/scheduler.py
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from django.utils import autoreload
from . import tasks

scheduler = BackgroundScheduler()

def start_scheduler():
    scheduler.add_job(
        tasks.update_all_stocks,
        trigger=IntervalTrigger(minutes=1),
        id='update_all_stocks',
        name='Update stock data every minute',
        replace_existing=True
    )
    scheduler.start()
    print("Scheduler started")

    # Shut down the scheduler when Django autoreload or exit
    autoreload.run_with_reloader(stop_scheduler)

def stop_scheduler():
    scheduler.shutdown(wait=False)



