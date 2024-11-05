# services.py

from django.core.mail import mail_admins
from django.conf import settings
import random


def send_hello_world_email():
    subject = "Hello World"
    message = f"Hello World! Your lucky number is {random.randint(1, 100)}."

    mail_admins(subject, message)
