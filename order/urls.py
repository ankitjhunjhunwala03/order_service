from django.urls import path
from .views import CreateOrderView, ListOrdersView, RetrieveOrderView

urlpatterns = [
    path('orders/', ListOrdersView.as_view(), name='order-list'),
    path('orders/create/', CreateOrderView.as_view(), name='order-create'),
    path('orders/<int:order_id>/', RetrieveOrderView.as_view(), name='order-detail'),
]