from django.apps import apps

def start_mqtt_client():
    from .mqtt import client
    try:
        client.loop_start()
    except Exception as e:
        print(e)
        client.disconnect()

# Chờ cho ứng dụng Django được tải và cấu hình
def ready():
    start_mqtt_client()

# Kiểm tra xem ứng dụng đã được tải chưa trước khi thực hiện bất kỳ thao tác nào
if apps.ready and apps.is_installed('manhdat') and apps.is_installed('dieukhien') and apps.is_installed('lichsu'):
    start_mqtt_client()
