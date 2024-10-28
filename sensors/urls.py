from django.contrib import admin
from django.urls import path, include
from .views import HydroponicsDataView
urlpatterns = [
    path('general/', HydroponicsDataView.as_view({
        'get':'HydroponicsDataList',
        'post': 'HydroponicsAcquire'
    }))
]