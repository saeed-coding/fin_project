from rest_framework import serializers
from .models import FastinnData


class GetDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = FastinnData
        fields = "__all__"
        # fields = ("postnr", "heimilisfang", "kaupverd", "tegund", "kaupverd")



class CSVUploadSerializer(serializers.Serializer):
    file = serializers.FileField()

