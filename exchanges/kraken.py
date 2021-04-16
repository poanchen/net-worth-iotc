execfile("configs/kraken_config.py")

import urllib
import hashlib
import hmac
import base64
import time
import requests

api_key = kraken_config['api_public_key']
api_sec = kraken_config['api_private_key']

def get_kraken_signature(urlpath, data, secret):
    postdata = urllib.urlencode(data)
    encoded = (str(data['nonce']) + postdata).encode()
    message = urlpath.encode() + hashlib.sha256(encoded).digest()
    mac = hmac.new(base64.b64decode(secret), message, hashlib.sha512)
    sigdigest = base64.b64encode(mac.digest())
    
    return sigdigest.decode()

def kraken_request(uri_path, data, api_key, api_sec):
    headers = {}
    headers['API-Key'] = api_key
    headers['API-Sign'] = get_kraken_signature(uri_path, data, api_sec)             
    req = requests.post((kraken_config['api_domain'] + uri_path), headers=headers, data=data)
    
    return req

def get_default_params():
  
  return {
    'nonce': str(int(1000*time.time()))
  }

def get_pair(ticker):
  pairs = {
    'XXLM': 'XLMUSD',
    'SC': 'SCUSD',
    'XXBT': 'XXBTZUSD',
    'XXRP': 'XRPUSD',
    'DOT.S': 'DOTUSD',
    'USDT': 'USDTUSD',
    'XETH': 'XETHZUSD',
    'ADA': 'ADAUSD',
    'UNI': 'UNIUSD',
    'FIL': 'FILUSD',
    'XREP': 'REPUSD',
  }
  pair = None

  try:
    pair = pairs[ticker]
  except:
    print('Unable to find ticker pair of ' + ticker)
  
  return pair

def transform_tickers_to_pairs(tickers):
  pairs = []
  
  for ticker in tickers:
    pair = get_pair(ticker)
    if pair != None:
      pairs.append(pair)

  return pairs

def get_balance():
  params = get_default_params()
  res = kraken_request('/0/private/Balance', params, api_key, api_sec)

  return res.json()

def get_tickers_info(tickers):
  params = get_default_params()
  params['pair'] = ','.join(transform_tickers_to_pairs(tickers))
  res = kraken_request('/0/public/Ticker', params, api_key, api_sec)
  
  return res.json()
