from django.contrib import admin
from.models import Vendor, PurchaseOrder, HistoricalPerformance


@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact_details', 'address', 'vendor_code', 'on_time_delivery_rate', 'quality_rating_avg', 'average_response_time', 'fulfillment_rate', 'created_at', 'updated_at')
    list_filter = ('on_time_delivery_rate',)
    search_fields = ('name', 'vendor_code', 'created_at', 'updated_at')


@admin.register(PurchaseOrder)
class PurchaseOrderAdmin(admin.ModelAdmin):
    list_display = ('po_number', 'vendor', 'order_date', 'delivery_date', 'items', 'quantity', 'status', 'quality_rating', 'issue_date', 'acknowledgment_date', 'created_at', 'updated_at')
    list_filter = ('status',)
    search_fields = ('po_number', 'vendor__name', 'created_at', 'updated_at')


@admin.register(HistoricalPerformance)
class HistoricalPerformanceAdmin(admin.ModelAdmin):
    list_display = ('vendor', 'date', 'on_time_delivery_rate', 'quality_rating_avg', 'average_response_time', 'fulfillment_rate', 'created_at', 'updated_at')
    list_filter = ('on_time_delivery_rate',)
    search_fields = ('vendor__name', 'date', 'created_at', 'updated_at')
