from rest_framework import serializers
from .models import Vendor,PurchaseOrder,HistoricalPerformance

class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = ['id', 'name', 'contact_details', 'address', 'vendor_code',
                  'on_time_delivery_rate', 'quality_rating_avg',
                  'average_response_time', 'fulfillment_rate']


class PurchaseOrderSerializer(serializers.ModelSerializer):
    vendor = VendorSerializer(read_only=True)
    class Meta:
        model = PurchaseOrder
        fields = ['id', 'po_number', 'vendor', 'order_date', 'delivery_date', 'items', 'quantity', 'status', 'quality_rating', 'issue_date', 'acknowledgment_date']


class HistoricalPerformanceSerializer(serializers.ModelSerializer):
    vendor = VendorSerializer(read_only=True)
    class Meta:
        model = HistoricalPerformance
        fields = ['id', 'endor', 'date', 'on_time_delivery_rate', 'quality_rating_avg', 'average_response_time', 'fulfillment_rate']

class VendorPerformanceSerializer(serializers.Serializer):
    on_time_delivery_rate = serializers.DecimalField(max_digits=5, decimal_places=2)
    quality_rating_avg = serializers.DecimalField(max_digits=5, decimal_places=2)
    average_response_time = serializers.DecimalField(max_digits=10, decimal_places=2)
    fulfillment_rate = serializers.DecimalField(max_digits=5, decimal_places=2)