from django.db import models
from model_utils import FieldTracker
from model_utils.models import TimeStampedModel
import httpx

class Product(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.title
    
    def sync(self):
        res = httpx.get("https://httpbin.org/uuid")
        if res.status_code == 200:
            zproduct = ZProduct.objects.create(id=res.json()["uuid"], product=self)
            zproduct.save()

class ZProduct(TimeStampedModel):
    id = models.UUIDField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    data = models.JSONField(null=True)
    tracker = FieldTracker(fields=['data'])

    def __str__(self):
        return self.product.title
