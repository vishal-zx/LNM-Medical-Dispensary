from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.deletion import CASCADE

# Create your models here.


class User(AbstractUser):
    GENDERCHOICE = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    age = models.IntegerField(null=False, default=20)
    gender = models.CharField(
        max_length=1,
        choices=GENDERCHOICE,
        default='M',
    )
    is_doctor = models.BooleanField('Is doctor', default=False)
    patient = models.BooleanField('Is patient', default=False)
    is_chemist = models.BooleanField('Is chemist', default=False)


class Patient(models.Model):
    GENDERCHOICE = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    Pid = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=20, null=False)
    age = models.IntegerField(null=False)
    gender = models.CharField(
        max_length=1,
        choices=GENDERCHOICE,
        default='M',
    )


class Doctor(models.Model):
    GENDERCHOICE = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    Did = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=20, null=False)
    age = models.IntegerField(null=False)
    gender = models.CharField(
        max_length=1,
        choices=GENDERCHOICE,
        default='M',
    )
    address = models.TextField()
    schedule = models.TextField(null=False)
    speciality = models.CharField(max_length=20)
    phonenumber = models.BigIntegerField()


class Chemist(models.Model):
    GENDERCHOICE = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    Cid = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=20, null=False)
    age = models.IntegerField(null=False)
    gender = models.CharField(
        max_length=1,
        choices=GENDERCHOICE,
        default='M',
    )
    
class Appointment(models.Model):
    Aid =models.IntegerField(primary_key=True)
    Pid=models.ForeignKey(Patient,on_delete=CASCADE)
    Did=models.ForeignKey(Doctor,on_delete=CASCADE)
    Timings=models.CharField(max_length=20)
    mailid=models.CharField(max_length=20)
    isApproved= models.BooleanField('IsApproved', default=False)
    
    
