import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NewsPaper.settings')

app = Celery('NewsPaper')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.beat_schedule = {
    'hello_every_30_sec': {
        'task': 'news.tasks.printer',
        'schedule': crontab(hour=8, minute=0, day_of_week='monday'),
        #'args': (5,),
    },
}

app.autodiscover_tasks()