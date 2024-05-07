from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.db.models import F, Avg, ExpressionWrapper, fields
from django.utils import timezone
from datetime import timedelta
from vms_app.models import PurchaseOrder, HistoricalPerformance




@receiver(pre_save, sender=PurchaseOrder)
def action_on_po_pre_save(sender, instance=None, **kwargs):
    if instance.pk is not None:
        old_instance = PurchaseOrder.objects.get(pk=instance.pk)
        changed_fields = [field.name for field in instance._meta.fields if getattr(instance, field.name)!= getattr(old_instance, field.name)]
        vendor = instance.vendor
        
        # Create or update Historical Performance for purticular date
        hist_perf = HistoricalPerformance.objects.filter(vendor=vendor, date=timezone.now().date()).first()
        if hist_perf is None:
            hist_perf = HistoricalPerformance(
                vendor = vendor,
                date = timezone.now().date(),
                on_time_delivery_rate = vendor.on_time_delivery_rate,
                quality_rating_avg = vendor.quality_rating_avg,
                average_response_time = vendor.average_response_time,
                fulfillment_rate = vendor.fulfillment_rate
            )
            hist_perf.save()
                
        if "status" in changed_fields:
            if instance.status == "COMPLETED":
                """
                    Calculate On-Time Delivery Rate.
                    Logic: Count the number of completed POs delivered on or before delivery_date and
                    divide by the total number of completed POs for that vendor.
                """
                on_time_delivered_pos = PurchaseOrder.objects.filter(
                    status="COMPLETED", delivery_date__gte=F('acknowledgment_date'))
                v_on_time_delivered_pos = on_time_delivered_pos.filter(vendor=vendor)
                try:
                    on_time_delivery_rate = on_time_delivered_pos.count() / v_on_time_delivered_pos.count()
                except ZeroDivisionError:
                    on_time_delivery_rate = 0
                
                vendor.on_time_delivery_rate = on_time_delivery_rate
                hist_perf.on_time_delivery_rate = on_time_delivery_rate
                
                
        """
            Calculate Quality Rating Average:
            ● Updated upon the completion of each PO where a quality_rating is provided.
            ● Logic: Calculate the average of all quality_rating values for completed POs of the vendor.
        """
        if "quality_rating" in changed_fields and instance.status =="COMPLETED":
            v_quality_rating = vendor.purchaseorder_set.filter(status="COMPLETED").aggregate(Avg('quality_rating'))["quality_rating__avg"] or 0
            vendor.quality_rating_avg = v_quality_rating  
            hist_perf.quality_rating_avg = v_quality_rating           


        """
        Calculate Average Response Time:
        ● Calculated each time a PO is acknowledged by the vendor.
        ● Logic: Compute the time difference between issue_date and
            acknowledgment_date for each PO, and then find the average of these times
            for all POs of the vendor.
        """
        if "acknowledgment_date" in changed_fields:
            average_response_time = vendor.purchaseorder_set.all().annotate(
                time_difference=ExpressionWrapper(
                    F('acknowledgment_date') - F('issue_date'),
                    output_field=fields.DurationField()
                )
            ).aggregate(Avg("time_difference"))["time_difference__avg"] or None
            
            if average_response_time:
                average_response_time_days = timedelta(seconds=average_response_time.total_seconds()) / timedelta(days=1)
                vendor.average_response_time = average_response_time_days
                hist_perf.average_response_time = average_response_time_days


        """
        Calculate Fulfilment Rate:
        ● Calculated upon any change in PO status.
        ● Logic: Divide the number of successfully fulfilled POs (status 'completed'
            without issues) by the total number of POs issued to the vendor.
        """
        if changed_fields:
            on_time_deliveries = vendor.purchaseorder_set.filter(delivery_date__lte=timezone.now(), status='COMPLETED').count()
            total_po = vendor.purchaseorder_set.count()
            fulfilment_rate = on_time_deliveries / total_po if total_po > 0 else 0
            vendor.fulfillment_rate = fulfilment_rate
            hist_perf.fulfillment_rate = fulfilment_rate
        
        vendor.save()
        hist_perf.save()
