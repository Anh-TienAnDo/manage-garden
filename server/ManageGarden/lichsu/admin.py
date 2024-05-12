from django.contrib import admin
from .models import *

db_name = "garden"
# Register your models here.
class LichSuCamBienAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        # obj.save(using='mongodb')
        obj.save(using=db_name)
    def get_queryset(self, request):
        # return Phone.objects.using('mongodb')
        return LichSuCamBien.objects.using(db_name)

class LichSuHanhDongAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        # obj.save(using='mongodb')
        obj.save(using=db_name)
    def get_queryset(self, request):
        # return Phone.objects.using('mongodb')
        return LichSuHanhDong.objects.using(db_name)

admin.site.register(LichSuCamBien, LichSuCamBienAdmin)
admin.site.register(LichSuHanhDong, LichSuHanhDongAdmin)
