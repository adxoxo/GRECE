from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import HydroponicSystem, HydroponicParameters

class HydroponicSystemSerializer(ModelSerializer):
    class Meta:
        model = HydroponicSystem
        fields = '__all__'

class HydroponicParametersSerializer(ModelSerializer):
    class Meta:
        model = HydroponicParameters
        fields = '__all__'