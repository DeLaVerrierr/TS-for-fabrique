from django.core.mail import send_mail
from django_q.models import Schedule
from django_q.tasks import schedule
from django.conf import settings
from .models import StatisticsNewletter


def send_statistics_email():
    statistics = StatisticsNewletter.objects.all()
    message = "Статистика отправленных сообщений:\n\n"
    for stat in statistics:
        message += str(stat) + "\n"

    subject = "Статистика отправленных сообщений"
    print('Letter sent')
    send_mail(subject, message, settings.EMAIL_HOST_USER, [settings.RECIPIENT_ADDRESS])

