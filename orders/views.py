from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render,get_object_or_404
from .models import OrderItem,Order
from .forms import OrderCreateForm
from cart.cart import Cart

import django_filters.rest_framework
from rest_framework import filters
from rest_framework import generics
from .serializers import  OrderSerializer, OrderItemSerializer


from .tasks import order_created

@staff_member_required
def admin_order_detail(request, order_id):
    order=get_object_or_404(Order, id=order_id)
    context={
        'order':order
    }
    return render(request, 'admin/orders/order/detail.html', context)

def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity']
                )
            cart.clear()
            order_created.delay(order.id)
            return render(request, 'orders/order/created.html', {'order': order})
    else:
        form = OrderCreateForm()
        return render(request, 'orders/order/create.html', {'cart': cart, 'form': form})

class OrderList(generics.ListAPIView):
    queryset=Order.objects.all()
    serializer_class= OrderSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['email']
    search_fields=['address', 'first_name', 'postal_code']
    ordering_field=['city']

class OrderItemList(generics.ListAPIView):
    queryset=OrderItem.objects.all()
    serializer_class=OrderItemSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['product', 'price']
    search_fields=['price']
    ordering_fields=['product']
