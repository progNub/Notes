from django.contrib.auth import get_user_model
from django.core.validators import EmailValidator

from django.db.models import Q
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.core.handlers.wsgi import WSGIRequest
from django.contrib.auth import login, logout

from accounts.models import User
from posts.models import Note, Tag


# User = get_user_model()


# Create your views here.

def authentication_view(request: WSGIRequest):
    return render(request, 'authentication.html')


def registration_view(request: WSGIRequest):
    if request.method == 'GET':
        return render(request, "registration.html")
    elif request.method == 'POST':
        data: dict = request.POST.dict()
        data['errors'] = []

        if data['username'] and data['email'] and data['password1'] and data['password2']:

            if User.objects.filter(Q(username=data['username']) | Q(email=data['email'])).count() > 0:
                data['errors'].append('*Такой username или email уже существует.')

            if data['password1'] != data['password2']:
                data['errors'].append('*Пароли не совпадают.')

        else:
            data['errors'].append('*Все поля должны быть заполнены.')
        if not (data['errors']):
            user = User(username=data['username'], email=data['email'])
            user.set_password(data['password1'])
            user.save()

            login(request, user)
            return redirect('home')

        return render(request, 'registration.html', context=data)


def user_login(request: WSGIRequest):
    if request.method == 'GET':
        return render(request, 'login.html', )
    elif request.method == 'POST':
        data: dict = request.POST.dict()
        data['errors'] = []

        if User.objects.filter(username=data['username']).exists():
            user: User = User.objects.get(username=data['username'])
            if user.check_password(data['password']):
                login(request, user)
                return redirect('home')
            else:
                data['errors'].append('Неправильный логин или пароль')
        return render(request, 'login.html', context=data)


def user_logout(request: WSGIRequest):
    logout(request)
    return redirect('home')


def user_profile(request: WSGIRequest, username):
    user = get_object_or_404(User, username=username)
    notes = user.notes.select_related('autor')
    tags = Tag.objects.filter(notes__autor=user)

    if request.method == 'GET':
        return render(request, "user_profile.html", context={'user': user, 'notes': notes, 'tags': tags})


def edit_user_profile(request: WSGIRequest, username):
    user = get_object_or_404(User, username=username)
    if request.user.id != user.id:
        return HttpResponseForbidden('Нет прав')
    if request.method == 'GET':
        return render(request, "edit_user_profile.html", context={'user': user})
    if request.method == 'POST':
        data = request.POST
        errors = []

        # ---------- check --------------- username ----------- check --------------
        if data['username'] != user.username and User.objects.filter(username=data['username']):
            errors.append('Такое имя пользователя уже существует.')

        # ---------- check --------------- email ----------- check --------------
        if data['email'] != user.email and User.objects.filter(email=data['email']):
            errors.append('Email уже существует.')

        if not errors:
            user.username = data['username']
            user.first_name = data['first_name']
            user.last_name = data['last_name']
            user.email = data['email']
            user.phone = data['phone']
            user.save()
            message = 'Данные успешно изменены'
            request.user = user
            return render(request, "user_profile.html", context={'user': user, 'message': message})

        else:
            return render(request, "edit_user_profile.html", context={'user': user, 'errors': errors})


def edit_user_password(request: WSGIRequest, username):
    user = get_object_or_404(User, username=username)
    if request.user.id != user.id:
        return HttpResponseForbidden('Нет прав')
    if request.method == 'GET':
        return render(request, "edit_password.html")

    if request.method == 'POST':
        old_password = request.POST['old_password']
        new_password = request.POST['new_password']
        errors = []
        # ---------- check --------------- password ----------- check --------------
        if user.check_password(old_password):
            if new_password == '':
                errors.append('Новый пароль не может быть пустым полем')
        else:
            errors.append('Не верный пароль.')

        if not errors:
            user.set_password(new_password)
            user.save()
            return redirect('login')

        return render(request, "edit_password.html", context={'user': user, 'errors': errors})
