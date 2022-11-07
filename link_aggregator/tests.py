from django.test import TestCase, Client
from link_aggregator.models import Link

# Create your tests here.


class APITestCase(TestCase):
    client = Client()

    def test_add_url_to_db(self):
        response = self.client.post('/api/links', {"url": "betao.se"})
        self.assertEqual(response.status_code, 201)
        Link.objects.get(url="betao.se")

    def test_error_on_duplication(self):
        response = self.client.post('/api/links', {"url": "betao.se"})
        self.assertEqual(response.status_code, 201)
        response = self.client.post('/api/links', {"url": "betao.se"})
        self.assertEqual(response.status_code, 409)
