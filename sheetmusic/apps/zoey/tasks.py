from celery import shared_task
from django.core.mail import mail_admins as django_mail_admins
from django.core.mail import send_mail as django_send_mail
from .models import Product


@shared_task
def sync_product(product_id):
    product = Product.objects.get(id=product_id)
    product.sync()


@shared_task(name="core.tasks.mail_admins")
def mail_admins(subject: str, message: str, html_message=None, **kwargs):
    """Allow mail_managers to go through celery."""
    django_mail_admins(
        subject=subject, message=message, html_message=html_message, **kwargs
    )


@shared_task(name="core.tasks.mail")
def send_mail(
    subject: str, message: str, recipient_list=None, html_message=None, **kwargs
):
    """Allow mail_managers to go through celery."""
    django_send_mail(
        subject=subject,
        message=message,
        recipient_list=recipient_list,
        html_message=html_message,
        **kwargs
    )


@shared_task(name="notification.service")
def notification():
    from .services import notify_admin

    notify_admin()
