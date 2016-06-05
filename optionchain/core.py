import requests

from pandas import DataFrame
from requests.exceptions import ConnectionError
from utils import json_decode

OPTION_CHAIN_URL = 'https://www.google.com/finance/option_chain'


class OptionChain(object):

    def __init__(self, q, ps):
        """
        Usage: 
        from optionchain import OptionChain
        oc = OptionChain('NASDAQ:AAPL')
        # oc.calls 
        # oc.puts
        """

        params = {
            'q': q,
            'output': 'json'
        }
        params.update(ps)
        print(params)

        data = self._get_content(OPTION_CHAIN_URL, params)
        # get first calls and puts
        calls = data['calls']
        puts = data['puts']


        self.calls = calls
        self.puts = puts


    def to_excel(self, puts_path='/tmp/puts.xls', calls_path='/tmp/calls.xls'):
        dataframe = DataFrame(data=self.puts)
        dataframe.to_excel(puts_path)
        print 'Puts saved at %s' % (puts_path)
        dataframe = DataFrame(data=self.calls)
        dataframe.to_excel(calls_path)
        print 'Calls saved at %s' % (calls_path)


    def _get_content(self, url, params):
        response = requests.get(url, params=params)
        print(response.url)
        if response.status_code == 200:
            content_json = response.content
            data = json_decode(content_json)

            return data
