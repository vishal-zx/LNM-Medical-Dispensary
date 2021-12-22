from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login_view'),
    path('register/', views.register, name='register'),
    path('doctor/', views.doctor, name='doctor'),
    path('chemist/', views.chemist, name='chemist'),
    path('patient/', views.patient, name='patient'),
    
    path('patientHistory/', views.patientHistory, name='patientHistory'),
    path('viewPatientHistory/', views.viewPatientHistory,
         name='viewPatientHistory'),
    path('feedback/', views.feedback, name='feedback'),
    path('patientProfile/', views.patientProfile, name='patientProfile'),
    path('bookAppointment/', views.bookAppointment, name='bookAppointment'),
    path('RequestAppointment/', views.RequestAppointment, name='RequestAppointment'),
    path('UpdatepatientProfile/', views.updatepatient, name='UpdatepatientProfile'),
    path('checkAppointment/', views.checkAppointment, name='checkAppointment'),
    path('MedicalCertificate/', views.MedicalCertificateFunction, name='MedicalCertificate'),
    path('Treatment/', views.Treatment, name='Treatment'),
    path('DoctorProfile/', views.DoctorProfile, name='DoctorProfile'),
    path('ChemistProfile/', views.ChemistProfile, name='ChemistProfile'),
    path('checkMedicine/', views.checkMedicine, name='checkMedicine'),
    path('updateMedicine/<str:pk>/', views.updateMedicine, name='updateMedicine'),
    path('MedicineRecord/', views.MedicineRecord, name='MedicineRecord'),
    path('issueMedicine/', views.issueMedicine, name='issueMedicine'),
]
