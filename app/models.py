from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

class Province(models.Model):
    name = models.CharField(max_length=30)

class PhysicalAddress(models.Model):
    building_name = models.CharField(max_length=30)
    street_name = models.CharField(max_length=30)
    suburb = models.CharField(max_length=30)
    province = models.OneToOneField(Province, on_delete=models.CASCADE)
    city = models.CharField(max_length=30)
    zip_code = models.IntegerField()


class UserRole(models.Model):
    name = models.CharField(max_length=15)


class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    contact_number = models.CharField(max_length=40)
    physical_address = models.OneToOneField(PhysicalAddress, \
    on_delete=models.CASCADE)


class Financier(Client):
    company_name = models.CharField(max_length=30)
    company_reg = models.CharField(max_length=40)
    web_address = models.URLField(null=True)
    role = models.OneToOneField(UserRole, on_delete=models.CASCADE, null=True)


class Service(models.Model):
    name = models.CharField(max_length=100)


class System(models.Model):
    name = models.CharField(max_length=100)


class SupplierInstallerSystem(models.Model):
    system = models.ForeignKey(System, on_delete=models.CASCADE)
    service = models.PositiveSmallIntegerField()


class SupplierInstaller(Financier):
    systems = models.ManyToManyField(SupplierInstallerSystem)


class Appliance(models.Model):
    name = models.CharField(max_length=30)


class SystemOrder(models.Model):
    need_finance = models.BooleanField(default=False)
    include_installation = models.BooleanField(default=False)


class GeyserSystemOrder(SystemOrder):
    property_type = models.CharField(max_length=10)
    roof_inclination = models.CharField(max_length=10)
    existing_geyser = models.BooleanField()
    new_system = models.BooleanField()
    water_collector = models.CharField(max_length=30)
    current_geyser_size = models.PositiveSmallIntegerField(null=True)
    users_number = models.PositiveSmallIntegerField(null=True)
    required_geyser_size = models.PositiveSmallIntegerField(null=True)
    same_as_existing = models.BooleanField()


class PVTSystem(SystemOrder):
    intended_use = models.CharField(max_length=50)
    possible_appliances = models.ManyToManyField(Appliance)
    site_visit = models.BooleanField()
    property_type = models.CharField(max_length=10)
    roof_inclination = models.CharField(max_length=10)


class SolarComponent(SystemOrder):
    name = models.CharField(max_length=30)

    
class Order(models.Model):
    order_number = models.AutoField(primary_key=True)
    client = models.OneToOneField(Client, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)


class OrderItem(models.Model):
    order = models.ForeignKey(Order)
    system = models.OneToOneField(SystemOrder, on_delete=models.CASCADE)
