from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime


def test_scheduler():
    print("-------test-scheduler------")

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(test_scheduler, 'interval', seconds=10)
    scheduler.start()

