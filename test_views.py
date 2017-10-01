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
        res = client().get('/', query_string={'board': 'o   xoxox'})
        got = res.data.decode()
        self.assertEqual(got, 'o o xoxox')

    def test_game_spec(self):
        res = client().get('/', query_string={'board': ' xxo  o  '})
        got = res.data.decode()
        self.assertEqual(got, 'oxxo  o  ')

    def test_invalid_boards_400(self):
        query_strings = [
            {},
            {'board': ''},
            {'board': 'ooooo'},
            {'board': 'xxxxxxxxx'},
            {'board': 'xxxxooooo'},
        ]
        for qs in query_strings:
            res = client().get('/', query_string=qs)
            self.assertEqual(res.status_code, 400)
