from django.contrib import admin
from .models import InboundEvent, InboundFile, Customer, Order, OrderLine

admin.site.register([InboundEvent, InboundFile, Customer, Order, OrderLine])
