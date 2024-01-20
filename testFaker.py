import os
import random

# Инициализация джанго
from django import setup

"""Run administrative tasks."""
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Notes.settings')  # взял эту строчку из файла manage.py
setup()

from posts.models import Note, Tag
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
    user = User(username='admin', is_superuser=True, is_staff=True)
    user.set_password('admin')
    users.append(user)
    User.objects.bulk_create(users)


def create_tags(max_limit):
    tags: [Tag] = []
    Tag.objects.all().delete()
    for i in range(max_limit):
        tag = Tag()
        tag.name = fake.unique.word()
        tags.append(tag)
    Tag.objects.bulk_create(tags)


def create_notes(max_limit, limit_tags):
    notes = []
    users = User.objects.all()
    tags = Tag.objects.all()

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

    for note in notes:
        count_tags = fake.pyint(0, limit_tags, 1)
        temp_tags = random.sample(list(tags), count_tags)
        note.tags.set(temp_tags)


if __name__ == '__main__':
    create_users(50)
    create_tags(150)
    create_notes(10, 5)
