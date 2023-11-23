from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Vendor

class CreateVendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = ['vendorName', 'vendorContact', 'address', 'password']
    exclude = ['on_time_delivery_rate', 'quality_rating_avg', 'average_response_time', 'fulfillment_rate']

    def validate(self, data):
        vendorName = data.get('vendorName')
        vendorContact = data.get('vendorContact')
        address = data.get('address')

        if not vendorName:
            raise serializers.ValidationError('Please provide a vendor name')

        if not vendorContact or not address:
            raise serializers.ValidationError("vendorContact and address fields can't be empty")

        existing_vendor = Vendor.objects.filter(vendorContact=vendorContact).first()

        if existing_vendor:
            raise serializers.ValidationError('Vendor with this contact already exists')

        password = data.get('password')
        data['password'] = make_password(password)

        if vendorContact and Vendor.objects.filter(vendorContact=vendorContact).exists():
            raise serializers.ValidationError({'message': 'Vendor contact already exists'})

        return data

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response.pop('password', None)
        return response



class VendorLoginSerializer(serializers.Serializer):
    vendorContact = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        vendorContact = data.get('vendorContact')
        password = data.get('password')

        if not vendorContact or not password:
            raise serializers.ValidationError('Please enter "vendorContact" and "password".')

        if vendorContact and password:
            vendor = authenticate(request=self.context.get('request'), vendorContact=vendorContact, password=password)
            if vendor:
                    refresh = RefreshToken.for_user(vendor)

                    return {
                            'message': 'Login successful.',
                            'username': vendor.vendorName,
                            'access': str(refresh.access_token),
                            'refresh': str(refresh),
                            }
            else:
                raise serializers.ValidationError('Incorrect vendorContact or password.')
        else:
            raise serializers.ValidationError(' Please enter "vndorContact" and "password".')


class GetVendorSerializer(serializers.ModelSerializer): 
    class Meta: 
        model = Vendor
        fields = '__all__'
