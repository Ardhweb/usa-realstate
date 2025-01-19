from django.db import models

# Create your models here.

class MyModel(models.Model):
    name = models.CharField(max_length=100)

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Country(models.Model):
    name = models.CharField(max_length=100, null=True)
    code = models.CharField(max_length=3, unique=True, null=True)  # ISO 3166-1 alpha-3 code


class Region(models.Model):
    name = models.CharField(max_length=100, null=True)
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True, blank=True, related_name="regions")


class City(models.Model):
    name = models.CharField(max_length=100, null=True)
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True, blank=True, related_name="cities")
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True, blank=True, related_name="cities")


class PostalCode(models.Model):
    code = models.CharField(max_length=20, unique=True, null=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True, related_name="postal_codes")

class Address(models.Model):
    line_1 = models.CharField(max_length=255, null=True)
    line_2 = models.CharField(max_length=255, null=True, blank=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True, related_name="addresses")
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True, blank=True, related_name="addresses")
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True, blank=True, related_name="addresses")
    postal_code = models.ForeignKey(PostalCode, on_delete=models.SET_NULL, null=True, blank=True, related_name="addresses")
