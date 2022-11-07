from django.test import TestCase, Client
from link_aggregator.models import Link
from datetime import datetime, timedelta, timezone


class PostTestCase(TestCase):
    client = Client()

    def test_add_url_to_db(self):
        response = self.client.post('/api/links/', {"url": "https://www.yahoo.com/"})
        self.assertEqual(response.status_code, 201)
        url = Link.objects.get(url="https://www.yahoo.com/")
        self.assertTrue(url.created - datetime.now(timezone.utc) < timedelta(minutes=1))

    def test_error_on_duplication(self):
        response = self.client.post('/api/links/', {"url": "https://www.yahoo.com/"})
        self.assertEqual(response.status_code, 201)
        response = self.client.post('/api/links/', {"url": "https://www.yahoo.com/"})
        self.assertEqual(response.status_code, 409)


class GetTestCase(TestCase):
    client = Client()

    def test_get_utls(self):
        Link.objects.create(url='a')
        Link.objects.create(url='b')
        Link.objects.create(url='c')
        response = self.client.get('/api/links/')
        data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertDictContainsSubset({'id': 1, 'url': 'a', 'upvotes': 0, 'downvotes': 0, 'score': 0}, data[0])
        self.assertDictContainsSubset({'id': 2, 'url': 'b', 'upvotes': 0, 'downvotes': 0, 'score': 0}, data[1])
        self.assertDictContainsSubset({'id': 3, 'url': 'c', 'upvotes': 0, 'downvotes': 0, 'score': 0}, data[2])


class VoteTestCase(TestCase):
    client = Client()

    def setup_model(self):
        Link.objects.create(url='a')
        Link.objects.create(url='b')
        Link.objects.create(url='c')

    def test_increase(self):
        self.setup_model()
        response = self.client.get('/api/links/1/upvote')
        self.assertEqual(response.status_code, 200)
        data = Link.objects.get(id=1)
        self.assertEqual(data.upvotes, 1)

    def test_decrease(self):
        self.setup_model()
        response = self.client.post('/api/links/2/downvote')
        self.assertEqual(response.status_code, 200)
        data = Link.objects.get(id=2)
        self.assertEqual(data.downvotes, 1)

    def test_score(self):
        self.setup_model()
        response = self.client.post('/api/links/3/upvote')
        response = self.client.post('/api/links/3/upvote')
        response = self.client.post('/api/links/3/upvote')
        response = self.client.post('/api/links/3/upvote')
        response = self.client.post('/api/links/3/downvote')
        response = self.client.post('/api/links/3/downvote')
        response = self.client.post('/api/links/3/downvote')
        self.assertEqual(response.status_code, 200)
        data = Link.objects.get(id=3)
        self.assertEqual(data.score, 1)
