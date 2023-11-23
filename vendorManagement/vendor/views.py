from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .serializer import CreateVendorSerializer, VendorLoginSerializer, GetVendorSerializer
from .models import Vendor
from purchaseorder.models import PurchaseOrder
from datetime import date

class CreateVendor(APIView):
    def post(self, request):
        vendor_data = request.data
        serializer = CreateVendorSerializer(data=vendor_data)

        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Vendor created', 'vendor': serializer.data}, status=status.HTTP_201_CREATED)

        return Response({'message': 'Validation errors', 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)



class VendorLogin(APIView):
    def post(self, request):
        data = request.data
        serializer = VendorLoginSerializer(data=data)
        if serializer.is_valid():
            response_data = serializer.validated_data
            return Response(response_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class GetAllVendors(APIView): 
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        vendors = Vendor.objects.all()

        if vendors: 
            serializer = GetVendorSerializer(vendors, many=True)
            return Response(serializer.data)
    
        return Response({ 'message': 'No vendors Found'}, status=status.HTTP_400_BAD_REQUEST)
    

class GetVendorById(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, vendorid):
        try:
            vendor = Vendor.objects.get(id=vendorid)
            serializer = GetVendorSerializer(vendor)
            return Response(serializer.data)
        except Vendor.DoesNotExist:
            return Response({'message': 'Vendor not found'}, status=status.HTTP_400_BAD_REQUEST)
        

class DeleteVendor(APIView): 
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def delete(self, request, vendorid):
        try:
            vendor = Vendor.objects.get(id=vendorid)
            vendor.delete()
            return Response({'message': 'Vendor deleted'})
        except Vendor.DoesNotExist:
            return Response({'message': 'Vendor not found'},status=status.HTTP_400_BAD_REQUEST)


class UpdateVendor(APIView):
    authentication_classes = [JWTAuthentication] 
    permission_classes = [IsAuthenticated]
    def put(self, request, vendorid):
        try:
            vendor = Vendor.objects.get(id=vendorid)
            serializer = GetVendorSerializer(vendor, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'Vendor Updated successfully', 'data': serializer.data})
        except: 
            return Response({'message': 'Vendor not found'})
        


class AcknowledgeOrder(APIView):

    response_times = []

    def post(self, request, po_number): 
        try:
            order = PurchaseOrder.objects.get(po_number=po_number)
            order.acknowledgment_date = date.today()

            #  response time calculate.
            response_time = (order.acknowledgment_date - order.issue_date).days
            self.response_times.append(response_time)

            # average response time calculate.
            average_response_time = sum(self.response_times) / len(self.response_times)

            vendor = Vendor.objects.get(id=order.vendor_id)
            vendor.average_response_time = average_response_time

            print(vendor.average_response_time)

            vendor.save()

            return Response({'message': 'Order Acknowledged', 'average_response_time': average_response_time})
        except:
            return Response({'message': 'Order not found'})    



class GetVendorPerformance(APIView): 
    def get(self, request, vendorid): 
        try:
            vendor = Vendor.objects.get(id=vendorid)

            return Response({'vendor': vendor.vendorName, 'on_time_delivery_rate': vendor.on_time_delivery_rate, 'quality_rating_avg': vendor.quality_rating_avg, 'average_response_time': vendor.average_response_time, 'fullfillment_rate': vendor.fulfillment_rate})
        except: 
            return Response({'message': 'Vendor Not Found'})

