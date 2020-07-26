from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class User(AbstractUser):
    user_types = (
        (1, "Seller"),
        (2, "Buyer")
    )
    user_type = models.IntegerField(
        choices=user_types, default=1, blank=False, null=False)
