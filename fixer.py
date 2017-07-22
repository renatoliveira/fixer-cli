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

def parse_api_result(from_currency, to_currency, result):
    """Returns a Rate object from the data retrieved via API"""
    rate = result['rates'][to_currency.upper()]
    when = datetime.strptime(result['date'], '%Y-%m-%d').date()
    return {'from':from_currency, 'to':to_currency, 'date':when, 'rate':rate}

def parse_db_result(result):
    """Returns a Rate object from the data from the database"""
    return {'from':result[1], 'to':result[2], 'date':result[0], 'rate':result[3]}

def get_from_api(exchange_date, base):
    """Queries the API for rates on a specific date"""
    return requests.get('http://api.fixer.io/' +
                        exchange_date.strftime('%Y-%m-%d') + '?base=' + base).json()

def get_rates(from_currency, to_currency):
    """
    Get today, yesterday and last week's rates
    """
    latest_rates = None
    yesterday_rates = None
    last_week_rates = None
    rates = []
    if not DB.rate_exists(from_currency, to_currency, TODAY):
        latest_rates = get_from_api(TODAY, from_currency)
        rates.append(parse_api_result(from_currency, to_currency, latest_rates))
    else:
        latest_rates = parse_db_result(DB.get_rate(from_currency, to_currency, TODAY))
        rates.append(latest_rates)
    if not DB.rate_exists(from_currency, to_currency, YESTERDAY):
        yesterday_rates = get_from_api(YESTERDAY, from_currency)
        rate = parse_api_result(from_currency, to_currency, yesterday_rates)
        rates.append(rate)
        DB.set_rate(from_currency, to_currency, YESTERDAY, rate['rate'])
    else:
        yesterday_rates = parse_db_result(DB.get_rate(from_currency, to_currency, YESTERDAY))
        rates.append(yesterday_rates)
    if not DB.rate_exists(from_currency, to_currency, LAST_WEEK):
        last_week_rates = get_from_api(LAST_WEEK, from_currency)
        rate = parse_api_result(from_currency, to_currency, last_week_rates)
        rates.append(rate)
        DB.set_rate(from_currency, to_currency, LAST_WEEK, rate['rate'])
    else:
        last_week_rates = parse_db_result(DB.get_rate(from_currency, to_currency, LAST_WEEK))
        rates.append(last_week_rates)
    return rates

def print_conversion(rates):
    """Prints the text on screen"""
    if len(rates) == 3:
        most_recent_rate = rates[0]['rate']
        yesterday_rate = rates[1]['rate']
        last_week_rate = rates[2]['rate']
        print('1 ' + rates[0]['from'] + ' is worth approximately ' + rates[0]['to'] + ' ' +
              str(rates[0]['rate']) + '.')
        if len(sys.argv) == 4:
            value_to_convert = float(sys.argv[3])
            val = round(float(value_to_convert) * most_recent_rate, 2)
            print('Latest exchange for ' + rates[0]['from'] + ' ' + str(value_to_convert) + ' to ' +
                  rates[0]['to'] + ' is ' + str(val) + '.')

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
