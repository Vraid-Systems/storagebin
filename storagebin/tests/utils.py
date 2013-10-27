from django.test import TestCase

from storagebin.internal.util import is_image

class UtilTestSuite(TestCase):
    def test_is_image(self):
        self.assertFalse(is_image("application/xml"))
        self.assertFalse(is_image("audio/mp4"))
        self.assertFalse(is_image("audio/mpeg"))
        self.assertTrue(is_image("image/x-xcf"))
        self.assertTrue(is_image("image/jpeg"))
        self.assertTrue(is_image("image/png"))
        self.assertTrue(is_image("image/svg+xml"))
