from celery import shared_task

from accounts.email import ConfirmEmailUserSender


@shared_task()
def test_a_b(a, b):
    print('TASK test_a_b(a,b)=', a, b)
    return a + b


@shared_task(ignore_result=True)
def send_register_email_tasks(request, user) -> None:
    """Отправка сообщения на почту для ее подтверждения"""
    email = ConfirmEmailUserSender(request, user).send_mail()
    print(f' TASK: "send_register_email_tasks" domain: {email._get_domain()}, user: {user.username}')
