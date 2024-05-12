from django.contrib import admin
from .models import *
db_name = "garden"

# Register your models here.
class ManhDatAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        # obj.save(using='mongodb')
        obj.save(using=db_name)
    def get_queryset(self, request):
        # return Phone.objects.using('mongodb')
        return ManhDat.objects.using(db_name)

class UseerManhDatAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        # obj.save(using='mongodb')
        obj.save(using=db_name)
    def get_queryset(self, request):
        # return Phone.objects.using('mongodb')
        return UserManhDat.objects.using(db_name)
admin.site.register(ManhDat, ManhDatAdmin)
admin.site.register(UserManhDat, UseerManhDatAdmin)
