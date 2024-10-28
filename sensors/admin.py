from django.contrib import admin
from .models import HydroponicParameters, HydroponicSystem
# Register your models here.

admin.site.register(HydroponicParameters)
admin.site.register(HydroponicSystem)