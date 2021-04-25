execfile("configs/questrade_config.py")

import requests
import urllib
import utils.cosmosdb as Cosmosdb_utils

def request_new_access_token_from_questrade(refresh_token):
  data = {
    'grant_type': 'refresh_token',
    'refresh_token': refresh_token
  }
  params = urllib.urlencode(data)
  res = requests.get('%s?%s' % (questrade_config['api_auth_domain'], params))

  return res.json()

def get_questrade_access_token(exchange):
  token = Cosmosdb_utils.get_access_token(exchange)

  try:
    return {
      "access_token": token['access_token'],
      "api_server": token['api_server']
    }
  except:
    new_access_token = request_new_access_token_from_questrade(token['refresh_token'])

    Cosmosdb_utils.add_new_access_token(exchange, new_access_token)
    Cosmosdb_utils.update_to_new_refresh_token(exchange, new_access_token)

    return new_access_token

def questrade_request(uri_path):
  access_token_res = get_questrade_access_token('questrade')

  headers = {
    'Authorization': 'Bearer %s' % access_token_res['access_token'],
  }

  res = requests.get('%s%s' % (access_token_res['api_server'], uri_path), headers=headers)

  return res

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

def get_accounts():
  res = questrade_request('v1/accounts')

  return res.json()

def get_balance():
  res = get_accounts()
  combined_positions = {}

  print("Found %s account(s) in questrade." % len(res['accounts']))

  for account in res['accounts']:
    positions_res = questrade_request('v1/accounts/%s/positions' % account['number']).json()
    for position in positions_res['positions']:
      try:
        combined_positions[str(position['symbolId'])] += position['openQuantity']
      except:
        combined_positions[str(position['symbolId'])] = position['openQuantity']
  
  return combined_positions

def get_tickers_info(tickers):
  data = ','.join(tickers)
  res = questrade_request('v1/markets/quotes?ids=%s' % (data))

  return res.json()['quotes']
