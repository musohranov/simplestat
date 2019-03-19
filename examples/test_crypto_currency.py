def grab_data():
    class CryptoCurrency:
        CurrencyList = {
            'Bitcoin': 'Bitcoin',
            'Ethereum': 'ETHUSD',
            'Monero': 'XMRUSD',
            'BitcoinCash': 'BCHUSD',
            'BitcoinGold': 'BTGUSD',
            'CARDANO': 'ADAUSD',
            'DASH': 'DSHUSD',
            'EOS': 'EOSUSD',
            'IOTA': 'IOTUSD',
            'NEM': 'XEMUSD',
            'NEO': 'NEOUSD',
            'OmiseGo': 'OMGUSD',
            'Ripple': 'XRPUSD'
        }

        GetUsdUrl = 'https://gaterest.fxclub.org/real/restapi/quotes/historyquotes?symbol={}&interval=m1'

        @classmethod
        def get_usd(cls, currency):
            import urllib.request
            import json

            with urllib.request.urlopen(cls.GetUsdUrl.format(currency)) as url_:
                result = json.loads(url_.read().decode())
                return result['Result']['RateHistory'][-1]['c']

    return {curr: CryptoCurrency.get_usd(code) for curr, code in CryptoCurrency.CurrencyList.items()}


