from django.db import models

# Create your models here.


class Patient(models.Model):
    pid = models.IntegerField(primary_key=True)
    pname = models.CharField(max_length=20)
