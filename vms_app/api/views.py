from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import (
    VendorSerializer, PurchaseOrderSerializer
)
from ..models import (
    Vendor, PurchaseOrder
)



"""
Define  the API views for vendors here
"""
class VendorView(viewsets.ModelViewSet):
    http_method_names = ("get", "post", "put", "delete")
    serializer_class = VendorSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = Vendor.objects.all()
        return queryset



"""
Define Purchase order related APIs here
"""
class PurchaseOrderView(viewsets.ModelViewSet):
    http_method_names = ("get", "post", "put", "delete")
    permission_classes = [IsAuthenticated]
    serializer_class = PurchaseOrderSerializer
    queryset = PurchaseOrder.objects.all()
