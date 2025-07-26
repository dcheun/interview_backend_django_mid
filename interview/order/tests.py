from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from interview.order.models import Order, OrderTag, Inventory
from interview.inventory.models import InventoryType, InventoryLanguage


class OrdersByTagListViewTests(APITestCase):
    def setUp(self):
        # Create test data
        self.inventory_type = InventoryType.objects.create(name="Movie")
        self.language = InventoryLanguage.objects.create(name="English")

        self.inventory = Inventory.objects.create(
            name="Test Movie",
            type=self.inventory_type,
            language=self.language,
            metadata={}
        )

        self.tag1 = OrderTag.objects.create(name="Pending")
        self.tag2 = OrderTag.objects.create(name="Urgent")

        self.order1 = Order.objects.create(
            inventory=self.inventory,
            start_date="2023-01-01",
            embargo_date="2023-02-01"
        )
        self.order1.tags.add(self.tag1)

        self.order2 = Order.objects.create(
            inventory=self.inventory,
            start_date="2023-01-15",
            embargo_date="2023-02-15"
        )
        self.order2.tags.add(self.tag1, self.tag2)

    def test_get_orders_by_tag(self):
        url = reverse('orders-by-tag', args=[self.tag1.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['id'], self.order1.id)
        self.assertEqual(response.data[1]['id'], self.order2.id)