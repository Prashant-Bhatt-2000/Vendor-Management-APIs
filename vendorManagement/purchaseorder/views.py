from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serailizer import PurchaseOrderSerializer, GetPurchaseOrderSerializer
from .models import PurchaseOrder
from vendor.models import Vendor
from datetime import date


# Create your views here.

class CreatePurchaseOrder(APIView):
    def post(self, request):
        purchase_order_data = request.data
        serializer = PurchaseOrderSerializer(data=purchase_order_data)

        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Order created successfully', 'order': serializer.data}, status=status.HTTP_201_CREATED)

        return Response({'message': 'Error', 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    

class GetAllPurchaseOrder(APIView): 
    def get(self, request):
        orders = PurchaseOrder.objects.all()

        if orders: 
            serializer = GetPurchaseOrderSerializer(orders, many=True)
            return Response(serializer.data)
    
        return Response({ 'message': 'No Orders Found'}, status=status.HTTP_400_BAD_REQUEST)
    

class GetPurchaseOrderById(APIView):
    def get(self, request, orderid):
        try:
            order = PurchaseOrder.objects.get(po_number=orderid)
            serializer = GetPurchaseOrderSerializer(order)
            return Response(serializer.data)
        except PurchaseOrder.DoesNotExist:
            return Response({'message': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)
        


class UpdatePurchaseOrder(APIView):
    def put(self, request, orderid):
        try:
            order = PurchaseOrder.objects.get(po_number=orderid)
            serializer = PurchaseOrderSerializer(order, data=request.data, partial=True)
        
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'Order updated successfully'}, status=status.HTTP_200_OK)
        except: 
            return Response({'message': 'Order not found'})
        

class DeletePurchaseOrder(APIView): 
    def delete(self, request, orderid):
        try:
            order = PurchaseOrder.objects.get(po_number=orderid)
            order.delete()
            return Response({'message': 'Order deleted'})
        except PurchaseOrder.DoesNotExist:
            return Response({'message': 'Order Not Found'}, status=status.HTTP_400_BAD_REQUEST)

class OrderStatusUpdate(APIView):
    def post(self, request, orderid):
        try:
            order = PurchaseOrder.objects.get(po_number=orderid)
            if request.data['status'] == "completed":
                order.status = "completed"
                order.delivered_on = date.today()
                order.save()

                # calculating ontimeDeliveryrate
                vendor = Vendor.objects.get(id=order.vendor_id)

                # count Completed Pos
                completed_pos_count = PurchaseOrder.objects.filter(vendor=vendor, status='completed').count()
                on_time_completed_pos_count = PurchaseOrder.objects.filter(
                    vendor=vendor,
                    status='completed',
                    delivered_on__lte=order.delivery_date
                ).count()

                # Updating on-time delivery rate if there are completed POs
                if completed_pos_count > 0 and vendor.on_time_delivery_rate == 0:
                    on_time_delivery_rate = min((on_time_completed_pos_count / completed_pos_count) * 100, 100.0)
                    vendor.on_time_delivery_rate = on_time_delivery_rate
                    vendor.save()
                
                #Fulfilment Rate:
                # ● Calculated upon any change in PO status.
                # ● Logic: Divide the number of successfully fulfilled POs (status 'completed'
                # without issues) by the total number of POs issued to the vendor.

                successfull_pos_count = PurchaseOrder.objects.filter(vendor=vendor, status='completed').count()
                total_pos_count = PurchaseOrder.objects.filter(vendor=vendor).count()
                fullfillmentRate = successfull_pos_count / total_pos_count

                vendor.fulfillment_rate = fullfillmentRate

                vendor.save()


            elif request.data['status'] == "cancelled": 
                order.status = "cancelled"
                order.save()
            else:
                return Response({'error': 'Invalid Status'}, status=status.HTTP_400_BAD_REQUEST)
        
            return Response({'message': 'Order status updated successfully', 'vendor': order.vendor_id}, status=status.HTTP_200_OK)
        except PurchaseOrder.DoesNotExist:
            return Response({'message': 'Order not found'}, status=status.HTTP_400_BAD_REQUEST)



class QualityRating(APIView):
    def post(self, request, po_number):
        try:
            order = PurchaseOrder.objects.get(po_number=po_number)

            if 0 <= request.data['quality_rating'] <= 5:
                order.quality_rating = request.data['quality_rating']
                order.save()

                vendor = order.vendor

                completed_orders = PurchaseOrder.objects.filter(quality_rating__isnull=False)

                total_quality_rating = sum(po.quality_rating for po in completed_orders)
                vendor.quality_rating_avg = total_quality_rating / completed_orders.count() if completed_orders.count() > 0 else 0

                vendor.save()

                return Response({'message': 'Quality rating updated successfully'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Quality rating should be between 0 and 5'}, status=status.HTTP_400_BAD_REQUEST)

        except PurchaseOrder.DoesNotExist:
            return Response({'error': 'Purchase Order not found'}, status=status.HTTP_404_NOT_FOUND)

