import datetime
import os

from django.http import HttpRequest
from django.conf import settings


# 3. * Создать и подключить middleware, который будет сохранять в файл
# usersActivity.log строку для каждого пользователя о посещенном им URL
# и время. Формат записи:
# 01.27.2024 10:42 | username | URL=/notes
# Чтобы получить URL запроса нужно использовать:
# request.get_full_path()
class ActivityUserLog:
    FILE_NAME = 'usersActivity.log'
    FILE_PATH = os.path.join(settings.BASE_DIR,FILE_NAME)

    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request: HttpRequest):
        response = self.get_response(request)
        date = datetime.datetime.now().strftime("%m.%d.%Y %H:%M")
        username = request.user
        url = request.get_full_path()
        line = f'{date} | {username} | {url}\n'
        with open(file=ActivityUserLog.FILE_PATH, mode='a', encoding='utf-8') as file:
            file.write(line)
        # Code to be executed for each request/response after
        # the view is called.
        return response
