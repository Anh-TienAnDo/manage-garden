from django.db import models
from manhdat.models import *
from datetime import time

# Create your models here.
class DieuKhien(models.Model):
    manhdat = models.OneToOneField(ManhDat, models.SET_NULL, null=True)
    lamp_time_on = models.TimeField(default=time(18,00,00))
    lamp_time_off = models.TimeField(default=time(6,00,00))
    water_pump_on = models.IntegerField(default=50)
    water_pump_off = models.IntegerField(default=70)
    fan_on = models.IntegerField(default=35)
    fan_off = models.IntegerField(default=25)
    sun_roof_time_close = models.TimeField(default=time(11,00,00))
    sun_roof_time_open = models.TimeField(default=time(14,00,00))
    created_at = models.DateTimeField(auto_now_add=True)

    # each individual status
    # TUOI_NUOC = 1
    # BAT_DEN_CHIEU_SANG = 2
    # BAT_QUAT_LAM_MAT = 3
    # MO_MAY_CHE = 4
    # DONG_MAY_CHE = 5
    # # set of possible order statuses
    # ACTIONS = ((TUOI_NUOC, 'TUOI_NUOC'),
    #                   (BAT_DEN_CHIEU_SANG, 'BAT_DEN_CHIEU_SANG'),
    #             (BAT_QUAT_LAM_MAT, 'BAT_QUAT_LAM_MAT'),
    #                   (MO_MAY_CHE, 'MO_MAY_CHE'),
    #             (DONG_MAY_CHE, 'DONG_MAY_CHE'),)
    def __str__(self):
        return self.manhdat.name

