from celery import shared_task
import time

from django.core.mail import send_mail


@shared_task()
def hello():
    time.sleep(10)
    print("Hello World!!!")


@shared_task()
def printer():
    send_mail(
        subject=f"Новости за неделю",
        message=f"Здравствуй."
                f" Новые новости в твоём любимом разделе! ",
        from_email='vas3011ds@yandex.ru',
        recipient_list=['d3011ss@yandex.ru']
    )

