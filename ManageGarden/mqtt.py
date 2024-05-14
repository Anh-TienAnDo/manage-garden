import paho.mqtt.client as paho
import json
from .connection_db import ConnectionDB
from datetime import datetime

MQTT_SERVER = "broker.mqttdashboard.com"
MQTT_PORT = 1883
TOPIC = '/htn/g6_smart_garden/'  # land/temp/edit
TOPIC_CAMBIEN = '/htn/g6_smart_garden/+/sensor'
TOPIC_TRANGTHAI = '/htn/g6_smart_garden/+/status'
TOPIC_HANHDONG = '/htn/g6_smart_garden/+/action'
MANHDAT_TABLE = 'manhdat_manhdat'
DIEUKHIEN_TABLE = 'dieukhien_dieukhien'
LICHSUHANHDONG_TABLE = 'lichsu_lichsuhanhdong'
LICHSUCAMBIEN_TABLE = 'lichsu_lichsucambien'

def on_subscribe(client, userdata, mid, granted_qos):
    print("Subscribed: " + str(userdata) + " " + str(mid) + " " + str(granted_qos))

# nhận data rồi set vào db
def on_message(client, userdata, msg):
    """
    Xử lý dữ liệu nhận được từ MQTT.

    Parameters:
        client: mqtt.Client - Client MQTT.
        userdata: object - Dữ liệu người dùng (nếu có).
        msg: MQTTMessage - Thông điệp MQTT.

    Returns:
        None
    """
    # ---------------------------
    db = ConnectionDB()
    cambien_data = {
        'nhiet_do': None,
        'do_am': None,
        'do_am_dat': None,
        'anh_sang': None,
        'manhdat_id': None,
    }
    topic = str(msg.topic)
    print(topic)
    data = json.loads(msg.payload.decode("UTF-8"))  # type dict
    print(data)
    land_id = topic.split('/')[3]
    try:
        # land = ManhDat.objects.get(id=int(land_id))
        land = db.select_by_manhdat(MANHDAT_TABLE, int(land_id))
    except:
        print(f'Error {land_id} not exists')
        return

    if 'sensor' in topic:
        try:
            nhiet_do = float(data["air_temperature"])
            do_am = float(data["air_humidity"])
            do_am_dat = float(data["soil_moisture"])
            anh_sang = float(data["light"])
        except:
            print(f"Error get data from {topic}")
            return
        try:
            cambien_data['nhiet_do'] = nhiet_do
            cambien_data['do_am'] = do_am
            cambien_data['do_am_dat'] = do_am_dat
            cambien_data['anh_sang'] = anh_sang
            cambien_data['manhdat_id'] = land_id
            db.insert_lichsucambien(LICHSUCAMBIEN_TABLE, cambien_data)
            print("saved history_sensor")
        except Exception as e:
            print(f"Error: {e}")

        dieukhien_land = db.select_by_dieukhienmanhdat(DIEUKHIEN_TABLE, land_id)

        # Lấy lịch sử hành động gần đây nhất cho mỗi mảnh đất
        # lich_su_hanh_dong_gan_nhat = LichSuHanhDong.objects.filter(manhdat=land).order_by('-created_at').first()
        lich_su_hanh_dong_gan_nhat = db.select_lichsuhanhdong_by_manhdat_id(LICHSUHANHDONG_TABLE, land_id)[0]
        print('lich_su_hanh_dong_gan_nhat')
        print(lich_su_hanh_dong_gan_nhat)
        is_send = False
        if lich_su_hanh_dong_gan_nhat:
            action_land = {
                'lamp'      : lich_su_hanh_dong_gan_nhat.get('den_chieu_sang'),
                'water_pump': lich_su_hanh_dong_gan_nhat.get('may_tuoi_nuoc'),
                'fan'       : lich_su_hanh_dong_gan_nhat.get('quat_mat'),
                'sun_roof'  : lich_su_hanh_dong_gan_nhat.get('mai_che'),
            }
        else:
            action_land = {
                'lamp'      : 0,
                'water_pump': 0,
                'fan'       : 0,
                'sun_roof'  : 0,
            }
        if nhiet_do >= dieukhien_land.get('fan_on') and action_land['fan'] == 0:
            action_land['fan'] = 1
            is_send = True
        elif nhiet_do <= dieukhien_land.get('fan_off') and action_land['fan'] == 1:
            action_land['fan'] = 0
            is_send = True
        # --------------------
        if do_am_dat <= dieukhien_land.get('water_pump_on') and action_land['water_pump'] == 0:
            action_land['water_pump'] = 1
            is_send = True
        elif do_am_dat >= dieukhien_land.get('water_pump_off') and action_land['water_pump'] == 1:
            action_land['water_pump'] = 0
            is_send = True
        # --------------------
        # time lamp
        now_seconds = (datetime.now() - datetime.combine(datetime.now(), datetime.min.time())).seconds
        lamp_time_off_seconds = dieukhien_land.get('lamp_time_off').seconds
        lamp_time_on_seconds = dieukhien_land.get('lamp_time_on').seconds
        if now_seconds >= lamp_time_off_seconds and now_seconds < lamp_time_on_seconds:
            if anh_sang <= 300 and action_land['lamp'] == 0:
                action_land['lamp'] = 1
                is_send = True
            elif anh_sang > 300 and action_land['lamp'] == 1:
                action_land['lamp'] = 0
                is_send = True
        else:
            if action_land['lamp'] == 0:
                action_land['lamp'] = 1
                is_send = True
        # --------------------
        # time sun_roof
        sun_roof_close_seconds = dieukhien_land.get('sun_roof_time_close').seconds
        sun_roof_open_seconds = dieukhien_land.get('sun_roof_time_open').seconds
        if now_seconds >= sun_roof_close_seconds and now_seconds < sun_roof_open_seconds:
            # Thực hiện việc đóng mái che
            if anh_sang > 2000 and action_land['sun_roof'] == 1:
                action_land['sun_roof'] = 0
                is_send = True

        else:
            if action_land['sun_roof'] == 0:
                # Thực hiện việc mở mái che
                action_land['sun_roof'] = 1
                is_send = True
        # --------------------
        if is_send:
            t = TOPIC_HANHDONG
            t = t.replace('+', str(land_id))
            action_land_json = json.dumps(action_land)
            try:
                client.publish(t, action_land_json, qos=1)
            except Exception as pub_error:
                print("Error publishing:", pub_error)

    elif 'status' in topic:
        hanhdong_data = {
            'mai_che': None,
            'quat_mat': None,
            'may_tuoi_nuoc': None,
            'den_chieu_sang': None,
            'manhdat_id': None,
        }
        try:
            mai_che = int(data["sun_roof"])
            quat_mat = int(data["fan"])
            may_tuoi_nuoc = int(data["water_pump"])
            den_chieu_sang = int(data["lamp"])
        except:
            print(f"Error get data from {topic}")
            return
        try:
            hanhdong_data['mai_che'] = mai_che
            hanhdong_data['quat_mat'] = quat_mat
            hanhdong_data['may_tuoi_nuoc'] = may_tuoi_nuoc
            hanhdong_data['den_chieu_sang'] = den_chieu_sang
            hanhdong_data['manhdat_id'] = land_id
            db.insert_lichsuhanhdong(LICHSUHANHDONG_TABLE, hanhdong_data)
            print('saved history_status')
        except Exception as e:
            print(f"Error: {e}")
            
    else:
        print(f"UnKnow: {topic}")
        return


client = paho.Client(paho.CallbackAPIVersion.VERSION1)
client.on_subscribe = on_subscribe
client.on_message = on_message
client.connect(MQTT_SERVER, MQTT_PORT)
# đăng ký các chủ đề (topics) để nhận dữ liệu từ broker MQTT
client.subscribe(TOPIC_CAMBIEN, qos=1)
client.subscribe(TOPIC_TRANGTHAI, qos=1)
