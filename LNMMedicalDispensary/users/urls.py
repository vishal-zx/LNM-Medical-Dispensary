from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login_view'),
    path('register/', views.register, name='register'),
    path('doctor/', views.doctor, name='doctor'),
    path('chemist/', views.chemist, name='chemist'),
    path('patient/', views.patient, name='patient'),
    path('scheduleTest/', views.scheduleTest, name='scheduleTest'),
    path('patientHistory/', views.patientHistory, name='patientHistory'),
<<<<<<< HEAD
    path('viewPatientHistory/', views.viewPatientHistory, name='viewPatientHistory'),
=======
    path('feedback/', views.feedback, name='feedback'),
    path('patientProfile/', views.patientProfile, name='patientProfile'),
<<<<<<< HEAD
    path('Treatment/', views.Treatment, name='Treatment'),
=======
>>>>>>> 1bd8fe30dd84a3fe18d284c5d2c9f192e4bd4b21
>>>>>>> 34f4c44c8ddae6af6a19876c4bb2dd9a4e58f806
]
