from coinbase.wallet.client import Client
import credentials as cred

client = None
currency_code = None


def init():
    api_key, api_secret = cred.get_coinbase_credentials()

    global client
    global currency_code

    client = Client(api_key, api_secret, api_version='YYYY-MM-DD')
    currency_code = 'USD'  # can also use EUR, CAD, etc.


def get_price():
    # Make the request
    price = client.get_spot_price(currency=currency_code)
    return 'Current bitcoin price in %s: %s' % (currency_code, price.amount)
