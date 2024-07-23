from rest_framework import serializers
from .models import Location

class StateProvinceSerializer(serializers.Serializer):
    state_province = serializers.CharField(max_length=100)

class CityCountySerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['city_county']

class TownVillageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['town_village', 'latitude', 'longitude']
