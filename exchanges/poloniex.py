execfile("configs/poloniex_config.py")

import urllib
import hashlib
import hmac
import time
import requests

api_key = poloniex_config['api_public_key']
api_sec = poloniex_config['api_private_key']

def get_poloniex_signature(postdata, secret):
    mac = hmac.new(secret, postdata, hashlib.sha512)

    return mac.hexdigest()

def poloniex_request(uri_path, data, api_key, api_sec):
    headers = {}
    headers['Key'] = api_key
    postdata = urllib.urlencode(data)
    headers['Sign'] = get_poloniex_signature(postdata, api_sec)
    headers['Content-Type'] = 'application/x-www-form-urlencoded'
    req = requests.post((poloniex_config['api_domain'] + uri_path), headers=headers, data=postdata)
    
    return req

def get_default_params():
  
  return {
    'nonce': str(int(1000*time.time()))
  }

def get_pair(ticker):
  pairs = {
    'GRT': 'USDT_GRT'
  }
  pair = None

  try:
    pair = pairs[ticker]
  except:
    print('Unable to find ticker pair of ' + ticker)
  
  return pair

def get_balance():
  params = get_default_params()
  params['command'] = 'returnBalances'
  res = poloniex_request('/tradingApi', params, api_key, api_sec)

  return res.json()

def get_tickers_info(tickers):
  res = requests.get(poloniex_config['api_domain'] + '/public?command=returnTicker')

  return res.json()
