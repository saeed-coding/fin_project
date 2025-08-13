from rest_framework import serializers
from .models import FastinnData


class GetDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = FastinnData
        fields = '__all__'
