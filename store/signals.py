from django.db.models.signals import post_save
from django.dispatch import receiver
import datetime
from payment.models import OrderItem

# add date to Orders if all OrderItem are shipped by the supplier
@receiver(post_save, sender=OrderItem)
def update_order_shipping_status(sender, instance, **kwargs):
    order = instance.order

    all_items_shipped = all(item.shipped for item in order.order_items.all())

    if all_items_shipped:
        if not order.date_shipped:
            order.date_shipped = datetime.datetime.now().date()
            order.save()
