from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import *
from .serializers import *
import json
from rest_framework import viewsets

#add id to the parameter
def get_ds_lichsu(request, id):
    ds_lichsu = LichSuCamBien.objects.filter(manhdat__id=id)[:30]
    return render(request, 'lichsu/lichsu.html', {
        'ds_lichsu': ds_lichsu,
        'land_id': id,
    })

def get_sensor_data(request, land_id):
    lichsu = LichSuCamBien.objects.filter(manhdat__id=land_id).order_by('-created_at')[:30]
    data = LichSuCamBienSerializer(lichsu, many=True).data
    return JsonResponse(data)
