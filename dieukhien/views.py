from django.shortcuts import render, redirect
from .models import DieuKhien
from lichsu.models import LichSuHanhDong
from datetime import datetime, time
from ManageGarden.mqtt import client, TOPIC_HANHDONG
import json

# Create your views here.

def get_action_land(lich_su_hanh_dong_gan_nhat):
    if lich_su_hanh_dong_gan_nhat:
        action_land = {
            'lamp'      : int(lich_su_hanh_dong_gan_nhat.den_chieu_sang),
            'water_pump': int(lich_su_hanh_dong_gan_nhat.may_tuoi_nuoc),
            'fan'       : int(lich_su_hanh_dong_gan_nhat.quat_mat),
            'sun_roof'  : int(lich_su_hanh_dong_gan_nhat.mai_che),
        }
    else:
        action_land = {
            'lamp'      : 0,
            'water_pump': 0,
            'fan'       : 0,
            'sun_roof'  : 0,
        }
    return action_land

def check_action_land(action_land, action_land_old):
    if action_land['lamp'] != action_land_old['lamp']:
        return False
    if action_land['water_pump'] != action_land_old['water_pump']:
        return False
    if action_land['fan'] != action_land_old['fan']:
        return False
    if action_land['sun_roof'] != action_land_old['sun_roof']:
        return False
    return True

def publish_mqtt(land_id, action_land):
    t = TOPIC_HANHDONG
    t = t.replace('+', str(land_id))
    action_land_json = json.dumps(action_land)
    time_past = datetime.now()
    while True:
        time_now = datetime.now()
        if time_now - time_past > 0.3:
            lich_su_hanh_dong_gan_nhat = LichSuHanhDong.objects.filter(manhdat__id=land_id).order_by('-created_at').first()
            action_land_old = get_action_land(lich_su_hanh_dong_gan_nhat)
            if check_action_land(action_land, action_land_old):
                break
            try:
                client.publish(t, action_land_json, qos=1)
                print("topic:", t)
                print(f"publish data: {action_land_json}")
            except Exception as pub_error:
                print("Error publishing:", pub_error)
                time_past = datetime.now()

def get_home(request):
    return render(request, 'home.html')

def dieu_khien(request, id):
    dieu_khien = DieuKhien.objects.filter(manhdat__id=id).first()
    lich_su_hanh_dong_gan_nhat = LichSuHanhDong.objects.filter(manhdat__id=id).order_by('-created_at').first()
    return render(request, 'dieukhien/dieukhien.html', {
        'dieukhien': dieu_khien,
        'land_id': id,
        'lichsu': lich_su_hanh_dong_gan_nhat,
    })

def updateLamp(request, id):
    dieu_khien = DieuKhien.objects.filter(manhdat__id=id).first()
    lich_su_hanh_dong_gan_nhat = LichSuHanhDong.objects.filter(manhdat__id=id).order_by('-created_at').first()
    method = request.method
    if method == 'GET':
        action = request.GET.get('action')
        action_land = get_action_land(lich_su_hanh_dong_gan_nhat)
        if action == "turn_on":
            action_land.update({'lamp': 1})
        elif action == 'turn_off':
            action_land.update({'lamp': 0})

        publish_mqtt(id, action_land)

    if method == 'POST':
        # Check which button was clicked
        if 'update' in request.POST:
            print("Update button clicked")
            lamp_time_on_hour = int(request.POST.get('lamp_time_on_hour'))
            lamp_time_on_minute = int(request.POST.get('lamp_time_on_minute'))
            lamp_time_off_hour = int(request.POST.get('lamp_time_off_hour'))
            lamp_time_off_minute = int(request.POST.get('lamp_time_off_minute'))
            
            lamp_time_off = datetime.combine(datetime.today(), time(lamp_time_off_hour, lamp_time_off_minute))
            lamp_time_on = datetime.combine(datetime.today(), time(lamp_time_on_hour, lamp_time_on_minute))
            dieu_khien.lamp_time_off = lamp_time_off
            dieu_khien.lamp_time_on = lamp_time_on
            dieu_khien.save()
        
    # elif 'action' in request.POST:
    #     action_value = request.POST.get('action')
    #     print(f"Action button clicked with value: {action_value}")
    #     action_land = get_action_land(lich_su_hanh_dong_gan_nhat)
    #     if action_value == 'turn_on':
    #         action_land.update({'lamp': 1})
            
    #     elif action_value == 'turn_off':
    #         action_land.update({'lamp': 0})

    #     publish_mqtt(id, action_land)
    
    return redirect('dieukhien', id=id)

