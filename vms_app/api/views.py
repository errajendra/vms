from django.utils import timezone
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from .serializers import (
    VendorSerializer, PurchaseOrderSerializer, VendorPerformanceSerializer,
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



""" 
Vendor Performance Matrix.
"""
class VendorPerformanceAPIView(APIView):
    def get(self, request, vendor_id):
        try:
            print(vendor_id)
            vendor = Vendor.objects.get(id=vendor_id)
        except Vendor.DoesNotExist:
            return Response({'error': 'Vendor not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = VendorPerformanceSerializer(vendor)
        return Response(serializer.data)



class AcknowledgePurchaseOrderView(APIView):
    def post(self, request, po_id):
        try:
            purchase_order = PurchaseOrder.objects.get(id=po_id)
        except PurchaseOrder.DoesNotExist:
            return Response({'error': 'Purchase order not found'}, status=status.HTTP_404_NOT_FOUND)

        # Update acknowledgment date
        purchase_order.acknowledgment_date = timezone.now()
        purchase_order.save()

        return Response({'message': 'Purchase order acknowledged successfully'})
