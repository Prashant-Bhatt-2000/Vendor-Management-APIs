from django.urls import path
from .views import CreateVendor, VendorLogin, GetAllVendors, GetVendorById, DeleteVendor, UpdateVendor, AcknowledgeOrder, GetVendorPerformance

urlpatterns = [
    path('createvendor', CreateVendor.as_view(), name='create_vendor'), 
    path('loginvendor', VendorLogin.as_view(), name='login_vendor'), 
    path('getallvendors', GetAllVendors.as_view(), name='getVendors'),
    path('getvendor/<str:vendorid>', GetVendorById.as_view(), name='getVendorbyid'), 
    path('deletevendor/<str:vendorid>', DeleteVendor.as_view(), name='deleteVendorbyid'), 
    path('updatevendor/<str:vendorid>', UpdateVendor.as_view(), name='updateVendorbyid'), 
    path('acknowledgeorder/<str:po_number>', AcknowledgeOrder.as_view(), name='acknowledgeOrder'), 
    path('vendorperformance/<str:vendorid>', GetVendorPerformance.as_view(), name='getVendorPerformance')
]
