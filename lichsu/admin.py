from django.contrib import admin
from .models import *
# Register your models here.
db_name = "default"
class LichSuCamBienAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        obj.save(using=db_name)
    def get_queryset(self, request):
        return LichSuCamBien.objects.using(db_name)

class LichSuHanhDongAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        obj.save(using=db_name)
    def get_queryset(self, request):
        return LichSuHanhDong.objects.using(db_name)

admin.site.register(LichSuCamBien, LichSuCamBienAdmin)
admin.site.register(LichSuHanhDong, LichSuHanhDongAdmin)
