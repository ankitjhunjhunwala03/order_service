import os

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

import requests

from .models import Order
from .serializers import OrderSerializer

PRODUCT_SERVICE_URL = os.environ.get('PRODUCT_SERVICE_URL')


def get_product_details(product_id, request):
    response = requests.get(f'{PRODUCT_SERVICE_URL}/api/products/{product_id}/',
                            headers={'Authorization': request.headers.get('Authorization')})
    if response.status_code == 200:
        return response.json()
    return None


class CreateOrderView(APIView):

    def post(self, request, *args, **kwargs):
        order_data = {**request.data, 'user_id': request.authenticated_user['id']}
        for item in order_data.get('items'):
            product_details = get_product_details(item['product_id'], request)
            if not product_details:
                return Response({'error': f'Product {item["product_id"]} not found'},
                                status=status.HTTP_400_BAD_REQUEST)
            item['price'] = product_details['price']

        serializer = OrderSerializer(data=order_data)
        if serializer.is_valid():
            order = serializer.save()
            return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ListOrdersView(APIView):

    def get(self, request, *args, **kwargs):
        orders = Order.objects.filter(user_id=request.user.id)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)


class RetrieveOrderView(APIView):

    def get(self, request, order_id, *args, **kwargs):
        try:
            order = Order.objects.get(id=order_id, user_id=request.user.id)
        except Order.DoesNotExist:
            return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = OrderSerializer(order)
        return Response(serializer.data)
