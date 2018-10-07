from coinbase.wallet.client import Client
import credentials as cred
import requests
import json
import csv
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import pandas as pd
plt.rcParams.update({'font.size': 22})
client = None
currency_code = None
key = cred.get_coinapi_credentials()
headers = {'X-CoinAPI-Key' : key}

def init():
    api_key, api_secret = cred.get_coinbase_credentials()


    global client
    global currency_code
    global img_filename
    global csv_filename
    csv_filename = "test.csv"
    img_filename="test.png"
    client = Client(api_key, api_secret, api_version='YYYY-MM-DD')
    currency_code = 'USD'  # can also use EUR, CAD, etc.


def get_price():
    # Make the request
    price = client.get_spot_price(currency=currency_code)
    return 'Current bitcoin price in %s: %s ' % (currency_code, price.amount)

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
    with open(csv_filename, 'w') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(currencies)


def plot_graph():
	GetHistoryBitcoinRates()
	hist = pd.read_csv(csv_filename,usecols=["time_period_end", "price_close"])
	hist.columns = ["time", "price"]
	hist['time'] = hist['time'].str[11:16]
	fig, ax = plt.subplots(1, figsize=(20,9))
	ax.plot(hist['time'],hist['price'], linewidth=2)
	ax.set(xlabel='Time', ylabel='BTC(USD)', title='Bitcoin Price Graph last hour')
	x = len(hist['time'])
	plt.xticks((hist['time'][0:x:x//6]))
	plt.grid()
	fig.savefig(img_filename)
	return img_filename
