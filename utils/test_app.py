import unittest
import app


class MyTestCase(unittest.TestCase):
    def test_valid_search_track(self):
        limit = 10

        result = app._search_by_song("Hello there", limit=limit)
        assert "error" not in result
        self.assertEqual(len(result["tracks"]["items"]), limit)

    def test_valid_search_album(self):
        limit = 10

        result = app._search_by_album("Wonders", limit=limit)
        assert "error" not in result
        self.assertEqual(len(result["albums"]["items"]), limit)

    def test_valid_search_artist(self):
        limit = 10

        result = app._search_by_artist("John", limit=limit)
        assert "error" not in result
        self.assertEqual(len(result["artists"]["items"]), limit)

    def test_regenerate_credentials(self):
        app.credential.access_token = "notvalidhahaha"
        limit = 10

        result = app._search_by_song("Hello there", limit=limit)
        assert "error" not in result
        self.assertEqual(len(result["tracks"]["items"]), limit)


if __name__ == '__main__':
    unittest.main()
