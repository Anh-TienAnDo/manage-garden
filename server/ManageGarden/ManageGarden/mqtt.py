import paho.mqtt.client as paho
import json
from manhdat.models import *
from dieukhien.models import *
from lichsu.models import *
from datetime import datetime

MQTT_SERVER = "broker.mqttdashboard.com"
MQTT_PORT = 1883
TOPIC = '/htn/g6_smart_garden/'  # land/temp/edit
TOPIC_CAMBIEN = '/htn/g6_smart_garden/+/sensor'
TOPIC_TRANGTHAI = '/htn/g6_smart_garden/+/status'
TOPIC_HANHDONG = '/htn/g6_smart_garden/+/action'

def send_control_data(land_id, action_land):
    """
    Gửi thông tin điều khiển qua MQTT.

    Parameters:
        land_id: int - ID của mảnh đất.
        action_land: dict - Thông tin điều khiển.

    Returns:
        None
    """
    # Xây dựng chủ đề MQTT
    t = TOPIC_HANHDONG
    t = t.replace('+', str(land_id))
    # Chuyển đổi thông tin điều khiển sang định dạng JSON
    action_land_json = json.dumps(action_land)
    try:
        # Gửi thông tin điều khiển qua MQTT
        client.publish(t, action_land_json, qos=1)
    except Exception as e:
        print(f"Error publishing control data: {e}")

def handle_sun_roof_control(dieukhien_land, action_land):
    """
    Xử lý việc điều khiển mái che.

    Parameters:
        dieukhien_land: DieuKhien - Thông tin điều khiển của mảnh đất.
        action_land: dict - Thông tin điều khiển hiện tại.

    Returns:
        bool: True nếu cần gửi thông tin điều khiển, ngược lại False.
    """
    is_send = False
    # Lấy thời gian hiện tại trên server
    now = datetime.now().time()
    # Kiểm tra điều kiện bật/tắt mái che
    if now >= dieukhien_land.sun_roof_time_close and now < dieukhien_land.sun_roof_time_open \
            and action_land['sun_roof'] == 1:
        # Thực hiện việc đóng mái che
        action_land['sun_roof'] = 0
        is_send = True
    else:
        if action_land['sun_roof'] == 0:
            # Thực hiện việc mở mái che
            action_land['sun_roof'] = 1
            is_send = True
    return is_send

def handle_lamp_control(anh_sang, dieukhien_land, action_land):
    """
    Xử lý việc điều khiển đèn chiếu sáng.

    Parameters:
        anh_sang: int - Cường độ ánh sáng.
        dieukhien_land: DieuKhien - Thông tin điều khiển của mảnh đất.
        action_land: dict - Thông tin điều khiển hiện tại.

    Returns:
        bool: True nếu cần gửi thông tin điều khiển, ngược lại False.
    """
    is_send = False
    # Lấy thời gian hiện tại trên server
    now = datetime.now().time()
    # Kiểm tra điều kiện bật/tắt đèn chiếu sáng
    if now >= dieukhien_land.lamp_time_off and now < dieukhien_land.lamp_time_on:
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
    return is_send

def handle_water_pump_control(do_am_dat, dieukhien_land, lich_su_hanh_dong_gan_nhat, action_land):
    """
    Xử lý việc điều khiển máy tưới nước.

    Parameters:
        do_am_dat: int - Độ ẩm đất.
        dieukhien_land: DieuKhien - Thông tin điều khiển của mảnh đất.
        lich_su_hanh_dong_gan_nhat: LichSuHanhDong - Lịch sử hành động gần đây nhất.
        action_land: dict - Thông tin điều khiển hiện tại.

    Returns:
        bool: True nếu cần gửi thông tin điều khiển, ngược lại False.
    """
    is_send = False
    # Kiểm tra điều kiện bật/tắt máy tưới nước
    if do_am_dat <= dieukhien_land.water_pump_on and action_land['water_pump'] == 0:
        action_land['water_pump'] = 1
        is_send = True
    if do_am_dat >= dieukhien_land.water_pump_off and action_land['water_pump'] == 1:
        action_land['water_pump'] = 0
        is_send = True
    return is_send

