from django.contrib import admin

# Register your models here.
from orders.models import Order

admin.site.register(Order)
