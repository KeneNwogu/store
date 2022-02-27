from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    stock = models.IntegerField(null=False, default=1)
    sold_out = models.BooleanField(null=False, default=False)
    details = models.TextField(null=False, default='No details for this product')
    product_image = models.CharField(max_length=100, null=False, default='default.jpg')
    category_id = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='category')

    def __str__(self):
        return self.name
    
    
class Category(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name