def handle_fan_control(nhiet_do, dieukhien_land, lich_su_hanh_dong_gan_nhat, action_land):
    """
    Xử lý việc điều khiển quạt.

    Parameters:
        nhiet_do: int - Nhiệt độ.
        dieukhien_land: DieuKhien - Thông tin điều khiển của mảnh đất.
        lich_su_hanh_dong_gan_nhat: LichSuHanhDong - Lịch sử hành động gần đây nhất.
        action_land: dict - Thông tin điều khiển hiện tại.

    Returns:
        bool: True nếu cần gửi thông tin điều khiển, ngược lại False.
    """
    is_send = False
    # Kiểm tra điều kiện bật/tắt quạt
    if nhiet_do >= dieukhien_land.fan_on and action_land['fan'] == 0:
        action_land['fan'] = 1
        is_send = True
    if nhiet_do <= dieukhien_land.fan_off and action_land['fan'] == 1:
        action_land['fan'] = 0
        is_send = True
    return is_send

def handle_control_actions(nhiet_do, do_am_dat, anh_sang, topic):
    """
    Xử lý điều khiển.

    Parameters:
        nhiet_do: int - Nhiệt độ.
        do_am_dat: int - Độ ẩm đất.
        anh_sang: int - Cường độ ánh sáng.
        topic: str - Chủ đề MQTT.

    Returns:
        None
    """
    # Lấy mã mảnh đất từ chủ đề
    land_id = topic.split('/')[3]

    try:
        # Lấy thông tin mảnh đất từ mã
        land = ManhDat.objects.get(id=int(land_id))
    except Exception as e:
        print(f'Error {land_id} does not exist: {e}')
        return

    # Lấy điều khiển của mảnh đất
    dieukhien_land = DieuKhien.objects.get(manhdat=land)

    # Lấy lịch sử hành động gần đây nhất cho mỗi mảnh đất
    lich_su_hanh_dong_gan_nhat = LichSuHanhDong.objects.filter(manhdat=land).order_by('-created_at').first()

    # Khởi tạo thông tin điều khiển mặc định
    if lich_su_hanh_dong_gan_nhat:
        action_land = {
            'lamp'      : lich_su_hanh_dong_gan_nhat.den_chieu_sang,
            'water_pump': lich_su_hanh_dong_gan_nhat.may_tuoi_nuoc,
            'fan'       : lich_su_hanh_dong_gan_nhat.quat_mat,
            'sun_roof'  : lich_su_hanh_dong_gan_nhat.mai_che,
        }
    else:
        action_land = {
            'lamp'      : 0,
            'water_pump': 0,
            'fan'       : 0,
            'sun_roof'  : 0,
        }

    # Xử lý việc điều khiển
    is_send = handle_fan_control(nhiet_do, dieukhien_land, lich_su_hanh_dong_gan_nhat, action_land)
    is_send |= handle_water_pump_control(do_am_dat, dieukhien_land, lich_su_hanh_dong_gan_nhat, action_land)
    is_send |= handle_lamp_control(anh_sang, dieukhien_land, action_land)
    is_send |= handle_sun_roof_control(dieukhien_land, action_land)

    # Gửi thông tin điều khiển nếu cần
    if is_send:
        send_control_data(land_id, action_land)

def save_status_history(mai_che, quat_mat, may_tuoi_nuoc, den_chieu_sang):
    """
    Lưu lịch sử dữ liệu trạng thái.

    Parameters:
        mai_che: int - Trạng thái mái che.
        quat_mat: int - Trạng thái quạt làm mát.
        may_tuoi_nuoc: int - Trạng thái máy tưới nước.
        den_chieu_sang: int - Trạng thái đèn chiếu sáng.

    Returns:
        None
    """
    try:
        history_status = LichSuHanhDong.objects.create(mai_che=mai_che, quat_mat=quat_mat,
                                                       may_tuoi_nuoc=may_tuoi_nuoc, den_chieu_sang=den_chieu_sang)
    except Exception as e:
        print(f"Error saving status history: {e}")

