from django.contrib import admin
from django.urls import path, include
from .views import *

app_name = 'lichsu'

urlpatterns = [
    path('<int:id>/', get_ds_lichsu, name='lichsu-land'),
    path('api/sensor-data/<int:land_id>/', get_sensor_data, name='get_sensor_data'),
]