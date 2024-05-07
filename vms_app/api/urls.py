from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    VendorView, PurchaseOrderView,
)

router = DefaultRouter()

router.register("venders", VendorView, basename="venders")
router.register("purchase_orders", PurchaseOrderView, basename="purchase_orders")


urlpatterns = [
    path('', include(router.urls)),
]
