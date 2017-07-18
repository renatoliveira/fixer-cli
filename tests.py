"""requets module and requets mocks"""
import unittest
import requests_mock
import fixer

# pylint: disable=invalid-name
class TestRequetsParsing(unittest.TestCase):
    """Test parsing from webservice"""
    def test_latest(self):
        """Test getting the latest currency"""
        with requests_mock.Mocker() as m:
            api_base_url = 'http://api.fixer.io/'
            m.register_uri('GET',
                           api_base_url + 'latest?base=USD',
                           text='{"status":200,"rates":{"EUR":0.8}}')
            rates = fixer.get_rates('USD')
            self.assertNotEqual(None, rates['rates'])
            self.assertNotEqual(None, rates['rates']['EUR'])
            self.assertEqual(0.8, rates['rates']['EUR'])

if __name__ == '__main__':
    unittest.main()
