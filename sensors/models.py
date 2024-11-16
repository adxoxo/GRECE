from django.db import models
from django.utils import timezone 
# Create your models here.

class HydroponicSystem(models.Model):
    name = models.CharField(max_length=200, null=True)

    def __str__(self):
        return f"{self.name}"

class HydroponicParameters(models.Model):
    System = models.ForeignKey(HydroponicSystem, on_delete=models.CASCADE)
    Water_level = models.FloatField(null=True)
    EC = models.FloatField(null=True)
    PH = models.FloatField(null=True)
    Temp = models.FloatField(null=True)
    Humid = models.FloatField(null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f"{self.System}"

class HydroponicActions(models.Model):
    LightStatus = models.BooleanField(null=True)
    PumpStatus = models.BooleanField(null=True)


