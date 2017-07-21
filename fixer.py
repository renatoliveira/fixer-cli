""""Fixer"""
from datetime import date, datetime, timedelta
import sys
import os
from colorama import Fore
import requests
from history import LocalHistory

DB_PATH = ''
if os.name == 'nt':
    DB_PATH = os.getenv('APPDATA') + '\\fixer\\history.db'
DB = LocalHistory(DB_PATH)
TODAY = date.today()
YESTERDAY = date.today() - timedelta(1)
LAST_WEEK = date.today() - timedelta(7)

class Rate:
    def __init__(self, fromx, tox, when, rate):
        self.fromx = fromx.upper()
        self.tox = tox.upper()
        self.retrieved_at = when
        self.rate = rate

def save_to_history(fromx, tox, latest_rate, latest_rate_date, yesterday_rate, last_week_rate):
    """Saves to the history the rates that were retrieved from the API."""
    DB.set_rate(fromx, tox, latest_rate_date, latest_rate)
    DB.set_rate(fromx, tox, YESTERDAY, yesterday_rate)
    DB.set_rate(fromx, tox, LAST_WEEK, last_week_rate)
    DB.close()

def parse_api_result(from_currency, to_currency, result):
    rate = result['rates'][to_currency.upper()]
    when = datetime.strptime(result['date'], '%Y-%m-%d').date()
    return Rate(from_currency, to_currency, when, rate)

def parse_db_result(result):
    return Rate(result[1], result[2], result[0], result[3])

def get_rates(from_currency, to_currency):
    """
    Get today, yesterday and last week's rates
    """
    latest_rates = None
    yesterday_rates = None
    last_week_rates = None
    rates = []
    if not DB.rate_exists(from_currency, to_currency, TODAY):
        latest_rates = requests.get('http://api.fixer.io/' + TODAY.strftime('%Y-%m-%d') +
                                    '?base=' + from_currency).json()
        rates.append(parse_api_result(from_currency, to_currency, latest_rates))
    else:
        latest_rates = parse_db_result(DB.get_rate(from_currency, to_currency, TODAY))
        rates.append(latest_rates)
    if not DB.rate_exists(from_currency, to_currency, YESTERDAY):
        yesterday_rates = requests.get('http://api.fixer.io/' + YESTERDAY.strftime('%Y-%m-%d') +
                                       '?base=' + from_currency).json()
        rate = parse_api_result(from_currency, to_currency, yesterday_rates)
        rates.append(rate)
        DB.set_rate(from_currency, to_currency, YESTERDAY, rate.rate)
    else:
        yesterday_rates = parse_db_result(DB.get_rate(from_currency, to_currency, YESTERDAY))
        rates.append(yesterday_rates)
    if not DB.rate_exists(from_currency, to_currency, LAST_WEEK):
        last_week_rates = requests.get('http://api.fixer.io/' + LAST_WEEK.strftime('%Y-%m-%d') +
                                       '?base=' + from_currency).json()
        rate = parse_api_result(from_currency, to_currency, last_week_rates)
        rates.append(rate)
        DB.set_rate(from_currency, to_currency, LAST_WEEK, rate.rate)
    else:
        last_week_rates = parse_db_result(DB.get_rate(from_currency, to_currency, LAST_WEEK))
        rates.append(last_week_rates)
    return rates

def print_conversion(rates):
    """Prints the text on screen"""
    if len(rates) == 3:
        most_recent_rate = rates[0].rate
        yesterday_rate = rates[1].rate
        last_week_rate = rates[2].rate
        print('1 ' + rates[0].fromx + ' is worth approximately ' + rates[0].tox + ' ' +
              str(rates[0].rate) + '.')
        if len(sys.argv) == 4:
            value_to_convert = float(sys.argv[3])
            val = round(float(value_to_convert) * most_recent_rate, 2)
            print('Latest exchange for ' + rates[0].fromx + ' ' + str(value_to_convert) + ' to ' +
                  rates[0].tox + ' is ' + str(val) + '.')

        print('')
        day_diff = round((1 - (most_recent_rate / yesterday_rate)) * 100, 3)
        week_diff = round((1 - (most_recent_rate / last_week_rate)) * 100, 3)
        if most_recent_rate > yesterday_rate:
            print(Fore.GREEN + '▲ ' + Fore.RESET + str(abs(day_diff)) + '% since yesterday')
        else:
            print(Fore.RED + '▼ ' + Fore.RESET + str(abs(day_diff)) + '% since yesterday')
        if most_recent_rate > last_week_rate:
            print(Fore.GREEN + '▲ ' + Fore.RESET + str(abs(week_diff)) + '% since last week')
        else:
            print(Fore.RED + '▼ ' + Fore.RESET + str(abs(week_diff)) + '% since last week')
        print(Fore.RESET)

def handle_options():
    """Handle arguments passed"""
    if len(sys.argv) >= 2:
        rates = get_rates(sys.argv[1], sys.argv[2])
        print_conversion(rates)

if __name__ == '__main__':
    handle_options()
