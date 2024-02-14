from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.core.validators import EmailValidator

from django.db.models import Q
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.core.handlers.wsgi import WSGIRequest
from django.contrib.auth import login, logout
from django.urls import reverse_lazy, reverse
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.views.generic import CreateView

from accounts.email import ConfirmUserResetPasswordEmailSender, ConfirmEmailUserSender
from accounts.forms import UserRegisterForm
from posts.models import Note, Tag
from tasks import send_register_email_tasks

User = get_user_model()


# Create your views here.

def authentication_view(request: WSGIRequest):
    return render(request, 'authentication.html')


class RegisterUser(CreateView):
    form_class = UserRegisterForm
    template_name = 'registration.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        response = super().form_valid(form)
        self.object.is_active = False
        self.object.save()
        #   тут отправка письма c помощью Celery
        send_register_email_tasks.delay(request=self.request, user=self.object)
        #   тут отправка письма c помощью Celery
        return response

    @staticmethod
    def confirm_email(request, uidb64: str, token: str):
        user_id = force_str(urlsafe_base64_decode(uidb64))
        user = get_object_or_404(User, pk=user_id)
        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            login(request, user)
            return redirect('home')
        else:
            return redirect('home')


def user_login(request: WSGIRequest):
    if request.method == 'GET':
        return render(request, 'login.html', )
    elif request.method == 'POST':
        data: dict = request.POST.dict()
        data['errors'] = []
        if User.objects.filter(username=data['username']).exists():
            user: User = User.objects.get(username=data['username'])
            if not user.is_active:
                data['errors'].append('Учетная запись не активна.')
                return render(request, 'login.html', context=data)

            if user.check_password(data['password']):
                login(request, user)
                return redirect('home')
            else:
                data['errors'].append('Неправильный логин или пароль')
        return render(request, 'login.html', context=data)


def user_logout(request: WSGIRequest):
    logout(request)
    return redirect('home')


def user_profile(request, username):
    context = {
        'user': get_object_or_404(User, username=username),
        'notes': Note.objects.filter(autor__username=username).prefetch_related('tags'),
        'message': request.GET.get('message', '')
    }

    if request.method == 'GET':
        return render(request, "user_profile.html", context=context)


@login_required
def edit_user_profile(request: WSGIRequest, username, ):
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


@login_required
def reset_password(request, user_id):
    if str(request.user.id) != str(user_id):
        return HttpResponseForbidden('Нет прав')

    ConfirmUserResetPasswordEmailSender(request, request.user).send_mail()

    message = f'На почту {request.user.email} было отправлено письмо с инструкцией'
    return redirect(reverse('profile', args=[request.user.username]) + f'?message={message}')


def get_page_edit_password(request: WSGIRequest, uidb64: str, token: str):
    user_id = force_str(urlsafe_base64_decode(uidb64))
    user = get_object_or_404(User, pk=user_id)
    if default_token_generator.check_token(user, token):
        return redirect('edit-password', user.username)
    return redirect('home')


@login_required
def edit_user_password(request: WSGIRequest, username):
    if request.method == 'GET':
        return render(request, "edit_password.html")

    errors = []
    user = get_object_or_404(User, username=username)
    if request.user.id != user.id:
        return HttpResponseForbidden('Нет прав')

    if request.method == 'POST':
        old_password = request.POST['old_password']
        new_password = request.POST['new_password']

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
