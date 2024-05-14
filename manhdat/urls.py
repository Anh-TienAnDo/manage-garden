from django.urls import path
from .views import *

urlpatterns = [
    path('', lands, name='lands'),
    path('land/<int:id>', land_details, name='land-details'),
]
