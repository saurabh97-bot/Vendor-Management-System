from django.urls import path,include
from. import views

urlpatterns = [
    path('api/vendors/', views.VendorList.as_view()),
    path('api/vendors/<pk>/', views.VendorDetail.as_view()),
    path('api/purchase_orders/', views.PurchaseOrderList.as_view()),
    path('api/purchase_orders/<pk>/', views.PurchaseOrderDetail.as_view()),
    path('api/vendors/<pk>/performance/', views.VendorPerformanceView.as_view()),
    path('api/purchase_orders/<str:po_number>/acknowledge/', views.UpdateAcknowledgmentView.as_view())
]