def updatePump(request, id):
    dieu_khien = DieuKhien.objects.filter(manhdat__id=id).first()
    lich_su_hanh_dong_gan_nhat = LichSuHanhDong.objects.filter(manhdat__id=id).order_by('-created_at').first()
    method = request.method
    if method == 'GET':
        action = request.GET.get('action')
        action_land = get_action_land(lich_su_hanh_dong_gan_nhat)
        if action == "turn_on":
            action_land.update({'water_pump': 1})
        elif action == 'turn_off':
            action_land.update({'water_pump': 0})

        publish_mqtt(id, action_land)
    
    if method == 'POST':
        # Check which button was clicked
        if 'update' in request.POST:
            water_pump_on = int(request.POST.get('water_pump_on'))
            water_pump_off = int(request.POST.get('water_pump_off'))
            dieu_khien.water_pump_on = water_pump_on
            dieu_khien.water_pump_off = water_pump_off
            dieu_khien.save()
        
    return redirect('dieukhien', id=id)

def updateFan(request, id):
    dieu_khien = DieuKhien.objects.filter(manhdat__id=id).first()
    lich_su_hanh_dong_gan_nhat = LichSuHanhDong.objects.filter(manhdat__id=id).order_by('-created_at').first()
    
    method = request.method
    if method == 'GET':
        action = request.GET.get('action')
        action_land = get_action_land(lich_su_hanh_dong_gan_nhat)
        if action == "turn_on":
            action_land.update({'fan': 1})
        elif action == 'turn_off':
            action_land.update({'fan': 0})

        publish_mqtt(id, action_land)
    
    if method == 'POST':
        # Check which button was clicked
        if 'update' in request.POST:
            fan_on = int(request.POST.get('fan_on'))
            fan_off = int(request.POST.get('fan_off'))
            dieu_khien.fan_on = fan_on
            dieu_khien.fan_off = fan_off
            dieu_khien.save()
    
    return redirect('dieukhien', id=id)

def updateRoof(request, id):
    dieu_khien = DieuKhien.objects.filter(manhdat__id=id).first()
    lich_su_hanh_dong_gan_nhat = LichSuHanhDong.objects.filter(manhdat__id=id).order_by('-created_at').first()
    
    method = request.method
    if method == 'GET':
        action = request.GET.get('action')
        action_land = get_action_land(lich_su_hanh_dong_gan_nhat)
        if action == "turn_on":
            action_land.update({'sun_roof': 1})
        elif action == 'turn_off':
            action_land.update({'sun_roof': 0})

        publish_mqtt(id, action_land)
    
    if method == 'POST':
        # Check which button was clicked
        if 'update' in request.POST:
            sun_roof_time_close_hour = int(request.POST.get('sun_roof_time_close_hour'))
            sun_roof_time_close_minute = int(request.POST.get('sun_roof_time_close_minute'))
            sun_roof_time_open_hour = int(request.POST.get('sun_roof_time_open_hour'))
            sun_roof_time_open_minute = int(request.POST.get('sun_roof_time_open_minute'))
            
            sun_roof_time_close = datetime.combine(datetime.today(), time(sun_roof_time_close_hour, sun_roof_time_close_minute))
            sun_roof_time_open = datetime.combine(datetime.today(), time(sun_roof_time_open_hour, sun_roof_time_open_minute))
            dieu_khien.sun_roof_time_close = sun_roof_time_close
            dieu_khien.sun_roof_time_open = sun_roof_time_open
            dieu_khien.save()
    
    return redirect('dieukhien', id=id)

    
    
    