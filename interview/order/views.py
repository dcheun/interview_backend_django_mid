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


class OrderTagsListView(APIView):
    """
    Retrieve all tags associated with a specific order
    """
    def get(self, request, order_id):
        try:
            order = Order.objects.get(pk=order_id)
            tags = order.tags.all()
            serializer = OrderTagSerializer(tags, many=True)
            return Response(serializer.data)
        except Order.DoesNotExist:
            return Response(
                {"error": f"Order with ID {order_id} not found"},
                status=status.HTTP_404_NOT_FOUND
            )