from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Vendor, PurchaseOrder
from .serializers import VendorSerializer, PurchaseOrderSerializer, VendorPerformanceSerializer
import datetime
from datetime import datetime

# Create your views here.
class VendorList(APIView):
    def get(self, request):
        vendors = Vendor.objects.all()
        serializer = VendorSerializer(vendors, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = VendorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VendorDetail(APIView):
    def get_object(self, pk):
        try:
            return Vendor.objects.get(pk=pk)
        except Vendor.DoesNotExist:
            return Response({'error': 'Vendor not found'}, status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk):
        vendor = self.get_object(pk)
        serializer = VendorSerializer(vendor)
        return Response(serializer.data)

    def put(self, request, pk):
        vendor = self.get_object(pk)
        serializer = VendorSerializer(vendor, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        vendor = self.get_object(pk)
        vendor.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class PurchaseOrderList(APIView):
    def get(self, request):
        purchase_orders = PurchaseOrder.objects.all()
        serializer = PurchaseOrderSerializer(purchase_orders, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PurchaseOrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PurchaseOrderDetail(APIView):
    def get_object(self, pk):
        try:
            return PurchaseOrder.objects.get(pk=pk)
        except PurchaseOrder.DoesNotExist:
            return Response({'error': 'Purchase Order not found'}, status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk):
        purchase_order = self.get_object(pk)
        serializer = PurchaseOrderSerializer(purchase_order)
        return Response(serializer.data)

    def put(self, request, pk):
        purchase_order = self.get_object(pk)
        serializer = PurchaseOrderSerializer(purchase_order, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        purchase_order = self.get_object(pk)
        purchase_order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class VendorPerformanceView(APIView):
    def get(self, request, pk):
        vendor = Vendor.objects.get(id=pk)
        vendor.update_on_time_delivery_rate()
        vendor.update_quality_rating_avg()
        vendor.update_average_response_time()
        vendor.update_fulfillment_rate()
        data = {
            'on_time_delivery_rate': vendor.on_time_delivery_rate,
            'quality_rating_avg': vendor.quality_rating_avg,
            'average_response_time': vendor.average_response_time,
            'fulfillment_rate': vendor.fulfillment_rate
        }
        serializer = VendorPerformanceSerializer(data=data)
        if serializer.is_valid():
            return Response(serializer.data)
        return Response(serializer.errors)

class UpdateAcknowledgmentView(APIView):
    def post(self, request, po_number):
        try:
            purchase_order = PurchaseOrder.objects.get(po_number=po_number)
        except PurchaseOrder.DoesNotExist:
            return Response({'error': 'Purchase Order not found'}, status=404)
        purchase_order.acknowledgment_date = datetime.now()
        purchase_order.save()
        purchase_order.vendor.update_average_response_time()
        serializer = PurchaseOrderSerializer(purchase_order)
        return Response(serializer.data)