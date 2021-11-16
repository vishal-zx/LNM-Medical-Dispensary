from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    is_doctor= models.BooleanField('Is doctor', default=False)
    patient = models.BooleanField('Is patient', default=False)
    is_chemist = models.BooleanField('Is chemist', default=False)
    
    
class Patient(models.Model):
    pid = models.IntegerField(primary_key=True)
    pname = models.CharField(max_length=20)
