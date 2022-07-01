from django.contrib.auth.models import AbstractUser
from djongo import models
# Create your models here.
from products.models import Product


class User(AbstractUser, models.Model):
    _id = models.ObjectIdField()
    phone = models.CharField(max_length=12)
    email = models.EmailField(unique=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    # objects = Manager()


class Wishlist(models.Model):
    _id = models.ObjectIdField()
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    products = models.ArrayReferenceField(Product)


class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reference = models.CharField(max_length=20)
    amount = models.FloatField()
    description = models.CharField(max_length=100)
    transaction_type = models.CharField(choices=[("dr", 'Debit'), ("cr", 'Credit')], max_length=2)
    created_at = models.DateTimeField(null=True)
    paid_at = models.DateTimeField(null=True)