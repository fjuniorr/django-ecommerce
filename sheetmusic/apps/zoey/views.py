from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .models import Product
from .tasks import sync_product

def sync_product_view(req, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    # Trigger the Celery task
    task = sync_product.delay(product_id)
    
    return JsonResponse({
        "message": f"Sync task for product '{product.title}' (ID: {product_id}) has been triggered.",
        "task_id": task.id
    })
