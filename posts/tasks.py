from celery import shared_task


@shared_task()
def home_page_task(string: str) -> str:
    print(f'hello {string}')
    return 'OK'
