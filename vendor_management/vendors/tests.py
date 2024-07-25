from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from rest_framework import status
from .models import Vendor, PurchaseOrder
from .serializers import VendorSerializer, PurchaseOrderSerializer
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

class TestVendorViews(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='Vendor', password='123456')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.vendor_url = reverse('vendor-list')

    def test_create_vendor(self):
        data = {
            'vendor_code': 'UNIQUE_CODE_001',  # Ensure this code is unique
            'name': 'Test Vendor',
            'contact_details': 'test@example.com',
            'address': '123 Main St',
            'on_time_delivery_rate': 95.0,
            'quality_rating_avg': 4.5,
            'average_response_time': 2.0,
            'fulfillment_rate': 90.0
        }
        response = self.client.post(self.vendor_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Vendor.objects.count(), 1)

    def test_get_vendors(self):
        Vendor.objects.create(vendor_code='UNIQUE_CODE_002', name='Test Vendor 2', contact_details='test2@example.com',
                              address='456 Main St')
        response = self.client.get(self.vendor_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

class TestPurchaseOrderViews(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.purchase_order_url = reverse('purchase-order-list')
        self.vendor = Vendor.objects.create(
            vendor_code='UNIQUE_CODE_002',
            name='Test Vendor',
            contact_details='test@example.com',
            address='123 Main St',
            on_time_delivery_rate=95.0,
            quality_rating_avg=4.5,
            average_response_time=2.0,
            fulfillment_rate=90.0
        )


class TestPurchaseOrderViews(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_authenticate(user=self.user)
        self.purchase_order_url = reverse('purchase-order-list')

        self.vendor = Vendor.objects.create(
            vendor_code='UNIQUE_CODE_002',
            name='Test Vendor',
            contact_details='test@example.com',
            address='123 Main St',
            on_time_delivery_rate=95.0,
            quality_rating_avg=4.5,
            average_response_time=2.0,
            fulfillment_rate=90.0
        )

    def test_create_purchase_order(self):
        data = {
            'po_number': 'PO123',
            'vendor': self.vendor.id,  # Reference the vendor ID
            'order_date': '2022-01-01T00:00:00Z',
            'delivery_date': '2022-01-15T00:00:00Z',
            'items': [{'item': 'Item 1', 'quantity': 2}],
            'quantity': 5,
            'status': 'open',
            'issue_date': '2022-01-01T00:00:00Z',
        }
        response = self.client.post(self.purchase_order_url, data, format='json')
        print(response.data)  # For debugging purposes
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(PurchaseOrder.objects.count(), 1)



