import requests
import json
import credentials
import csv
from datetime import datetime, timedelta

key = credentials.get_coinapi_credentials()
headers = {'X-CoinAPI-Key' : key}

def GetCurrentExchangeRates():
	url = 'https://rest.coinapi.io/v1/assets'
	response = requests.get(url, headers=headers)
	currencies = json.loads(response.text)

	for currency in currencies:
		if (currency['type_is_crypto'] =='1'):
			exchangerateURL = 'https://rest.coinapi.io/v1/exchangerate/' + currency['asset_id'] + "/USD"
			exchangeres =  requests.get(exchangerateURL, headers=headers)
			currencyrates = json.loads(exchangeres.text)
			print("Cryptocurrency: %s rate in USD: %s" % (currency['name'], currencyrates['rate']))

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

def _main():
    # GetCurrentExchangeRates()
    GetHistoryBitcoinRates()

if __name__ == '__main__' :
  _main()
