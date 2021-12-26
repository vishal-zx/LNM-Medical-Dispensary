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
     path('UpdatedoctorProfile/', views.updatedoctor, name='UpdatedoctorProfile'),
    path('UpdatepatientProfile/', views.updatepatient, name='UpdatepatientProfile'),
    path('checkAppointment/', views.checkAppointment, name='checkAppointment'),
    path('MedicalCertificate/', views.MedicalCertificateFunction,name='MedicalCertificate'),
    path('viewMedicalCertificate/', views.viewMedicalCertificateFunction,name='viewMedicalCertificate'),
    path('Treatment/', views.Treatment, name='Treatment'),
    path('checkMedicalCertificateStatus/', views.checkMedicalCertificateStatus, name='checkMedicalCertificateStatus'),
    path('ViewFeedback/', views.ViewFeedback, name='ViewFeedback'),
    path('DoctorProfile/', views.DoctorProfile, name='DoctorProfile'),
    path('ChemistProfile/', views.ChemistProfile, name='ChemistProfile'),
    path('checkMedicine/', views.checkMedicine, name='checkMedicine'),
    path('addMedicine/', views.addMedicine, name='addMedicine'),
    path('updateMedicine/<str:pk>/', views.updateMedicine, name='updateMedicine'),
    path('MedicineRecord/', views.MedicineRecord, name='MedicineRecord'),
    path('issueMedicine/', views.issueMedicine, name='issueMedicine'),
    path('checkAppointmentStatus/', views.checkAppointmentStatus, name='checkAppointmentStatus'),
]
