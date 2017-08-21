from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from app import serializers, models

from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response


class GetProductBrand(generics.ListAPIView):
    serializer_class = serializers.ProductBrandSerializer
    permissions = (IsAuthenticated,)

    def get_queryset(self):
        brand_id = self.kwargs['brand_id']
        return models.ProductBrand.objects.filter(id=brand_id)


class GetOrderDetails(generics.ListAPIView):
    serializer_class = serializers.OrderSerializer
    permissions = (IsAuthenticated,)

    def get_queryset(self):
        order_number = self.kwargs['order_number']
        return models.Order.objects.filter(order_number=order_number)


class GetSystemOrderDetails(generics.ListAPIView):
    serializer_class = serializers.SystemOrderSerializer
    permissions = (IsAuthenticated,)

    def get_queryset(self):
        order_number = self.kwargs['order_number']
        return models.SystemOrder.objects.filter(order_number=order_number)


class GetClientDetails(generics.ListAPIView):
    serializer_class = serializers.ClientSerializer
    permissions = (IsAuthenticated,)

    def get_queryset(self):
        client_id = self.kwargs['id']
        return models.Client.objects.filter(client_id=client_id)


class GetClientAddress(generics.ListAPIView):
    serializer_class = serializers.AddressSerializer
    permissions = (IsAuthenticated,)

    def get_queryset(self):
        address_id = self.kwargs['id']
        return models.PhysicalAddress.objects.filter(address_id=address_id)


class GetMyProducts(generics.ListAPIView):
    serializer_class = serializers.SellingProductSerializer
    permissions  = (IsAuthenticated,)

    def get_queryset(self):
        user = models.SpazrUser.objects.get(user=self.request.user)
        return models.SellingProduct.objects.filter(user=user)


"""
@api_view(['GET', 'POST'])
def system_order_details(request, order_num):
    
    system_order = models.SystemOrder.objects.all()
    """
