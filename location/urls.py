from django.urls import path
from .views import StateProvinceView, CityCountyView, TownVillageView

urlpatterns = [
    path('state_provinces/', StateProvinceView.as_view(), name='state_province-list'),
    path('city_counties/', CityCountyView.as_view(), name='city_county-list'),
    path('town_villages/', TownVillageView.as_view(), name='town_village-list'),
]