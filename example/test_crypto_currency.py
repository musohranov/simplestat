def grab_data() -> dict:
    """
    Следим за курсами (в долларах США) крипто-валют
    """

    class CryptoCurrency:
        """
        Курс крипто-валюты с сайта fxclub.org
        """

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
        """
        Перечень кодов крипто-валют
        """

        GetUsdUrl = 'https://gaterest.fxclub.org/real/restapi/quotes/historyquotes?symbol={}&interval=m1'
        """
        Url для get запроса получения курса
        """

        @classmethod
        def get_usd(cls, currency: str) -> float:
            """
            Получить курс (в долларах США)
            :param currency: Код крипто-валюты
            """

            import urllib.request
            import json

            with urllib.request.urlopen(cls.GetUsdUrl.format(currency)) as url_:
                result = json.loads(url_.read().decode())
                return result['Result']['RateHistory'][-1]['c']

    return {curr: CryptoCurrency.get_usd(code) for curr, code in CryptoCurrency.CurrencyList.items()}
