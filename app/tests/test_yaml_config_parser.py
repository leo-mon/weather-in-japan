import unittest
from src import yaml_config_parser


class TestScraper(unittest.TestCase):
    def test_get_area_ids(self):
        self.assertEqual(yaml_config_parser.get_area_ids(prefecture='東京', block='東京'), ('44', '47662'))
