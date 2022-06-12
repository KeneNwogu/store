from django import forms
from djongo import models


class ProductImage(models.Model):
    id = models.IntegerField(primary_key=True)
    urls = models.CharField(max_length=400)


class Product(models.Model):
    _id = models.ObjectIdField()
    name = models.CharField(max_length=100)
    brand = models.CharField(max_length=20)
    currency = models.CharField(max_length=3)
    price = models.IntegerField()
    in_stock = models.BooleanField()
    description = models.TextField(null=False, default='No details for this product')
    images = models.JSONField()
    gender = models.CharField(max_length=15)

    class MongoMeta:
        db_table = "products"


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['_id']

