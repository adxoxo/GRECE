from django.shortcuts import render
from rest_framework import serializers
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response 
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
from .models import HydroponicParameters
from .serializers import HydroponicSystemSerializer, HydroponicParametersSerializer

class HydroponicsDataView(ViewSet):

    def HydroponicsDataList(self, request):

        data = HydroponicParameters.objects.all()
        serializer = HydroponicParametersSerializer(data, many=True)

        return Response(serializer.data, status=200)

    def HydroponicsAcquire(self, request):

        serializer = HydroponicParametersSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        else:
            return Response(serializer.data, status=400)


