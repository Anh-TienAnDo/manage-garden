# file dieukhien/urls.py
from django.contrib import admin
from django.urls import path, include
from .views import *

app_name = 'dieukhien'

urlpatterns = [
    # path('', get_home, name='home'),
    path('<int:id>/', dieu_khien, name='dieukhien'),
    path('update-lamp/<int:id>/', updateLamp, name='update-lamp'),
    path('update-pump/<int:id>/', updatePump, name='update-pump'),
    path('update-fan/<int:id>/', updateFan, name='update-fan'),
    path('update-roof/<int:id>/', updateRoof, name='update-roof'),
]