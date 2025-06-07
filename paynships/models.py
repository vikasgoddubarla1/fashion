from django.db import models
from orders.models import Order
# Create your models here.
class Payment(models.Model):
    order_id = models.OneToOneField(Order, on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=50)
    payment_id = models.CharField(max_length=100, null=True, blank=True)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50)
    paid_at = models.DateTimeField(auto_now_add=True)


class Shipment(models.Model):
    order_id = models.OneToOneField(Order, on_delete=models.CASCADE)
    courier_name = models.CharField(max_length=100)
    tracking_id = models.CharField(max_length=100)
    estimated_delivery = models.DateTimeField(null=True, blank=True)
    shipped_at = models.DateTimeField(null=True, blank=True)
    delivered_at = models.DateTimeField(null=True, blank=True)