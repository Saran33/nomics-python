import requests

from .api import API

class Volume(API):
    def get_volume_history(self, start = None, end = None):
        '''
        https://nomics.com/docs#tag/Volume
        
        Returns the total volume for all cryptoassets in USD at intervals between the requested time period.

        :param  str start:  Start time of the interval in RFC3339 format

        :param  str end:    End time of the interval in RFC3339 format. If not provided, the current time is used.  
        '''

        url = self.client.get_url('volume/history')
        params = {
            'start': start,
            'end': end
        }
        
        resp = requests.get(url, params = params)

        if resp.status_code == 200:
            return resp.json()
        else:
            return resp.text