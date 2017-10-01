from views import app

from unittest import TestCase


def client():
    return app.test_client()


class TestViews(TestCase):
    def test_hello(self):
        res = client().get('/hi')
        got = res.data.decode()
        self.assertEqual(got, 'Hello World!')

    def test_game(self):
        res = client().get('/', query_string={'game': 'o   xoxox'})
        got = res.data.decode()
        self.assertEqual(got, 'o o xoxox')
