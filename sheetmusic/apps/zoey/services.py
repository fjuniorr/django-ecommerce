import random
from .tasks import mail_admins, send_mail


def notify_admin():
    subject = "Hello Admin"
    message = f"Hello! Your lucky number is {random.randint(1, 100)}."
    mail_admins.delay(subject, message)


def notify(recipient):
    subject = "Hello Staff"
    message = f"Hello! Your lucky number is {random.randint(1, 100)}."
    send_mail.delay(subject, message, recipient)
