import requests
import time
import pandas as pd

from .api import API

class Markets(API):
    def get_exchange_markets(self, exchange = None, base = None, quote = None):
        '''
        https://nomics.com/docs#tag/Markets

        Returns information on the exchanges and markets that Nomics supports

        :param  str     exchange:   Nomics Exchange ID to filter by
                                    Optional   

        :param  [str]   base:       Comma separated list of base currencies to filter by
                                    Optional

        :param  [str]   quote:      Comma separated list of quote currencies to filter by 
                                    Optional   
        '''

        url = self.client.get_url('markets')
        params = {
            'exchange': exchange,
            'base': base,
            'quote': quote
        }

        resp = requests.get(url, params = params)

        if resp.status_code == 200:
            return resp.json()
        else:
            return resp.text


    def get_exchange_markets_df(self, exchange, base='BTC',quote='USD'):
        '''
        Returns a Pandas dataframe of information on the exchanges and markets that Nomics supports
        '''
        exch = self.get_exchange_markets(exchange, base, quote)
        exchange = pd.DataFrame(exch)
        return exchange


    def search_exchanges(self, exchange, base='BTC',quote='USD'):
        '''
        Search Nomics listed exchanges for a given exchange name, through the active Markets endpoint (free) rather than the Exchanges one.
        '''
        markets = self.get_exchange_markets_df(exchange,base,quote)
        if not markets.empty:
            # markets.head()
            if len(markets) > 1:
                match = markets.sort_values('exchange', ascending=True)
            # match[1200:]
            match = match['exchange'].unique()
            return match
        else:
            return None

    
    def yield_exchanges(self, exchanges):
        """
        Helper function for get_nomics_mkts_by_exchanges_for_coin()
        """
        d = {}
        for exchange in exchanges:
            d["{}".format(exchange)] = pd.DataFrame(self.get_exchange_markets_df(exchange))
            exch = d["{}".format(exchange)]
            yield exch
            #print (exch.head())
            time.sleep(1)
            continue
        return;


    def get_mkts_by_exchanges_for_coin(self, exchanges):
        '''
        Returns a Pandas dataframe of every existing market for a currency pair, for a specified list of exchanges.

        :param  [str] exchanges:  List of exhange names to search for a currency pair.
                                        e.g. ['binance','bitstamp','gdax','itbit','kraken','gemini']
        '''
        genr_exchs = self.yield_exchanges(exchanges)
        exchs_coin_mkts_df = pd.concat([x for x in genr_exchs])
        return exchs_coin_mkts_df


    def get_market_cap_history(self, start, end = None):
        '''
        Returns the total market cap for all cryptoassets at intervals between the requested time period.

        :param  str start:  Start time of the interval in RFC3339 format

        :param  str end:    End time of the interval in RFC3339 format. If not provided, the current time is used.  
        '''

        url = self.client.get_url('market-cap/history')
        params = {
            'start': start,
            'end': end
        }
        
        resp = requests.get(url, params = params)

        if resp.status_code == 200:
            return resp.json()
        else:
            return resp.text

    def get_exchange_markets_ticker(self, interval = None, currency = None, base = None, quote = None, exchange = None, market = None, convert = None):
        '''
        Returns high level information about individual markets on exchanges integrated with Nomics.

        :param  [str]   interval:   Comma separated time interval of the ticker(s). 
                                    Default is 1d,7d,30d,365d,ytd

        :param  [str]   currency:   A comma separated list of Nomics Currency IDs.

        :param  [str]   base:       A comma separated list of Nomics Currency IDs.

        :param  [str]   quote:      A comma separated list of Nomics Currency IDs. 

        :param  [str]   exchange:   A comma separated list of Nomics Exchange IDs.

        :param  [str]   market:     A comma separated list of Nomics Market IDs.

        :param  str     convert:    Nomics Currency ID to convert all financial data to     
        '''

        url = self.client.get_url('exchange-markets/ticker')
        params = {
            'interval': interval,
            'currency': currency,
            'base': base,
            'quote': quote,
            'exchange': exchange,
            'market': market,
            'convert': convert
        }
        
        resp = requests.get(url, params = params)

        if resp.status_code == 200:
            return resp.json()
        else:
            return resp.text


# async def create_queries_from_response(response):
#     """Make an API call, then use those results as a list to pass to another call:"""
#     all_ids = []
    
#     for d in response:
#         for key, value in d['to'].items():
#             if key == 'id':
#                 all_ids.append(value)   
                
#     # for id in all_ids:
#     #     response2 = await make_api_call(id)
#         # return response2;
#     response2 = await asyncio.gather(*[make_api_call(id) for id in all_ids])
#     return response2;