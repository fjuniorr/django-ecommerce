from django.urls import path
from . import views

urlpatterns = [
    path('sync/<int:product_id>/', views.sync_product_view, name='sync_product_view_name'),
]
