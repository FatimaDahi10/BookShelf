from django.contrib import admin
from .models import ShippingAddress, Order_P, OrderItem

# Register models on admin section
admin.site.register(ShippingAddress)
admin.site.register(Order_P)
admin.site.register(OrderItem)


# create OrderItem Inline. For each Order we attach the Order Items
class OrderItemInline(admin.StackedInline):
    model = OrderItem
    extra = 0


# extend order Model
class OrderAdmin(admin.ModelAdmin):
    model = Order_P
    readonly_fields = ["date_ordered"]
    inlines = [OrderItemInline]


# unregister order Model (to make it work on admin)
admin.site.unregister(Order_P)


# re-register Order and OrderAdmin
admin.site.register(Order_P, OrderAdmin)

