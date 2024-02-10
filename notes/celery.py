import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'notes.settings')
app = Celery('notes')

app.config_from_object('django.conf:settings', namespace='CELERY')
# namespace = 'CELERY' для того что бы в переменных в файле settings.py отбрасывалась часть с CELERY
# то есть CELERY_ЧТО-Что-то

app.autodiscover_tasks() # это для того что бы CELERY сам нашел задачи в файлах(приложениях).