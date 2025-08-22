from rest_framework import serializers
from .models import FastinnData


# class GetDataSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = FastinnData
#         # fields = "__all__"
#         fields = ("id", "postnr", "heimilisfang", "kaupverd", "tegund", "fastnum", "einflm", "thinglystdags", "onothaefur_samningur")

class GetDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = FastinnData
        fields = ("id", "postnr", "heimilisfang", "kaupverd", "tegund", "fastnum", "einflm", "thinglystdags",
                  "onothaefur_samningur", "fermetravera")

    def to_representation(self, instance):
        # Get the default representation
        representation = super().to_representation(instance)

        # Format kaupverd: convert int to string with thousand separator and 'kr'
        if representation.get('kaupverd') is not None:
            kaupverd = str(representation['kaupverd'])
            # Add thousand separator (dot after every 3 digits from the right)
            if len(kaupverd) > 3:
                formatted_kaupverd = ''
                for i, digit in enumerate(reversed(kaupverd)):
                    if i > 0 and i % 3 == 0:
                        formatted_kaupverd = '.' + formatted_kaupverd
                    formatted_kaupverd = digit + formatted_kaupverd
                representation['kaupverd'] = formatted_kaupverd + ' kr'
            else:
                representation['kaupverd'] = kaupverd + ' kr'

        # Format einflm: convert float to string and add 'm²'
        if representation.get('einflm') is not None:
            representation['einflm'] = str(representation['einflm']) + ' m²'

        # Format fermetravera: convert float to string and add 'kr./m²'
        if representation.get('fermetravera') is not None:
            representation['fermetravera'] = str(representation['fermetravera']) + ' kr./m²'

        return representation

class SingleDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = FastinnData
        fields = "__all__"
    def to_representation(self, instance):
        # Get the default representation
        representation = super().to_representation(instance)

        # Format kaupverd: convert int to string with thousand separator and 'kr'
        if representation.get('kaupverd') is not None:
            kaupverd = str(representation['kaupverd'])
            # Add thousand separator (dot after every 3 digits from the right)
            if len(kaupverd) > 3:
                formatted_kaupverd = ''
                for i, digit in enumerate(reversed(kaupverd)):
                    if i > 0 and i % 3 == 0:
                        formatted_kaupverd = '.' + formatted_kaupverd
                    formatted_kaupverd = digit + formatted_kaupverd
                representation['kaupverd'] = formatted_kaupverd + ' kr'
            else:
                representation['kaupverd'] = kaupverd + ' kr'

        # Format einflm: convert float to string and add 'm²'
        if representation.get('einflm') is not None:
            representation['einflm'] = str(representation['einflm']) + ' m²'

        # Format fermetravera: convert float to string and add 'kr./m²'
        if representation.get('fermetravera') is not None:
            representation['fermetravera'] = str(representation['fermetravera']) + ' kr./m²'

        return representation


class CSVUploadSerializer(serializers.Serializer):
    file = serializers.FileField()

