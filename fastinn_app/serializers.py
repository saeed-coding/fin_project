from rest_framework import serializers
from .models import FastinnData


class GetDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = FastinnData
        # fields = "__all__"
        fields = ("id", "postnr", "heimilisfang", "kaupverd", "tegund", "fastnum", "einflm", "thinglystdags", "onothaefur_samningur")


class SingleDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = FastinnData
        fields = "__all__"


class CSVUploadSerializer(serializers.Serializer):
    file = serializers.FileField()

