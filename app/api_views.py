from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from app import serializers, models


class ListSolarPanels(generics.ListAPIView):
    queryset = models.SolarPanel.objects.all()
    serializer_class = serializers.SolarPanelSerializer
    permissions = (IsAuthenticated,)


class GetProductBrand(generics.ListAPIView):
    serializer_class = serializers.ProductBrandSerializer
    permissions = (IsAuthenticated,)

    def get_queryset(self):
        brand_id = self.kwargs['brand_id']
        return models.ProductBrand.objects.filter(id=brand_id)
