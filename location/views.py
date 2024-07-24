# Create your views here.
# views.py
from django.shortcuts import render
import pandas as pd
from .models import Location
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import StateProvinceSerializer, CityCountySerializer, TownVillageSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated

class StateProvinceView(APIView):
    # permission_classes = [AllowAny]
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        state_provinces = Location.objects.values('state_province').distinct().exclude(state_province="nan")
        serializer = StateProvinceSerializer(state_provinces, many=True)
        return Response(serializer.data)

class CityCountyView(APIView):
    # permission_classes = [AllowAny]
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        state_province = request.POST.get('state_province')
        if not state_province or state_province == "nan":
            return Response({"error": "유효한 state_province 파라미터가 필요합니다."}, status=400)

        city_counties = Location.objects.filter(
            state_province=state_province
        ).exclude(
            city_country__isnull=True
        ).exclude(
            city_country="nan"
        ).exclude(
            city_country=state_province
        ).values('city_country').distinct()
        
        serializer = CityCountySerializer(city_counties, many=True)
        return Response(serializer.data)

class TownVillageView(APIView):
    # permission_classes = [AllowAny]
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        state_province = request.POST.get('state_province')
        city_country = request.POST.get('city_country')
        if not state_province or state_province == "nan" or not city_country or city_country == "nan":
            return Response({"error": "유효한 state_province 및 city_country 파라미터가 필요합니다."}, status=400)

        town_villages = Location.objects.filter(
            state_province=state_province,
            city_country=city_country
        ).exclude(
            town_village__isnull=True
        ).exclude(
            town_village="nan"
        ).values('town_village', 'latitude', 'longitude').distinct()
        
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
