from django.db import models
from django.contrib.postgres.fields import JSONField
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Sum, F
from django.utils import timezone

class Vendor(models.Model):
    name = models.CharField(max_length=100)
    contact_details = models.TextField()
    address = models.TextField()
    vendor_code = models.CharField(max_length=50, unique=True)
    on_time_delivery_rate = models.FloatField()
    quality_rating_avg = models.FloatField()
    average_response_time = models.FloatField()
    fulfillment_rate = models.FloatField()

    def __str__(self):
        return self.name

    def update_on_time_delivery_rate(self):
        completed_pos = self.purchase_orders.filter(status='completed')
        on_time_deliveries = completed_pos.filter(delivery_date__lte=F('delivery_date'))
        total_completed = completed_pos.count()
        on_time_count = on_time_deliveries.count()

        if total_completed > 0:
            on_time_delivery_rate = (on_time_count / total_completed) * 100
        else:
            on_time_delivery_rate = 0.0

        self.on_time_delivery_rate = on_time_delivery_rate
        self.save()

    def update_quality_rating_avg(self):
        completed_pos = self.purchase_orders.filter(status='completed')
        total_quality_rating = completed_pos.aggregate(total=Sum('quality_rating'))['total'] or 0
        count = completed_pos.count()

        if count > 0:
            quality_rating_avg = total_quality_rating / count
        else:
            quality_rating_avg = 0.0

        self.quality_rating_avg = quality_rating_avg
        self.save()

    def update_average_response_time(self):
        acknowledged_pos = self.purchase_orders.exclude(acknowledgment_date__isnull=True)
        total_response_time = acknowledged_pos.aggregate(
            total=Sum(F('acknowledgment_date') - F('issue_date'))
        )['total']
        count = acknowledged_pos.count()

        if count > 0:
            average_response_time = total_response_time / count
        else:
            average_response_time = 0.0

        self.average_response_time = round(average_response_time.total_seconds() / 3600, 2)   # Convert to hours  # Convert to hours
        self.save()

    def update_fulfillment_rate(self):
        fulfilled_pos = self.purchase_orders.filter(status='completed')
        total_pos = self.purchase_orders.count()

        if total_pos > 0:
            fulfillment_rate = (fulfilled_pos.count() / total_pos) * 100
        else:
            fulfillment_rate = 0.0

        self.fulfillment_rate = fulfillment_rate
        self.save()

class PurchaseOrder(models.Model):
    po_number = models.CharField(max_length=50, unique=True)
    vendor = models.ForeignKey(Vendor, related_name='purchase_orders', on_delete=models.CASCADE)
    order_date = models.DateTimeField()
    delivery_date = models.DateTimeField()
    items = models.JSONField()
    quantity = models.IntegerField()
    status = models.CharField(max_length=50)
    quality_rating = models.FloatField(null=True, blank=True)
    issue_date = models.DateTimeField()
    acknowledgment_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'PO {self.po_number} - {self.vendor.name}'

class HistoricalPerformance(models.Model):
    vendor = models.ForeignKey(Vendor, related_name='historical_performance', on_delete=models.CASCADE)
    date = models.DateTimeField()
    on_time_delivery_rate = models.FloatField()
    quality_rating_avg = models.FloatField()
    average_response_time = models.FloatField()
    fulfillment_rate = models.FloatField()

    def __str__(self):
        return f'Historical Performance - {self.vendor.name} on {self.date}'

@receiver(post_save, sender=PurchaseOrder)
def calculate_performance_metrics(sender, instance, **kwargs):
    if instance.status == 'completed':
        vendor = instance.vendor
        vendor.update_on_time_delivery_rate()
        if instance.quality_rating is not None:
            vendor.update_quality_rating_avg()

    if instance.acknowledgment_date is not None:
        vendor = instance.vendor
        vendor.update_average_response_time()

    vendor = instance.vendor
    vendor.update_fulfillment_rate()