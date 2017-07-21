"""requets module and requets mocks"""
import unittest
from datetime import date, timedelta
import requests_mock
import fixer
from history import LocalHistory

# pylint: disable=invalid-name
class TestRequetsParsing(unittest.TestCase):
    """Test parsing from webservice"""
    def test_latest(self):
        """Test getting the latest currency"""
        with requests_mock.Mocker() as m:
            today = date.today()
            yesterday = date.today() - timedelta(1)
            last_week = date.today() - timedelta(7)
            api_base_url = 'http://api.fixer.io/'
            m.register_uri('GET',
                           api_base_url + today.strftime('%Y-%m-%d') + '?base=USD',
                           text='{"status":200,"rates":{"EUR":0.8},"date":"' +
                           str(today) + '"}')
            m.register_uri('GET',
                           api_base_url + yesterday.strftime('%Y-%m-%d') + '?base=USD',
                           text='{"status":200,"rates":{"EUR":0.8},"date":"' +
                           str(yesterday) + '"}')
            m.register_uri('GET',
                           api_base_url + last_week.strftime('%Y-%m-%d') + '?base=USD',
                           text='{"status":200,"rates":{"EUR":0.8},"date":"' +
                           str(last_week) + '"}')
            rates = fixer.get_rates('USD', 'EUR')
            self.assertNotEqual(None, rates[0].rate)
            self.assertNotEqual(None, rates[0].rate)
            self.assertEqual(0.8, rates[0].rate)

    def test_database(self):
        """Testing the database operations"""
        db_path = ':memory:'
        today = date.today()
        yesterday = date.today() - timedelta(1)
        last_week = date.today() - timedelta(7)
        history = LocalHistory(db_path)
        history.create_tables(db_path)
        history.set_rate('USD', 'EUR', date.today(), 0.8)
        history.set_rate('USD', 'EUR', yesterday, 0.5)
        history.set_rate('USD', 'EUR', last_week, 0.2)
        today_record = history.get_rate('USD', 'EUR', today)
        yesterday_record = history.get_rate('USD', 'EUR', yesterday)
        last_week_record = history.get_rate('USD', 'EUR', last_week)
        self.assertEqual(0.8, today_record[3])
        self.assertEqual(0.5, yesterday_record[3])
        self.assertEqual(0.2, last_week_record[3])
        all_records = history.get_rates('USD', 'EUR')
        self.assertEqual(3, len(all_records))

if __name__ == '__main__':
    unittest.main()
