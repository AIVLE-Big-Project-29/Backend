from django.db import models

# Create your models here.
class Location(models.Model):
    latitude = models.DecimalField(max_digits=9, decimal_places=6, help_text="위도")
    longitude = models.DecimalField(max_digits=9, decimal_places=6, help_text="경도")
    state_province = models.CharField(max_length=100, help_text="시/도")
    city_county = models.CharField(max_length=100, help_text="시/군/구")
    town_village = models.CharField(max_length=100, help_text="읍/면/동")

    def __str__(self):
        return f"{self.state_province} {self.city_county} {self.town_village}"

    class Meta:
        verbose_name = "Address"
        verbose_name_plural = "Addresses"