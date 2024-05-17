from rest_framework import serializers
from lichsu.models import LichSuCamBien, LichSuHanhDong

class LichSuCamBienSerializer(serializers.ModelSerializer):
    class Meta:
        model = LichSuCamBien
        fields = '__all__'
    
class LichSuHanhDongSerializer(serializers.ModelSerializer):    
    class Meta:
        model = LichSuHanhDong
        fields = '__all__'