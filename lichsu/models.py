from django.db import models
from manhdat.models import *

# Create your models here.

# Create your models here.
class LichSuCamBien(models.Model):
    manhdat = models.ForeignKey(ManhDat, models.SET_NULL, null=True)
    nhiet_do = models.FloatField(default=0)
    do_am = models.FloatField(default=0)
    do_am_dat = models.FloatField(default=0)
    anh_sang = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.manhdat

class LichSuHanhDong(models.Model):
    manhdat = models.ForeignKey(ManhDat, models.SET_NULL, null=True)
    mai_che = models.FloatField(default=0)
    quat_mat = models.FloatField(default=0)
    may_tuoi_nuoc = models.FloatField(default=0)
    den_chieu_sang = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.manhdat
