from django.db import models
import uuid
from vendor.models import Vendor
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from django.core.exceptions import ValidationError

# Create your models here.

class PurchaseOrder(models.Model):
    po_number = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    delivery_date = models.DateField(blank=True, null=True)
    delivered_on = models.DateField(blank=True, null=True)
    items = models.JSONField(blank=False, default=list)
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    quality_rating = models.FloatField(default=0.0, validators=[MinValueValidator(0.0), MaxValueValidator(5.0)])
    issue_date = models.DateField(blank=True, null=True)
    acknowledgment_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"PurchaseOrder {self.po_number}"

    def save(self, *args, **kwargs):
        self.issue_date_before_save = self.issue_date
        super().save(*args, **kwargs)

        if self.acknowledgment_date and self.issue_date != self.issue_date_before_save:
            raise ValidationError('Issue date cannot be modified after acknowledgment')



        
        if self.delivery_date and self.delivery_date < timezone.now().date():
            raise ValidationError('Delivery date cannot be in the past')
            
        super().save(*args, **kwargs)

    