def save_sensor_history(nhiet_do, do_am, do_am_dat, anh_sang):
    """
    Lưu lịch sử dữ liệu cảm biến.

    Parameters:
        nhiet_do: int - Nhiệt độ.
        do_am: int - Độ ẩm không khí.
        do_am_dat: int - Độ ẩm đất.
        anh_sang: int - Cường độ ánh sáng.

    Returns:
        None
    """
    try:
        history_sensor = LichSuCamBien.objects.create(nhiet_do=nhiet_do, do_am=do_am,
                                                      do_am_dat=do_am_dat, anh_sang=anh_sang)
    except Exception as e:
        print(f"Error saving sensor history: {e}")

def handle_status_data(data, topic):
    """
    Xử lý dữ liệu trạng thái.

    Parameters:
        data: dict - Dữ liệu trạng thái.
        topic: str - Chủ đề MQTT.

    Returns:
        None
    """
    try:
        # Lấy thông tin trạng thái từ dữ liệu
        mai_che = data["sun_roof"]
        quat_mat = data["fan"]
        may_tuoi_nuoc = data["water_pump"]
        den_chieu_sang = data["lamp"]
    except Exception as e:
        print(f"Error getting status data from {topic}: {e}")
        return

    # Lưu lịch sử trạng thái
    save_status_history(mai_che, quat_mat, may_tuoi_nuoc, den_chieu_sang)

