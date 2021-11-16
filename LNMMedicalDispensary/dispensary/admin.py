from django.contrib import admin

from LNMMedicalDispensary.dispensary.apps import DispensaryConfig
from LNMMedicalDispensary.dispensary.models import Patient

# Register your models here.
admin.site.register(Patient)
