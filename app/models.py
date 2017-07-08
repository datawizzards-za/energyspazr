from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User, Group


class Province(models.Model):
    name = models.CharField(max_length=30)


class PhysicalAddress(models.Model):
    building_name = models.CharField(max_length=30)
    street_name = models.CharField(max_length=30)
    suburb = models.CharField(max_length=30)
    province = models.ForeignKey(Province, on_delete=models.CASCADE)
    city = models.CharField(max_length=30)
    zip_code = models.IntegerField()


class Client(models.Model):
    username = models.CharField(max_length=30)
    lastname = models.CharField(max_length=30)
    firstname = models.CharField(max_length=30)
    contact_number = models.CharField(max_length=40)
    physical_address = models.OneToOneField(PhysicalAddress, \
                                            on_delete=models.CASCADE)


class SpazrUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    contact_number = models.CharField(max_length=40)
    physical_address = models.OneToOneField(PhysicalAddress, \
                                            on_delete=models.CASCADE)
    company_name = models.CharField(max_length=30)
    company_reg = models.CharField(max_length=40)
    web_address = models.URLField(null=True)


class ProductBrand(models.Model):
    name = models.CharField(max_length=100, primary_key=True)


class Product(models.Model):
    name = models.CharField(max_length=100, primary_key=True)


class SpazrUserProduct(models.Model):
    user = models.ForeignKey(SpazrUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.FloatField()
    brand = models.ForeignKey(ProductBrand, on_delete=models.CASCADE)


class PanelSize(models.Model):
    value = models.FloatField()


class InverterSize(models.Model):
    value = models.CharField(max_length=20)


class BatterySize(models.Model):
    value = models.IntegerField()


class SolarPanel(SpazrUserProduct):
    size = models.ForeignKey(PanelSize, on_delete=models.CASCADE)


class Inverter(SpazrUserProduct):
    size = models.ForeignKey(InverterSize, on_delete=models.CASCADE)


class Battery(SpazrUserProduct):
    size = models.ForeignKey(BatterySize, on_delete=models.CASCADE)


class DCCable(SpazrUserProduct):
    size = models.FloatField()
    length = models.FloatField()


class System(models.Model):
    name = models.CharField(max_length=100)


class SupplierInstallerSystem(models.Model):
    system = models.ForeignKey(System, on_delete=models.CASCADE)
    service = models.PositiveSmallIntegerField()


class SupplierInstaller(SpazrUser):
    systems = models.ManyToManyField(SupplierInstallerSystem)


class Appliance(models.Model):
    name = models.CharField(max_length=30)


class SystemOrder(models.Model):
    need_finance = models.BooleanField(default=False)
    include_installation = models.BooleanField(default=False)


class GeyserSystemOrder(SystemOrder):
    property_type = models.CharField(max_length=10)
    roof_inclination = models.CharField(max_length=10)
    users_number = models.PositiveSmallIntegerField(null=True)
    required_geyser_size = models.PositiveSmallIntegerField(null=True)
    water_collector = models.CharField(max_length=15)


class PVTSystem(SystemOrder):
    intended_use = models.CharField(max_length=50)
    possible_appliances = models.ManyToManyField(Appliance)
    site_visit = models.BooleanField()
    property_type = models.CharField(max_length=10)
    roof_inclination = models.CharField(max_length=10)


class SolarComponentOrder(SystemOrder):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    
class Order(models.Model):
    order_number = models.AutoField(primary_key=True)
    client = models.OneToOneField(Client, on_delete=models.CASCADE)
    supplier = models.ForeignKey(SpazrUser)
    date = models.DateField(auto_now_add=True)


class OrderItem(models.Model):
    order = models.ForeignKey(Order)
    system = models.OneToOneField(SystemOrder, on_delete=models.CASCADE)
