
from .models import Order, OrderItem
from rest_framework.serializers import ModelSerializer

class OrderSerializer(ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'


class OrderItemSerializer(ModelSerializer):
    class Meta:
        model = OrderItem
        fields=['product', 'price']