from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    VendorView, PurchaseOrderView,
    VendorPerformanceAPIView, AcknowledgePurchaseOrderView
)

router = DefaultRouter()

router.register("vendors", VendorView, basename="vendors")
router.register("purchase_orders", PurchaseOrderView, basename="purchase_orders")


urlpatterns = [
    path('', include(router.urls)),
    path('vendors/<int:vendor_id>/performance/',
         VendorPerformanceAPIView.as_view(), name='vendor_performance'),
    path('purchase_orders/<int:po_id>/acknowledge/', 
         AcknowledgePurchaseOrderView.as_view(), name='acknowledge_purchase_order'),
]
