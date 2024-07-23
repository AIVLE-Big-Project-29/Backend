# Create your views here.
# views.py
from django.shortcuts import render
import pandas as pd
from .models import Location
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import StateProvinceSerializer, CityCountySerializer, TownVillageSerializer

class StateProvinceView(APIView):
    def get(self, request):
        state_provinces = Location.objects.values('state_province').distinct()
        serializer = StateProvinceSerializer(state_provinces, many=True)
        return Response(serializer.data)

class CityCountyView(APIView):
    def get(self, request):
        state_province = request.GET.get('state_province')
        city_counties = Location.objects.filter(state_province=state_province).values('city_county', 'latitude', 'longitude').distinct()
        serializer = CityCountySerializer(city_counties, many=True)
        return Response(serializer.data)

class TownVillageView(APIView):
    def get(self, request):
        state_province = request.GET.get('state_province')
        city_county = request.GET.get('city_county')
        town_villages = Location.objects.filter(state_province=state_province, city_county=city_county).values('town_village', 'latitude', 'longitude').distinct()
        serializer = TownVillageSerializer(town_villages, many=True)
        return Response(serializer.data)


# db 업데이트
def import_excel():
    excel_file = ''
    df = pd.read_excel(excel_file)

    try:
        for _, row in df.iterrows():
            Location.objects.create(
                latitude=row['위도'],
                longitude=row['경도'],
                state_province=row['시/도'],
                city_county=row['시/군/구'],
                town_village=row['읍/면/동']
            )
    except:
        print('error')
