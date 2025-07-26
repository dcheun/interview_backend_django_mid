from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from interview.order.models import Order, OrderTag, Inventory
from interview.inventory.models import InventoryType, InventoryLanguage


class OrderTagsListViewTests(APITestCase):
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

        self.tag1 = OrderTag.objects.create(name="Pending", is_active=True)
        self.tag2 = OrderTag.objects.create(name="Urgent", is_active=True)

        self.order = Order.objects.create(
            inventory=self.inventory,
            start_date="2023-01-01",
            embargo_date="2023-02-01"
        )
        self.order.tags.add(self.tag1, self.tag2)

    def test_get_tags_for_existing_order(self):
        """
        Test retrieving tags for an order that exists
        """
        url = reverse('order-tags-list', args=[self.order.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['name'], "Pending")
        self.assertEqual(response.data[1]['name'], "Urgent")

    def test_get_tags_for_order_with_no_tags(self):
        """
        Test retrieving tags for an order with no tags
        """
        new_order = Order.objects.create(
            inventory=self.inventory,
            start_date="2023-01-02",
            embargo_date="2023-02-02"
        )
        url = reverse('order-tags-list', args=[new_order.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)