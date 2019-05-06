import time
import logging
logger = logging.getLogger('dj')


'''
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events, register_job

scheduler = BackgroundScheduler()
scheduler.add_jobstore(DjangoJobStore(), "default")

@register_job(scheduler, "interval", seconds=1)
def test_job():
    time.sleep(4)
    logger.info("I'm a test job!")

register_events(scheduler)

#scheduler.start()
#print("Scheduler started!")
'''

import os,django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Polaris.settings")  # project_name 项目名称
django.setup()

from apscheduler.schedulers.blocking import BlockingScheduler
import threading

sched = BlockingScheduler(daemonic=False)
#scheduler.add_jobstore(DjangoJobStore(), "default")


def my_job():
    logger.info("I'm a test job!")
def do_something():
    sched.add_job(my_job, 'interval', seconds=5)