def handle_sensor_data(data, topic):
    """
    Xử lý dữ liệu cảm biến.

    Parameters:
        data: dict - Dữ liệu cảm biến.
        topic: str - Chủ đề MQTT.

    Returns:
        None
    """
    try:
        # Lấy thông tin cảm biến từ dữ liệu
        nhiet_do = int(data["air_temperature"])
        do_am = int(data["air_humidity"])
        do_am_dat = int(data["soil_moisture"])
        anh_sang = int(data["light"])
    except Exception as e:
        print(f"Error getting sensor data from {topic}: {e}")
        return

    # Lưu lịch sử dữ liệu cảm biến
    save_sensor_history(nhiet_do, do_am, do_am_dat, anh_sang)

    # Xử lý điều khiển
    handle_control_actions(nhiet_do, do_am_dat, anh_sang, topic)

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
    # Lấy thông tin từ chủ đề và dữ liệu
    topic = str(msg.topic)
    data = json.loads(msg.payload.decode("UTF-8"))

    # Phân loại và xử lý dữ liệu
    if 'sensor' in topic:
        handle_sensor_data(data, topic)
    elif 'status' in topic:
        handle_status_data(data, topic)
    else:
        print(f"UnKnow: {topic}")
        return
    # ---------------------------
    # topic = str(msg.topic)
    # data = json.loads(msg.payload.decode("UTF-8"))  # type dict
    # land_id = topic.split('/')[3]
    # try:
    #     land = ManhDat.objects.get(id=int(land_id))
    # except:
    #     print(f'Error {land_id} not exists')
    #     return
    #
    # if 'sensor' in topic:
    #     try:
    #         nhiet_do = int(data["air_temperature"])
    #         do_am = int(data["air_humidity"])
    #         do_am_dat = int(data["soil_moisture"])
    #         anh_sang = int(data["light"])
    #     except:
    #         print(f"Error get data from {topic}")
    #         return
    #     history_sensor = LichSuCamBien.objects.create(manhdat=land, nhiet_do=nhiet_do,
    #                                                   do_am=do_am, do_am_dat=do_am_dat,
    #                                                   anh_sang=anh_sang)
    #     dieukhien_land = DieuKhien.objects.get(manhdat=land)
    #     # Lấy lịch sử hành động gần đây nhất cho mỗi mảnh đất
    #     lich_su_hanh_dong_gan_nhat = LichSuHanhDong.objects.filter(manhdat=land).order_by('-created_at').first()
    #     is_send = False
    #     if lich_su_hanh_dong_gan_nhat:
    #         action_land = {
    #             'lamp'      : lich_su_hanh_dong_gan_nhat.den_chieu_sang,
    #             'water_pump': lich_su_hanh_dong_gan_nhat.may_tuoi_nuoc,
    #             'fan'       : lich_su_hanh_dong_gan_nhat.quat_mat,
    #             'sun_roof'  : lich_su_hanh_dong_gan_nhat.mai_che,
    #         }
    #     else:
    #         action_land = {
    #             'lamp'      : 0,
    #             'water_pump': 0,
    #             'fan'       : 0,
    #             'sun_roof'  : 0,
    #         }
    #     if nhiet_do >= dieukhien_land.fan_on and action_land['fan'] == 0:
    #         action_land['fan'] = 1
    #         is_send = True
    #     if nhiet_do <= dieukhien_land.fan_off and action_land['fan'] == 1:
    #         action_land['fan'] = 0
    #         is_send = True
    #     # --------------------
    #     if do_am_dat <= dieukhien_land.water_pump_on and action_land['water_pump'] == 0:
    #         action_land['water_pump'] = 1
    #         is_send = True
    #     if do_am_dat >= dieukhien_land.water_pump_off and action_land['water_pump'] == 1:
    #         action_land['water_pump'] = 0
    #         is_send = True
    #     # --------------------
    #     # time lamp
    #     now = datetime.now().time()
    #     if now >= dieukhien_land.lamp_time_off and now < dieukhien_land.lamp_time_on:
    #         if anh_sang <= 300 and action_land['lamp'] == 0:
    #             action_land['lamp'] = 1
    #             is_send = True
    #         elif anh_sang > 300 and action_land['lamp'] == 1:
    #             action_land['lamp'] = 0
    #             is_send = True
    #     else:
    #         if action_land['lamp'] == 0:
    #             action_land['lamp'] = 1
    #             is_send = True
    #     # --------------------
    #     # time sun_roof
    #     if now >= dieukhien_land.sun_roof_time_close and now < dieukhien_land.sun_roof_time_open \
    #             and action_land['sun_roof'] == 1:
    #         # Thực hiện việc đóng mái che
    #         action_land['sun_roof'] = 0
    #         is_send = True
    #
    #     else:
    #         if action_land['sun_roof'] == 0:
    #             # Thực hiện việc mở mái che
    #             action_land['sun_roof'] = 1
    #             is_send = True
    #     # --------------------
    #     if is_send:
    #         t = TOPIC_HANHDONG
    #         t = t.replace('+', str(land_id))
    #         action_land_json = json.dumps(action_land)
    #         try:
    #             client.publish(t, action_land_json, qos=1)
    #         except Exception as pub_error:
    #             print("Error publishing:", pub_error)
    #
    # elif 'status' in topic:
    #     try:
    #         mai_che = data["sun_roof"]
    #         quat_mat = data["fan"]
    #         may_tuoi_nuoc = data["water_pump"]
    #         den_chieu_sang = data["lamp"]
    #     except:
    #         print(f"Error get data from {topic}")
    #         return
    #     history_status = LichSuHanhDong.objects.create(manhdat=land, mai_che=mai_che, quat_mat=quat_mat,
    #                                                    may_tuoi_nuoc=may_tuoi_nuoc, den_chieu_sang=den_chieu_sang)
    # else:
    #     print(f"UnKnow: {topic}")
    #     return


client = paho.Client(paho.CallbackAPIVersion.VERSION1)
client.on_subscribe = on_subscribe
client.on_message = on_message
client.connect(MQTT_SERVER, MQTT_PORT)
# đăng ký các chủ đề (topics) để nhận dữ liệu từ broker MQTT
client.subscribe(TOPIC_CAMBIEN, qos=1)
client.subscribe(TOPIC_TRANGTHAI, qos=1)
