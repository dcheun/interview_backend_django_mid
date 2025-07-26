from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response

from interview.order.models import Order, OrderTag
from interview.order.serializers import OrderSerializer, OrderTagSerializer

# Create your views here.
class OrderListCreateView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class OrderTagListCreateView(generics.ListCreateAPIView):
    queryset = OrderTag.objects.all()
    serializer_class = OrderTagSerializer


class OrdersByTagListView(APIView):
    """
    Retrieve all orders associated with a specific tag
    Example: GET /orders/tags/1/orders/
    """
    def get(self, request, tag_id):
        try:
            tag = OrderTag.objects.get(pk=tag_id)
            orders = tag.orders.all()  # Uses the related_name="orders" from the model
            serializer = OrderSerializer(orders, many=True)
            return Response(serializer.data)
        except OrderTag.DoesNotExist:
            return Response(
                {"error": f"Tag with ID {tag_id} not found"},
                status=status.HTTP_404_NOT_FOUND
            )
