from django.urls import path, include

urlpatterns = [
    path('api/v1/', include('vendor.urls')),
    path('api/v1/', include('purchaseorder.urls')),
]
