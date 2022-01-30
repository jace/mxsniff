import unittest

from mxsniff import mxsniff


class MXSniffTestCase(unittest.TestCase):
    def test_mxsniff(self):
        result = mxsniff('google.com')
        self.assertFalse(result['public'])
        self.assertIn('google-apps', result['match'])
        self.assertGreater(len(result['mx']), 0)

        result = mxsniff('gmail.com')
        self.assertTrue(result['public'])
        self.assertIn('google-gmail', result['match'])
        self.assertEqual(len(result['mx']), 0)

        result = mxsniff('hasgeek.com')
        self.assertFalse(result['public'])
        self.assertIn('google-apps', result['match'])
        self.assertGreater(len(result['mx']), 0)

        result = mxsniff('yandex.ru')
        self.assertTrue(result['public'])
        self.assertIn('yandex', result['match'])
        self.assertEqual(len(result['mx']), 0)

        result = mxsniff('vayve.in')
        self.assertFalse(result['public'])
        self.assertIn('yandex-hosted', result['match'])
        self.assertGreater(len(result['mx']), 0)
