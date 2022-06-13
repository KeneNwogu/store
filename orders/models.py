from datetime import datetime

from djongo import models

# Create your models here.
from products.models import Product, ProductForm
from users.models import User


class OrderItem(models.Model):
    # product_id = models.ObjectIdField(Product, primary_key=False, auto_created=False)
    # order_id = models.ObjectIdField('Order', primary_key=False, auto_created=False)
    _id = models.ObjectIdField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.FloatField()
    total = models.FloatField()

    # class Meta:
    #     abstract = True


class Order(models.Model):
    _id = models.ObjectIdField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ArrayReferenceField(OrderItem, on_delete=models.CASCADE)
    total_items = models.IntegerField()
    total_price = models.FloatField()
    created_at = models.DateTimeField(default=datetime.utcnow)
    processed_at = models.DateTimeField(null=True)



