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


class GetTestCase(TestCase):
    client = Client()

    def test_get_utls(self):
        Link.objects.create(url='a', created=datetime.date)
        Link.objects.create(url='b')
        Link.objects.create(url='c')
        response = self.client.get('/api/links')
        data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertDictContainsSubset({'id': 1, 'url': 'a', 'upvotes': 0, 'downvotes': 0, 'score': 0}, data[0])
        self.assertDictContainsSubset({'id': 2, 'url': 'b', 'upvotes': 0, 'downvotes': 0, 'score': 0}, data[1])
        self.assertDictContainsSubset({'id': 3, 'url': 'c', 'upvotes': 0, 'downvotes': 0, 'score': 0}, data[2])


# class VoteTestCase(TestCase):
#     client = Client()

#     def test_add_url_to_db(self):
#         response = self.client.post('/api/links', {"url": "https://www.yahoo.com/"})
#         self.assertEqual(response.status_code, 201)
#         Link.objects.get(url="https://www.yahoo.com/")

#     def test_error_on_duplication(self):
#         response = self.client.post('/api/links', {"url": "https://www.yahoo.com/"})
#         self.assertEqual(response.status_code, 201)
#         response = self.client.post('/api/links', {"url": "https://www.yahoo.com/"})
#         self.assertEqual(response.status_code, 409)
