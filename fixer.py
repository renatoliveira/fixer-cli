""""Fixer"""
from datetime import date, timedelta
import sys
from colorama import Fore
import requests

def get_rates(source_currency):
    """
    Get today, yesterday and last week's rates
    """
    yesterday = date.today() - timedelta(1)
    last_week = date.today() - timedelta(7)
    latest_rates = requests.get('http://api.fixer.io/latest?base=' + source_currency).json()
    yesterday_rates = requests.get('http://api.fixer.io/' + yesterday.strftime('%Y-%m-%d') +
                                   '?base=' + source_currency).json()
    last_week_rates = requests.get('http://api.fixer.io/' + last_week.strftime('%Y-%m-%d') +
                                   '?base=' + source_currency).json()
    return (latest_rates, yesterday_rates, last_week_rates)

def print_conversion(rates):
    """prints the conversion information"""
    if len(rates) == 3 and 'error' not in rates[0]:
        most_recent_rate = rates[0]['rates'][sys.argv[2].upper()]
        yesterday_rate = rates[1]['rates'][sys.argv[2].upper()]
        last_week_rate = rates[2]['rates'][sys.argv[2].upper()]
        print('1 ' + sys.argv[1].upper() + ' is worth approximately ' + sys.argv[2].upper() +
              ' ' + str(most_recent_rate) + ' today.')
        print('')
        if len(sys.argv) == 4:
            val = round(float(sys.argv[3]) * most_recent_rate, 2)
            print(sys.argv[3] + ' ' + sys.argv[1].upper() + ' is worth ' + str(val) + ' ' +
                  sys.argv[2].upper() + ' today.')
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
        rates = get_rates(sys.argv[1])
    if len(sys.argv) == 3 or len(sys.argv) == 4:
        print_conversion(rates)

if __name__ == '__main__':
    handle_options()
