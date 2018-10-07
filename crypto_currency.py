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
    global csv_pred_filename

    csv_filename = "test.csv"
    img_filename="test.png"
    csv_pred_filename="pred.csv"

    client = Client(api_key, api_secret, api_version='YYYY-MM-DD')
    currency_code = 'USD'  # can also use EUR, CAD, etc.


def get_price():
    # Make the request
    price = client.get_spot_price(currency=currency_code)
    return 'Current bitcoin price in %s: %s ' % (currency_code, price.amount)

def GetHistoryBitcoinRates(filename,delay=True,currentdate=datetime.now()):
    if delay:
        starttime = currentdate - timedelta(minutes=60)
        endtime = currentdate + timedelta(minutes=3)
    else:
        starttime = currentdate
        endtime = currentdate + timedelta(minutes=15)
        
    endtimeval = str(endtime.date()) + "T" + str(endtime.time())
    subendtime = endtimeval[:19]
    startvalue = str(starttime.date()) + "T" + str(starttime.time())
    substr = startvalue[:19]
    url = 'https://rest.coinapi.io/v1/ohlcv/BITSTAMP_SPOT_BTC_USD/history?period_id=1MIN&time_start=' + substr + '&time_end=' +subendtime
    response = requests.get(url, headers=headers,timeout=5)
    currencies = json.loads(response.text)
    keys = currencies[0].keys()
    with open(filename, 'w') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(currencies)

def stad(arg,arg1):
	for i in [arg,arg1]:
		i.columns = ["time", "price"]
		i['time'] = i['time'].str[11:16]
	return arg, arg1

def plot_graph():
	currentdate = datetime.now()
	GetHistoryBitcoinRates(csv_filename,True,currentdate)
	GetHistoryBitcoinRates(csv_pred_filename,False,currentdate)
	hist = pd.read_csv(csv_filename,usecols=["time_period_end", "price_close"])
	pred = pd.read_csv(csv_pred_filename,usecols=["time_period_end", "price_close"])
	hist, pred = stad(hist, pred)
	fig, ax = plt.subplots(1, figsize=(20,9))
	ax.plot(hist['time'],hist['price'],label="Actual Price",color="blue", linewidth=2)
	ax.plot(pred['time'],pred['price'],label="Predicted Price", color="orange", linewidth=2)
	ax.set(xlabel='Time', ylabel='BTC(USD)', title='Bitcoin Price Graph last hour')
	time = list(hist['time'])+list(pred['time'])
	x = len(time)
	plt.xticks((time[0:x:x//6]))
	ax.legend(loc='best', fontsize=18);
	plt.grid()
	fig.savefig(img_filename)
	return img_filename
