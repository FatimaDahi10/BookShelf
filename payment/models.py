from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
import datetime
from store.models import Product


class ShippingAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    shipping_name_surname = models.CharField(max_length=200)
    shipping_phone_number = models.CharField(max_length=200)
    shipping_email = models.EmailField(max_length=200)
    shipping_address = models.CharField(max_length=200)
    shipping_city = models.CharField(max_length=200)
    shipping_country = models.CharField(max_length=200)
    shipping_zipcode = models.CharField(max_length=200)

    class Meta:
        verbose_name_plural = "Shipping Address"

    def __str__(self):
        return f'Shipping Address - {str(self.id)}'


# crea user deafult, automaticamente
def create_shipping(sender, instance, created, **kwargs):
    if created:
        user_shipping = ShippingAddress(user=instance)
        user_shipping.save()


# automate the profile
post_save.connect(create_shipping, sender=User)


# Modello Ordini
class Order_P(models.Model):
    # foreign key
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    name_surname = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    shipping_address = models.TextField(max_length=15000)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    date_ordered = models.DateField(auto_now_add=True)
    date_shipped = models.DateField(blank=True, null=True)
    data_received = models.DateField(blank=True, null=True)


    # admin section
    def __str__(self):
        return f'Order - {str(self.id)}'


# Modello OrderItem (i prodotti che sono stati acquistati)
class OrderItem(models.Model):
    # Foreign key
    order = models.ForeignKey(Order_P, on_delete=models.CASCADE, null=True, related_name="order_items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)

    buyer = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="purchased_items")
    supplier = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="supplied_items")

    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    shipped = models.BooleanField(default=False)
    message_read = models.BooleanField(default=False)
    update_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.product} - {self.buyer.username} -> {self.supplier.username}"




