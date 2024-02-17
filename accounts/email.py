from django.contrib.auth.models import AbstractUser
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode


class BaseEmailSender:
    template_name = None
    subject = None
    user_id_field = "pk"

    def __init__(self, domain, user: AbstractUser, token: str = ''):
        self._domain = domain
        self._user = user
        self.__token = token

    def get_template_name(self) -> str:
        if self.template_name is None:
            raise NotImplemented("Вы должны указать имя шаблона в атрибуте класса")
        return self.template_name

    def get_subject(self) -> str:
        if self.subject is None:
            raise NotImplemented("Укажите тему письма в атрибуте класса")
        return self.subject

    def send_mail(self):
        mail = EmailMultiAlternatives(
            subject=self.get_subject() + " на сайте " + self._get_domain(),
            to=[self._user.email]
        )
        mail.attach_alternative(self._get_mail_body(), "text/html")
        mail.send()

    def _get_mail_body(self) -> str:
        context = {
            "user": self._user,
            "domain": self._get_domain(),
            "uidb64": self._get_user_base64(),
            "token": self._get_token(),
        }
        return render_to_string(self.get_template_name(), context)

    def _get_domain(self) -> str:
        return self._domain

    def _get_token(self) -> str:
        if self.__token == '':
            self.__token = default_token_generator.make_token(self._user)
        return self.__token

    def _get_user_base64(self) -> str:
        """Кодируем идентификационное поле пользователя, указанное в атрибуте класса"""
        return urlsafe_base64_encode(
            force_bytes(str(getattr(self._user, self.user_id_field)))
        )


class ConfirmUserResetPasswordEmailSender(BaseEmailSender):
    template_name = "reset_password.html"
    user_id_field = "id"
    subject = "Сброс пароля"


class ConfirmEmailUserSender(BaseEmailSender):
    template_name = "register_confirm_email.html"
    user_id_field = "id"
    subject = "Подтверждение почты"
