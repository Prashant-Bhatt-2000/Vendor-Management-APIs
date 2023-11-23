from django.urls import path
from .views import CreatePurchaseOrder, GetAllPurchaseOrder, GetPurchaseOrderById, UpdatePurchaseOrder, DeletePurchaseOrder, OrderStatusUpdate, QualityRating

urlpatterns = [
    path('purchaseorder', CreatePurchaseOrder.as_view(), name='purchase_order'),
    path('getallorders', GetAllPurchaseOrder.as_view(), name='getorders'),
    path('getorder/<str:orderid>', GetPurchaseOrderById.as_view(), name='getordersbyid'), 
    path('updateorder/<str:orderid>', UpdatePurchaseOrder.as_view(), name='updateordersbyid'), 
    path('deleteorder/<str:orderid>', DeletePurchaseOrder.as_view(), name='deleteordersbyid'), 
    path('orderstatus/<str:orderid>', OrderStatusUpdate.as_view(), name='orderStatus'),
    path('qualityrating/<str:po_number>', QualityRating.as_view(), name='qualityRating')
]
