name = "nomics-python"

import json
from decouple import config

NOMICS_KEY = config('NOMICS_KEY', default='2018-09-demo-dont-deploy-b69315e440beb145')

from nomics.api import (
    Candles,
    Currencies,
    ExchangeRates,
    Markets,
    Volume
)

class Nomics:
    def __init__(self, key=NOMICS_KEY):
        self.key = key

        self.Candles = Candles(self)
        self.Currencies = Currencies(self)
        self.ExchangeRates = ExchangeRates(self)
        self.Markets = Markets(self)
        self.Volume = Volume(self)

    def get_url(self, endpoint):
        return "https://api.nomics.com/v1/{}?key={}".format(endpoint, self.key)

