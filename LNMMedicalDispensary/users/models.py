from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.deletion import CASCADE
import datetime

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from django.contrib.auth.models import User
# from .models import Doctor, Chemist

import uuid
from uuid import uuid4
# Create your models here.


def generateUUID():
    return str(uuid4())


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
    Uid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    phonenumber = models.BigIntegerField(null=True, blank=True)
    is_doctor = models.BooleanField('Is doctor', default=False)
    patient = models.BooleanField('Is patient', default=False)
    is_chemist = models.BooleanField('Is chemist', default=False)
    

class Patient(models.Model):
    GENDERCHOICE = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    Pid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20, null=False)
    age = models.IntegerField(null=False)
    phonenumber = models.BigIntegerField(null=True, blank=True)
    Uid = models.UUIDField(null=True, editable=False)
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
    # Uid = models.ForeignKey(User,on_delete=CASCADE, null=True)
    Uid = models.UUIDField(null=True, editable=False)
    Did = models.AutoField(primary_key=True)
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
    phonenumber = models.BigIntegerField(null=True, blank=True)

    def __str__(self):
        return 'Did : {} Name : {}'.format(self.Did, self.name)


class Chemist(models.Model):
    GENDERCHOICE = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    Uid = models.UUIDField(null=True, editable=False)
    # Uid = models.ForeignKey(User,on_delete=CASCADE, null=True)
    Cid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, null=False)
    age = models.IntegerField(null=False)
    phonenumber = models.BigIntegerField(null=True, blank=True)
    gender = models.CharField(
        max_length=1,
        choices=GENDERCHOICE,
        default='M',
    )

    def __str__(self):
        return 'Cid : {} Name : {}'.format(self.Cid, self.name)


class Appointment(models.Model):
    Aid = models.AutoField(primary_key=True)
    Pid = models.ForeignKey(Patient, on_delete=CASCADE)
    Did = models.ForeignKey(Doctor, on_delete=CASCADE)
    Timings = models.CharField(max_length=20)
    mailid = models.CharField(max_length=20)
    isApproved = models.BooleanField('IsApproved', default=True)


class PatientHistory(models.Model):
    Aid = models.ForeignKey(Appointment, on_delete=CASCADE)
    Pid = models.ForeignKey(Patient, on_delete=CASCADE)
    Description = models.TextField()
    # def __str__(self):
    #     return str(self.Aid, self.Pid)


class Medicine(models.Model):
    Mid = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=50, null=False)
    Type = models.CharField(max_length=50, null=False)
    Quantity = models.IntegerField(default=1000)
    Usage = models.IntegerField(default=0)
    Supplier = models.CharField(max_length=30)
    PurchaseDate = models.DateField(("Date"), default=datetime.date.today)
    ExpiryDate = models.DateField()

    def __str__(self):
        return 'id : {} Name : {}'.format(self.Mid, self.Name)


class MedicineIssued(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.SET_NULL, null=True)
    medicine = models.ForeignKey(
    Medicine, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField()
    prescription = models.TextField()
    date = models.DateField(("Date"), default=datetime.date.today)


class Medicalcertificate(models.Model):
    STATUSCHOICE = (
        ('P', 'Pending'),
        ('A', 'Approve'),
        ('R', 'Reject'),
    )
    patient = models.ForeignKey(Patient, on_delete=CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=CASCADE)
    medicalID = models.AutoField(primary_key=True)
    reason = models.TextField()
    fromdate = models.DateField(("Date"), default=datetime.date.today)
    todate = models.DateField(("Date"), default=datetime.date.today)
    status =models.CharField(
        max_length=1,
        choices=STATUSCHOICE,
        default='P',
    )

class Feedback(models.Model):
    feedbackID = models.AutoField(primary_key=True)
    patient = models.ForeignKey(Patient, on_delete=models.SET_NULL, null=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True)
    feedback = models.TextField()


def createDocChem(sender, instance, created, **kwargs):
    user = instance
    print('Signal Triggered')
    if created:
        print('Created')
        if user.is_doctor:
            print('Doctor')
            doctor = Doctor.objects.create(
                # user = user,
                # username = user.username,
                Uid=user.Uid,
                age=user.age,
                name=user.first_name + ' ' + user.last_name,
                gender=user.gender,
                phonenumber=user.phonenumber,
            )
            doctor.save()
        if user.is_chemist:
            print('Chemist')
            chemist = Chemist.objects.create(
                Uid=user.Uid,
                name=user.first_name + ' ' + user.last_name,
                age=user.age,
                gender=user.gender,
                phonenumber=user.phonenumber,
            )
            chemist.save()
        if user.patient:
            print('Patient')
            patient = Patient.objects.create(
                Uid=user.Uid,
                name=user.first_name + ' ' + user.last_name,
                age=user.age,
                gender=user.gender,
                phonenumber=user.phonenumber,
            )
            patient.save()

    else:
        # user = instance
        print('Not created')
        ui = user.Uid
        if user.is_doctor:
            print('Doctor')
            try:
                doctor = Doctor.objects.get(
                    # Uid = user.Uid
                    Uid=ui
                )
            except Doctor.DoesNotExist:
                doctor = None

            if doctor is not None:
                doctor.name = user.first_name + ' ' + user.last_name
                doctor.age = user.age
                doctor.gender = user.gender
                doctor.save()
            else:
                doctor = Doctor.objects.create(
                    # user = user,
                    # username = user.username,
                    Uid=user.Uid,
                    age=user.age,
                    name=user.first_name + ' ' + user.last_name,
                    gender=user.gender,
                    phonenumber=user.phonenumber,
                )
                doctor.save()
        if user.is_chemist:
            print('Chemist')
            print('HI')
            try:
                chemist = Chemist.objects.get(
                    Uid=user.Uid
                )
            except Chemist.DoesNotExist:
                chemist = None
            print('BYE')
            print(chemist)
            if chemist is not None:
                chemist.name = user.first_name + ' ' + user.last_name
                chemist.age = user.age
                chemist.gender = user.gender
                chemist.save()
            else:
                chemist = Chemist.objects.create(
                    Uid=user.Uid,
                    name=user.first_name + ' ' + user.last_name,
                    age=user.age,
                    gender=user.gender,
                    phonenumber=user.phonenumber,
                )
                chemist.save()

        if user.patient:
            print('Patient')
            try:
                patient = Patient.objects.get(
                    Uid=user.Uid
                )
            except Patient.DoesNotExist:
                patient = None
            if patient is not None:
                patient.name = user.first_name + ' ' + user.last_name
                patient.age = user.age
                patient.gender = user.gender
                patient.phonenumber = user.phonenumber
                patient.save()
            else:
                patient = Patient.objects.create(
                    Uid=user.Uid,
                    name=user.first_name + ' ' + user.last_name,
                    age=user.age,
                    gender=user.gender,
                    phonenumber=user.phonenumber,
                )
                patient.save()


def deleteUser(sender, instance, **kwargs):
    user = User.objects.get(Uid=instance.Uid)
    user.delete()

# def deleteChemUser(sender, instance, **kwargs):
#     user = instance.Chemist
#     user.delete()


post_save.connect(createDocChem, sender=User,
                  dispatch_uid="create_DocChem_instance")

post_delete.connect(deleteUser, sender=Doctor)
post_delete.connect(deleteUser, sender=Chemist)
post_delete.connect(deleteUser, sender=Patient)
