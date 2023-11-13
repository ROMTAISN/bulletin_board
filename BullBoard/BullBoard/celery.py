import os
from celery import Celery
from celery.schedules import crontab


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'BullBoard.settings')

app = Celery('BullBoard')
app.config_from_object('django.conf.settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'send_post_every_week': {
        'task': 'board.tasks.send_message_every_week',
        'schedule': crontab(hour=18, minute=10, day_of_week='sunday'),
    },
}
