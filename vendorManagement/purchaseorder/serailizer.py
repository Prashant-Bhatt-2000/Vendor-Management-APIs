
from rest_framework import serializers
from .models import PurchaseOrder
from decimal import Decimal
import json
from datetime import date

class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Decimal):
            return float(o)
        return super().default(o)

class ItemSerializer(serializers.Serializer):
    name = serializers.CharField()
    price = serializers.FloatField()
    quantity = serializers.IntegerField(default=1)

class PurchaseOrderSerializer(serializers.ModelSerializer):
    items = ItemSerializer(many=True)
    delivery_date = serializers.DateField()

    class Meta:
        model = PurchaseOrder
        fields = ['vendor', 'items', 'delivery_date', 'issue_date']

    def validate(self, data):
        vendor = data['vendor']
        delivery_date = data.get('delivery_date')

        if not vendor:
            raise serializers.ValidationError('Vendor field is empty')

        if delivery_date and delivery_date < date.today():
            raise serializers.ValidationError('Delivery date cannot be in the past')
        
        data['issue_date'] = data.get('issue_date', date.today())

        return data

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        
        representation['items'] = json.loads(json.dumps(representation['items'], cls=DecimalEncoder))
        return representation



from rest_framework import serializers
from .models import PurchaseOrder


class GetPurchaseOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrder
        fields = '__all__'


