# services.py

from django.core.mail import send_mail
from django.conf import settings
import random


def send_hello_world_email(to_email):
    subject = "Hello World"
    message = f"Hello World! Your lucky number is {random.randint(1, 100)}."
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [to_email]

    send_mail(subject, message, from_email, recipient_list)
