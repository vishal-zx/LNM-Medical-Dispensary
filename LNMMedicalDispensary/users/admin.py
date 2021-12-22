from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(User)
admin.site.register(Patient)
admin.site.register(Doctor)
admin.site.register(Chemist)
admin.site.register(Appointment)
admin.site.register(PatientHistory)
admin.site.register(Medicine)
admin.site.register(MedicineIssued)
admin.site.register(Medicalcertificate)
admin.site.register(Feedback)
