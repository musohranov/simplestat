def grab_data():
    class CryptoCurrency:
        CurrencyList = {
            'Bitcoin': 'Bitcoin',
            'Ethereum': 'ETHUSD',
            'Monero': 'XMRUSD',
            'BitcoinCash': 'BCHUSD'
        }

        GetUsdUrl = 'https://gaterest.fxclub.org/real/restapi/quotes/historyquotes?symbol={}&interval=m1'

        @classmethod
        def get_usd(cls, currency):
            import urllib.request, json
            with urllib.request.urlopen(cls.GetUsdUrl.format(currency)) as url_:
                result = json.loads(url_.read().decode())
                return result['Result']['RateHistory'][-1]['c']

    return tuple([CryptoCurrency.get_usd(currency) for currency in CryptoCurrency.CurrencyList.values()])


