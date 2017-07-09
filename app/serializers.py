from rest_framework import serializers
from app import models


class SolarPanelSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.SolarPanel
        fields = ['id', 'brand', 'size']


class ProductBrandSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.ProductBrand
        fields = ['id', 'name', 'product']
