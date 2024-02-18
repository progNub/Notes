from celery import shared_task
from django.contrib.auth import get_user_model

from accounts.email import ConfirmEmailUserSender

User = get_user_model()




@shared_task(ignore_result=True)
def send_register_email_tasks(domain, user_id, token='') -> None:
    """Отправка сообщения на почту для ее подтверждения"""
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        print(f' TASK: "send_register_email_tasks" id: {user_id}, User.DoesNotExist')
    else:
        ConfirmEmailUserSender(domain, user, token).send_mail()
