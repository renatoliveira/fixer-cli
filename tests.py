"""requets module and requets mocks"""
import unittest
from datetime import date, timedelta
import requests_mock
import fixer

# pylint: disable=invalid-name
class TestRequetsParsing(unittest.TestCase):
    """Test parsing from webservice"""
    def test_latest(self):
        """Test getting the latest currency"""
        with requests_mock.Mocker() as m:
            yesterday = date.today() - timedelta(1)
            last_week = date.today() - timedelta(7)
            api_base_url = 'http://api.fixer.io/'
            m.register_uri('GET',
                           api_base_url + 'latest?base=USD',
                           text='{"status":200,"rates":{"EUR":0.8}}')
            m.register_uri('GET',
                           api_base_url + yesterday.strftime('%Y-%m-%d'),
                           text='{"status":200,"rates":{"EUR":0.8}}')
            m.register_uri('GET',
                           api_base_url + last_week.strftime('%Y-%m-%d'),
                           text='{"status":200,"rates":{"EUR":0.8}}')
            rates = fixer.get_rates('USD')
            self.assertNotEqual(None, rates[0]['rates'])
            self.assertNotEqual(None, rates[0]['rates']['EUR'])
            self.assertEqual(0.8, rates[0]['rates']['EUR'])

if __name__ == '__main__':
    unittest.main()
