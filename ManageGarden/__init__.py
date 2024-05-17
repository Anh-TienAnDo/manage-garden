import pymysql
from django.apps import apps
from .settings import INSTALLED_APPS
from .mqtt import client

# Cài đặt pymysql cho MySQL
pymysql.install_as_MySQLdb()

try:
    client.loop_start()
except Exception as e:
    print(e)
    client.disconnect()

# # Đảm bảo rằng ứng dụng mqtt đã được cài đặt
# def start_mqtt_client():
#     from .mqtt import client
#
#     print('start_mqtt_client')
#     try:
#         client.loop_start()
#     except Exception as e:
#         print(e)
#         client.disconnect()
#
# # Chờ cho ứng dụng Django được tải và cấu hình
# def ready():
#     if apps.ready and all(apps.is_installed(app_name) for app_name in INSTALLED_APPS):
#         start_mqtt_client()

