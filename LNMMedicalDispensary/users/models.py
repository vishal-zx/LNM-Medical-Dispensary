from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    is_doctor= models.BooleanField('Is admin', default=False)
    is_patient = models.BooleanField('Is customer', default=False)
    is_chemist = models.BooleanField('Is employee', default=False)