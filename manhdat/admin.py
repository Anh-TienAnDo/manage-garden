from django.contrib import admin
from .models import *
# Register your models here.
db_name = "default"

class ManhDatAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        obj.save(using=db_name)
    def get_queryset(self, request):
        return ManhDat.objects.using(db_name)

class UseerManhDatAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        obj.save(using=db_name)
    def get_queryset(self, request):
        return UserManhDat.objects.using(db_name)
admin.site.register(ManhDat, ManhDatAdmin)
admin.site.register(UserManhDat, UseerManhDatAdmin)
