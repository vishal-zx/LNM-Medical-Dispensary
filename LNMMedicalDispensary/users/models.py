from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.deletion import CASCADE
import datetime 

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
    uid = models.IntegerField(null=False, default=20)
 


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
    def __str__(self):
        # template = '{self}'
        # return self.name, self.Pid
        return 'id : {} Name : {}'.format(self.Pid, self.name)

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
    isApproved= models.BooleanField('IsApproved', default=True)
    
class PatientHistory(models.Model):
    Aid=models.ForeignKey(Appointment,on_delete=CASCADE)
    Pid=models.ForeignKey(Patient,on_delete=CASCADE)
    Description=models.TextField()
    # def __str__(self):
    #     return str(self.Aid, self.Pid)

class Medicine(models.Model):
    Mid=models.IntegerField(primary_key=True)
    Name=models.CharField(max_length=50, null=False)
    Type=models.CharField(max_length=50, null=False)
    Quantity=models.IntegerField(default=1000)
    Usage=models.IntegerField(default=0)
    Supplier=models.CharField(max_length=30)
    PurchaseDate=models.DateField(("Date"),default=datetime.date.today)
    ExpiryDate=models.DateField()

    def __str__(self):
        return 'id : {} Name : {}'.format(self.Mid, self.Name)



    
class MedicineIssued(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.SET_NULL, null=True)
    medicine = models.ForeignKey(Medicine, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField()
    prescription = models.TextField()
    date = models.DateField(("Date"),default=datetime.date.today)


