import unittest
from context import utils
from utils.address_utils import *



class LocationTestCase(unittest.TestCase):
    def test_city_lookup(self):
        self.assertTrue(is_in_region("London", "London"))
        self.assertTrue(is_in_region("London, United Kingdom", "london"))

    def test_postcode(self):
        self.assertTrue(is_in_region("SW72BB", "London"))
        self.assertTrue(is_in_region("sw72bb", "SW72BB"))

    def test_wrong_city(self):
        self.assertFalse(is_in_region("SW72BB", "Dublin"))
        self.assertFalse(is_in_region("London", "Dublin"))

if __name__ == '__main__':
    unittest.main()