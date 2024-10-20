from celery import shared_task
from .models import Product

@shared_task
def sync_product(product_id):
    product = Product.objects.get(id=product_id)
    product.sync()
