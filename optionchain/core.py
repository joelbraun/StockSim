import requests

from pandas import DataFrame
from requests.exceptions import ConnectionError

OPTION_CHAIN_URL = 'https://www.google.com/finance/option_chain'

import json
import token, tokenize

from io import *


# using below solution fixes the json output from google
# http://stackoverflow.com/questions/4033633/handling-lazy-json-in-python-expecting-property-name
def fixLazyJson (in_text):
    tokengen = tokenize.generate_tokens(StringIO(in_text).readline)

    result = []
    for tokid, tokval, _, _, _ in tokengen:
        # fix unquoted strings
        if (tokid == token.NAME):
            if tokval not in ['true', 'false', 'null', '-Infinity', 'Infinity', 'NaN']:
                tokid = token.STRING
                tokval = u'"%s"' % tokval

        # fix single-quoted strings
        elif (tokid == token.STRING):
            if tokval.startswith ("'"):
                tokval = u'"%s"' % tokval[1:-1].replace ('"', '\\"')

        # remove invalid commas
        elif (tokid == token.OP) and ((tokval == '}') or (tokval == ']')):
            if (len(result) > 0) and (result[-1][1] == ','):
                result.pop()

        # fix single-quoted strings
        elif (tokid == token.STRING):
            if tokval.startswith ("'"):
                tokval = u'"%s"' % tokval[1:-1].replace ('"', '\\"')

        result.append((tokid, tokval))

    return tokenize.untokenize(result)


def json_decode(json_string):
    try:
        ret = json.loads(str(json_string))
    except:
        json_string = fixLazyJson(str(json_string))
        ret = json.loads(fixLazyJson(str(json_string[2:-1])))

    return ret

class OptionChain(object):

    def __init__(self, q):
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

        data = self._get_content(OPTION_CHAIN_URL, params)

        # get first calls and puts
        calls = data['calls']
        puts = data['puts']

        for (ctr, exp) in enumerate(data['expirations']):
            # we already got the first put and call
            # skip first
            if ctr:
                params['expd'] = exp['d']
                params['expm'] = exp['m']
                params['expy'] = exp['y']

                new_data = self._get_content(OPTION_CHAIN_URL, params)

                if new_data.get('calls') is not None:
                    calls += new_data.get('calls')

                if new_data.get('puts') is not None:
                    puts += new_data.get('puts')

        self.calls = calls
        self.puts = puts


    def to_excel(self, puts_path='/tmp/puts.xls', calls_path='/tmp/calls.xls'):
        dataframe = DataFrame(data=self.puts)
        dataframe.to_excel(puts_path)
        print ('Puts saved at %s' % (puts_path))
        dataframe = DataFrame(data=self.calls)
        dataframe.to_excel(calls_path)
        print('Calls saved at %s' % (calls_path))


    def _get_content(self, url, params):
        response = requests.get(url, params=params)
        if response.status_code == 200:
            content_json = response.content
            data = json_decode(content_json)

            return data
