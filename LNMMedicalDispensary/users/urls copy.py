from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name= 'index'),
    path('login/', views.login_view, name='login_view'),
    path('register/', views.register, name='register'),
    path('doctor/', views.doctor, name='doctor'),
    path('chemist/', views.chemist, name='chemist'),
    path('patient/', views.patient, name='patient'),
    path('scheduleTest/', views.scheduleTest, name='scheduleTest'),
    path('patientHistory/', views.patientHistory, name='patientHistory'),
]
