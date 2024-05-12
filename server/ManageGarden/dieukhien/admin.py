from django.contrib import admin
from .models import *
# Register your models here.
db_name = "garden"
class DieuKhienAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        # obj.save(using='mongodb')
        obj.save(using=db_name)
    def get_queryset(self, request):
        # return Phone.objects.using('mongodb')
        return DieuKhien.objects.using(db_name)

admin.site.register(DieuKhien, DieuKhienAdmin)
