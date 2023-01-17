from django.urls import path
from . import views
app_name = 'orders'
urlpatterns = [
    path('order/', views.OrderList.as_view()),
    path('orderitem/', views.OrderItemList.as_view()),


    path('create/', views.order_create, name='order_create'),
    path('admin/order/<int:order_id>', views.admin_order_detail, name='admin-order-detail'),
]