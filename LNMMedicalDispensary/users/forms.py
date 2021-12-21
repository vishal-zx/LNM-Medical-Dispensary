from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db.models.base import Model
from .models import MedicineIssued, User
from .models import Medicine
from django.forms import ModelForm  

class LoginForm(forms.Form):
    username = forms.CharField(
        widget= forms.TextInput(
            attrs={
                "class": "form-control"
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control"
            }
        )
    )


class SignUpForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            }
        )
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control"
            }
        )
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control"
            }
        )
    )
    email = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            }
        )
    )
    
    patient=forms.BooleanField(initial=True)
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'gender', 'age', 'is_doctor', 'patient', 'is_chemist')

class MedicineForm(ModelForm):
    class Meta:
        model = Medicine
        fields = ('Mid',)

class MedicineInstance(ModelForm):
    class Meta:
        model = Medicine
        fields = '__all__'

class IssueMedicineForm(ModelForm):
    class Meta:
        model = MedicineIssued
        fields = '__all__'

# class ChemistForm(ModelForm):
#     class Meta:
#         model = Chemist
#         fileds = '__all__'
# class IssueMedicineForm(forms.Form):
#     patientID = forms.IntegerField()
#     medicineID = forms.IntegerField()
#     quantity = forms.IntegerField()
#     prescription = forms.TextField(max_length = 200)
#     date = forms.DateTimeField(default=datetime.now(), blank=True)