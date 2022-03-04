from djongo import models


class ProductImage(models.Model):
    id = models.IntegerField(primary_key=True)
    url = models.CharField(max_length=400)


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

# class Category(models.Model):
#     name = models.CharField(max_length=50)
#
#     class Meta:
#         verbose_name_plural = "categories"
#
#     def __str__(self):
#         return self.name
