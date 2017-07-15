from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User, Group

import uuid


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


class Product(models.Model):
    name = models.CharField(max_length=100, primary_key=True)

    def natural_key(self):
        return (self.name)


class ProductBrandName(models.Model):
    name = models.CharField(max_length=100, primary_key=True)

    def natural_key(self):
        return (self.name)


class ProductBrandManager(models.Manager):
    def get_by_natural_key(self, name, product):
        return self.get(name=name, product=product)


class ProductBrand(models.Model):
    objects = ProductBrandManager()

    name = models.ForeignKey(ProductBrandName, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def natural_key(self):
        return (self.name, self.product)

    class Meta:
        unique_together = (('name', 'product'),)


class DimensionName(models.Model):
    name = models.CharField(max_length=100, primary_key=True)

    def natural_key(self):
        return (self.name)


class DimensionManager(models.Manager):
    def get_by_natural_key(self, name, value):
        return self.get(name=name, value=value)


class Dimension(models.Model):
    objects = DimensionManager()

    name = models.ForeignKey(DimensionName, on_delete=models.CASCADE)
    value = models.CharField(max_length=100)

    def natural_key(self):
        return (self.name, self.value)

    class Meta:
        unique_together = (('name', 'value'),)


class GeneralProduct(models.Model):
    brand = models.ForeignKey(ProductBrand, on_delete=models.CASCADE)
    dimensions = models.ManyToManyField(Dimension)


'''
class InverterSize(models.Model):
    value = models.CharField(max_length=20)


class Inverter(models.Model):
    size = models.ForeignKey(InverterSize, on_delete=models.CASCADE)
    brand = models.ForeignKey(ProductBrand, on_delete=models.CASCADE)


class BatterySize(models.Model):
    value = models.IntegerField()


class Battery(models.Model):
    size = models.ForeignKey(BatterySize, on_delete=models.CASCADE)
    brand = models.ForeignKey(ProductBrand, on_delete=models.CASCADE)


class DCCable(models.Model):
    size = models.FloatField()
    length = models.FloatField()
    brand = models.ForeignKey(ProductBrand, on_delete=models.CASCADE)


class Connector(models.Model):
    size = models.FloatField()
    length = models.FloatField()
    brand = models.ForeignKey(ProductBrand, on_delete=models.CASCADE)


class Combiner(models.Model):
    size = models.FloatField()
    length = models.FloatField()
    brand = models.ForeignKey(ProductBrand, on_delete=models.CASCADE)
'''

class SellingProduct(models.Model):
    user = models.ForeignKey(SpazrUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.FloatField()


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
    order_number = models.CharField(max_length=100, primary_key=True, default=uuid.uuid4)
    #order_number = models.AutoField(primary_key=True)
    #order_number = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)


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
    order_number = models.ForeignKey(SystemOrder, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    supplier = models.ForeignKey(SpazrUser)
    date = models.DateField(auto_now_add=True)
