from rest_framework import serializers
from app import models


class ProductBrandSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.ProductBrand
        fields = ['id', 'name', 'product']


class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Order
        fields = ['client', 'date', 'order_number']


class GeyserSystemSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.GeyserSystemOrder
        fields = ['property_type', 'roof_inclination',
                  'users_number', 'required_geyser_size', 'water_collector']


class PVTSystemSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.PVTSystem
        fields = ['property_type', 'roof_inclination',
                  'intended_use', 'site_visit']


class SystemOrderSerializer(serializers.ModelSerializer):
    geyser = GeyserSystemSerializer(many=True, read_only=True)
    pvt = PVTSystemSerializer(many=True, read_only=True)

    class Meta:
        model = models.SystemOrder
        fields = ['need_finance', 'include_installation',
                  'order_number', 'geyser', 'pvt']


class ProvinceSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Province
        fields = ['name']


class AddressSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.PhysicalAddress
        fields = ['building_name', 'street_name', 'suburb',
                  'city', 'zip_code', 'province_id']


class ClientSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Client
        fields = ['username', 'lastname', 'firstname',
                  'contact_number', 'physical_address_id']
