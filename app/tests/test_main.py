import unittest
from src import main

class TestMain(unittest.TestCase):
    def test_main(self):
        result = main.main('10min', '東京', '東京', 'csv', '20181214', '20181215')
        self.assertTrue(result)
        result = main.main('hourly', '東京', '東京', 'csv', '20181214', '20181215')
        self.assertTrue(result)


if __name__ == "__main__":
    unittest.main()