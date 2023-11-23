import uuid
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class VendorManager(BaseUserManager):
    def create_user(self, vendorContact, password=None, **extra_fields):
        if not vendorContact:
            raise ValueError('The vendorContact field must be set')
        email = self.normalize_email(vendorContact)
        user = self.model(vendorContact=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, vendorContact, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(vendorContact, password, **extra_fields)

class Vendor(AbstractBaseUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    vendor_code = models.UUIDField(default=uuid.uuid4, editable=False)
    vendorName = models.CharField(max_length=200, blank=False)
    vendorContact = models.EmailField(max_length=254, unique=True, blank=False) 
    address = models.TextField(blank=False)
    password = models.CharField(max_length=355, blank=False)
    on_time_delivery_rate = models.FloatField(default=0.0, validators=[MinValueValidator(0.0), MaxValueValidator(5.0)])
    quality_rating_avg = models.FloatField(default=0.0, validators=[MinValueValidator(0.0), MaxValueValidator(5.0)])
    average_response_time = models.FloatField(default=0.0)
    fulfillment_rate = models.FloatField(default=0.0, validators=[MinValueValidator(0.0), MaxValueValidator(1.0)])

    objects = VendorManager()

    USERNAME_FIELD = 'vendorContact'


