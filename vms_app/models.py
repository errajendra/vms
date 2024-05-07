from django.db import models
from django.utils.translation import gettext_lazy as _



class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Vendor(BaseModel):
    name = models.CharField(max_length=255)
    contact_details = models.CharField(
        max_length=150,
        help_text=_("- Contact information of the vendor.")
    )
    address = models.TextField()
    vendor_code = models.CharField(max_length=50, unique=True)
    on_time_delivery_rate = models.FloatField(
        help_text=_("Tracks the percentage of on-time deliveries."))
    quality_rating_avg = models.FloatField(
        help_text=_("Average rating of quality based on purchase orders."))
    average_response_time = models.FloatField(
        help_text=_("Average time taken to acknowledge purchase orders."))
    fulfillment_rate = models.FloatField(
        help_text=_("Percentage of purchase orders fulfilled successfully."))

    def __str__(self):
        return self.name


class PurchaseOrder(BaseModel):
    STATUS_CHOICES = [
        ('PENDING', 'PENDING'),
        ('COMPLETED', 'COMPLETED'),
        ('CANCELED', 'CANCELED'),
    ]

    po_number = models.CharField(max_length=100, unique=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    order_date = models.DateTimeField()
    delivery_date = models.DateTimeField()
    items = models.JSONField()
    quantity = models.IntegerField()
    status = models.CharField(max_length=50, choices=STATUS_CHOICES)
    quality_rating = models.FloatField(null=True, blank=True)
    issue_date = models.DateTimeField()
    acknowledgment_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"PO {self.po_number} for {self.vendor.name}"


class HistoricalPerformance(BaseModel):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    date = models.DateTimeField()
    on_time_delivery_rate = models.FloatField()
    quality_rating_avg = models.FloatField()
    average_response_time = models.FloatField()
    fulfillment_rate = models.FloatField()

    def __str__(self):
        return f"{self.vendor.name} - {self.date}"
