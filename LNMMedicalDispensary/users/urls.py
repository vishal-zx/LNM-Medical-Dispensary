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

    path('viewPatientHistory/', views.viewPatientHistory, name='viewPatientHistory'),

    path('feedback/', views.feedback, name='feedback'),
    path('patientProfile/', views.patientProfile, name='patientProfile'),
    path('bookAppointment/', views.bookAppointment, name='bookAppointment'),

    path('checkAppointment/', views.checkAppointment, name='checkAppointment'),

    path('Treatment/', views.Treatment, name='Treatment'),

]
