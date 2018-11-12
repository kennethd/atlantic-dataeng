
from unittest import TestCase

from flaskapp.app import configured_app


class TestFlaskApp(TestCase):

    def setUp(self):
        # init app for each test
        self.app = configured_app(config_module='flaskapp.test_settings')
        self.client = self.app.test_client()

    def test_get_index(self):
        response = self.client.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_post_with_no_file(self):
        pass

    def test_post_with_empty_filename(self):
        pass

    def test_post_with_invalid_extension(self):
        pass

    def test_post_with_misconfigured_upload_dir(self):
        pass

