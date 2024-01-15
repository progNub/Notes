import os

# Инициализация джанго
from django import setup

"""Run administrative tasks."""
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Notes.settings')  # взял эту строчку из файла manage.py
setup()

from posts.models import Note
from django.contrib.auth import get_user_model
from faker import Faker

User = get_user_model()
fake = Faker('ru-RU')


def create_users(limit):
    users: [User] = []
    User.objects.all().delete()
    for i in range(limit):
        user = User()
        user.username = fake.unique.user_name()
        user.first_name = fake.first_name()
        user.last_name = fake.last_name()
        user.email = fake.email()
        user.is_superuser = False
        user.is_staff = False
        user.password = fake.password()
        user.phone = fake.msisdn()
        users.append(user)
    User.objects.bulk_create(users)


def create_notes(max_limit):
    notes: [Note] = []
    users = User.objects.all()
    for user in users:
        count_notes = fake.pyint(0, max_limit, 1)
        for i in range(count_notes):
            note = Note()
            note.title = fake.text(max_nb_chars=50)
            note.content = fake.text(max_nb_chars=1000)
            note.autor = user
            note.created_at = fake.date_time(tzinfo=None)
            notes.append(note)
    Note.objects.bulk_create(notes)




if __name__ == '__main__':
    create_users(100)
    create_notes(10)
