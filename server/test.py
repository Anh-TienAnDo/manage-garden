# s = '/htn/g6_smart_garden/+/sensor'
# print(s.split(r"/")[3])

import datetime
# from ManageGarden.ManageGarden.mqtt import TOPIC_HANHDONG

# Lấy thời gian hiện tại trên server
now = datetime.datetime.now()
print(now)
print(now.time())

time = datetime.time(6,48,00)
if time > now.time():
    print('Yes')
else:
    print('No')

# print(TOPIC_HANHDONG)
# Xử lý việc điều khiển
is_send = False
is_send |= False
is_send |= False
is_send |= False
print(is_send)