from django.test import TestCase, Client
from link_aggregator.models import Link
from datetime import datetime, timedelta, timezone
# Create your tests here.


class POSTTestCase(TestCase):
    client = Client()

    def test_add_url_to_db(self):
        response = self.client.post('/api/links', {"url": "https://www.yahoo.com/"})
        self.assertEqual(response.status_code, 201)
        url = Link.objects.get(url="https://www.yahoo.com/")
        self.assertTrue(url.created - datetime.now(timezone.utc) < timedelta(minutes=1))

    def test_error_on_duplication(self):
        response = self.client.post('/api/links', {"url": "https://www.yahoo.com/"})
        self.assertEqual(response.status_code, 201)
        response = self.client.post('/api/links', {"url": "https://www.yahoo.com/"})
        self.assertEqual(response.status_code, 409)
