from rest_framework import serializers
from ..models import (
    Vendor, PurchaseOrder, HistoricalPerformance
)



# Define a serializer for the Vendor model
class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = "__all__"
        


# Define a serializer for the PurchaseOrder model
class PurchaseOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrder
        fields = "__all__"
    
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        
        # Serialize the vendor field using the VendorSerializer
        data["vendor"] = VendorSerializer(instance.vendor).data
        return data



# Define a serializer for the Vendor Performance Matrix
class VendorPerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = (
            "on_time_delivery_rate", "quality_rating_avg", "average_response_time",
            "fulfillment_rate"
        )
