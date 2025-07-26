from datetime import datetime, timedelta
from decimal import Decimal

from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from interview.inventory.models import Inventory
from interview.inventory.schemas import InventoryMetaData


class InventoryListCreateViewTests(APITestCase):
    def setUp(self):
        # Create test data with different creation dates
        now = datetime.now()
        self.item1 = Inventory.objects.create(
            name="The Shawshank Redemption",
            metadata=InventoryMetaData(
                year=1994,
                actors=["Tim Robbins", "Morgan Freeman"],
                imdb_rating=Decimal("9.3"),
                rotten_tomatoes_rating=98
            ).dict(),
            created_at=now - timedelta(days=10)
        )
        self.item2 = Inventory.objects.create(
            name="The Godfather",
            metadata=InventoryMetaData(
                year=1972,
                actors=["Marlon Brando", "Al Pacino"],
                imdb_rating=Decimal("9.2"),
                rotten_tomatoes_rating=97
            ).dict(),
            created_at=now - timedelta(days=5)
        )
        self.item3 = Inventory.objects.create(
            name="The Dark Knight",
            metadata=InventoryMetaData(
                year=2008,
                actors=["Christian Bale", "Heath Ledger"],
                imdb_rating=Decimal("9.0"),
                rotten_tomatoes_rating=94
            ).dict(),
            created_at=now
        )

        self.list_url = reverse('inventory')

    def test_filter_by_after_date_returns_correct_items(self):
        test_date = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
        response = self.client.get(f"{self.list_url}?after_date={test_date}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        # Verify the filtered items
        returned_names = {item['name'] for item in response.data}
        self.assertIn("The Godfather", returned_names)
        self.assertIn("The Dark Knight", returned_names)

    def test_filter_with_empty_results(self):
        future_date = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
        response = self.client.get(f"{self.list_url}?after_date={future_date}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)
