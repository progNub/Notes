from celery import shared_task
from django.contrib.auth import get_user_model

from accounts.email import ConfirmEmailUserSender

User = get_user_model()


@shared_task()
def test_a_b(a, b):
    print('TASK test_a_b(a,b)=', a, b)
    return a + b


@shared_task(ignore_result=True)
def send_register_email_tasks(domain, user_id) -> None:
    """Отправка сообщения на почту для ее подтверждения"""
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        print(f' TASK: "send_register_email_tasks" id: {user_id} DoesNotExist')
        ConfirmEmailUserSender(domain, user).send_mail()
    else:
        ConfirmEmailUserSender(domain, user).send_mail()
        print(f' TASK: "send_register_email_tasks" domain: {domain}, user: {user.username}')
