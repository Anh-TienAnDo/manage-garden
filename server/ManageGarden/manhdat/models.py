from djongo import models
from django.contrib.auth.models import User

# Create your models here.
class ManhDat(models.Model):
    name = models.CharField(max_length=255, null=True)
    address = models.TextField(null=True)
    description = models.TextField(null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class UserManhDat(models.Model):
    # each individual status
    CHU = 1
    KHACH = 2
    # set of possible order statuses
    STATUSES = ((CHU, 'CHU'),
                      (KHACH, 'KHACH'),)
    user = models.ForeignKey(User, models.SET_NULL, null=True)
    manhdat = models.ForeignKey(ManhDat, models.SET_NULL, null=True)
    role = models.IntegerField(choices=STATUSES, default=CHU)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.user) + '-' + str(self.manhdat)
