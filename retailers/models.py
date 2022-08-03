from djongo import models
from users.models import User
from utilities.utils import generate_unique_state_identifier


class Retailer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    access_token = models.TextField(null=True)
    refresh_token = models.TextField(null=True)
    state_identifier = models.CharField(null=True, max_length=600, default=generate_unique_state_identifier)