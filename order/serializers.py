from decimal import Decimal as D
from rest_framework import serializers
from .models import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['product_id', 'quantity', 'price']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'user_id', 'created_at', 'updated_at', 'status', 'order_total', 'items']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        order = Order.objects.create(**validated_data)
        order_total = D(0.0)
        for item_data in items_data:
            item = OrderItem.objects.create(order=order, **item_data)
            order_total += D(item.price) * D(item.quantity)
        order.order_total = order_total
        order.save()
        return order
