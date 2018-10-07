from coinbase.wallet.client import Client
import credentials as cred
import requests
import json
import csv
from datetime import datetime, timedelta

client = None
currency_code = None
key = None
headers = None

def init():
    api_key, api_secret = cred.get_coinbase_credentials()
    key = cred.get_coinapi_credentials()
    headers = {'X-CoinAPI-Key' : key}


    global client
    global currency_code

    client = Client(api_key, api_secret, api_version='YYYY-MM-DD')
    currency_code = 'USD'  # can also use EUR, CAD, etc.


def get_price():
    # Make the request
    price = client.get_spot_price(currency=currency_code)
    return 'Current bitcoin price in %s: %s' % (currency_code, price.amount)

def GetHistoryBitcoinRates():
    currentdate = datetime.now()
    starttime = currentdate - timedelta(minutes=60)
    endtime = str(currentdate.date()) + "T" + str(currentdate.time())
    subendtime = endtime[:19]
    value = str(starttime.date()) + "T" + str(starttime.time())
    substr = value[:19]
    url = 'https://rest.coinapi.io/v1/ohlcv/BITSTAMP_SPOT_BTC_USD/history?period_id=1MIN&time_start=' + substr + '&time_end=' +subendtime
    response = requests.get(url, headers=headers)
    currencies = json.loads(response.text)
    keys = currencies[0].keys()
    with open('test.csv', 'w') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(currencies)
