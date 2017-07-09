import sys
import requests

def get_rates(source_currency):
    result = requests.get('http://api.fixer.io/latest?base=' + source_currency).json()
    return result

def print_all(r):
    if 'error' not in r:
        print(' - - - - - - - - - - - - - - - - - - - -')
        for k in r['rates']:
            print(k + ': ' + str(r['rates'][k]))
        print(' - - - - - - - - - - - - - - - - - - - -')
    else:
        print(r['error'])

def print_conversion(r):
    if 'error' not in r:
        print(' - - - - - - - - - - - - - - - - - - - -')
        print(sys.argv[1].upper() + ' is worth approximately ' + sys.argv[2].upper() + ' ' + str(r['rates'][sys.argv[2].upper()]))
        print(' - - - - - - - - - - - - - - - - - - - -')
    else:
        print(r['error'])

def print_conversion_with_value(r):
    if 'error' not in r:
        v = float(sys.argv[3])
        print(' - - - - - - - - - - - - - - - - - - - -')
        print(sys.argv[1].upper() + ' ' + str(v) + ' is worth approximately ' + sys.argv[2].upper() + ' ' + str(r['rates'][sys.argv[2].upper()] * v))
        print(' - - - - - - - - - - - - - - - - - - - -')
    else:
        print(r['error'])

def handle_options():
    if len(sys.argv) >= 2:
        r = get_rates(sys.argv[1])
    
    if len(sys.argv) == 2:
        print_all(r)
    if len(sys.argv) == 3:
        print_conversion(r)
    if len(sys.argv) == 4:
        print_conversion_with_value(r)

if __name__ == '__main__':
    handle_options()