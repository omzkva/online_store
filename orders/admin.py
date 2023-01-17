from django.contrib import admin
from .models import Order, OrderItem
from django.utils.safestring import mark_safe

from django.urls import reverse

def order_detail(obj):
    return mark_safe('<a href="{}">View</a>'.format(reverse('orders:admin-order-detail',args=[obj.id])))


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email','address', 'postal_code', 'city', 'paid','created', 'updated', order_detail]
    list_filter = ['paid', 'created', 'updated']
    inlines = [OrderItemInline]

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display=['id','order','product','price','quantity']
