import json
from django.http import JsonResponse
from .mqtt import client as mqtt_client
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader


def publish_message(request):
    request_data = json.loads(request.body)
    rc, mid = mqtt_client.publish(request_data['topic'], request_data['msg'])
    return JsonResponse({'code': rc, 'request_data': request_data})

def home(request):
    template = loader.get_template('home.html')
    context = {
        
    }
    return HttpResponse(template.render(context, request))
