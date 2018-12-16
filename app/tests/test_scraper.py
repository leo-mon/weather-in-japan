import unittest
import pandas
from src import scraper


class TestScraper(unittest.TestCase):
    def test_construct_url(self):
        url1 = scraper.construct_url('10min', 44, 47662, 2018, 12, 15)
        self.assertEqual(url1,
                         'https://www.data.jma.go.jp/obd/stats/etrn/view/10min_s1.php?prec_no=44&block_no=47662&year'
                         '=2018&month=12&day=15&view=p1')

    def test_fetch_weather_by_10(self):
        df = scraper.fetch_weather_by_10(44, 47662, 2018, 12, 15)
        self.assertIsInstance(df, pandas.core.frame.DataFrame)
        self.assertEqual(df.timestamp[0], pandas.to_datetime('2018-12-15 00:10:00').tz_localize('Asia/Tokyo'))
        self.assertEqual(df.timestamp[-1], pandas.to_datetime('2018-12-16 00:00:00').tz_localize('Asia/Tokyo'))

        df = scraper.fetch_weather_by_10(44, 47662, 2018, 6, 30)

    def test_fetch_hourly_weather(self):
        df = scraper.fetch_hourly_weather(44, 47662, 2018, 12, 15)
        self.assertIsInstance(df, pandas.core.frame.DataFrame)
        self.assertEqual(df.timestamp[0], pandas.to_datetime('2018-12-15 01:00:00').tz_localize('Asia/Tokyo'))
        self.assertEqual(df.timestamp[-1], pandas.to_datetime('2018-12-16 00:00:00').tz_localize('Asia/Tokyo'))

        df = scraper.fetch_hourly_weather(44, 47662, 2018, 6, 30)

if __name__ == "__main__":
    unittest.main()
