execfile("configs/iotc_config.py")

import requests

def transform_tickers_and_data_to_telemetries(res, tickers, data, additional_data):
  ticker_and_data_to_telemetry = {
    'SC': ['CurrentAskPriceForSiacoin', 'CurrentSiacoinTotalMarketValue', 'NumberOfSiacoin'],
    'XXBT': ['CurrentAskPriceForBitcoin', 'CurrentBitcoinTotalMarketValue', 'NumberOfBitcoin'],
    'DOT.S': ['CurrentAskPriceForPolkadot', 'CurrentPolkadotTotalMarketValue', 'NumberOfPolkadot'],
    'XETH': ['CurrentAskPriceForEthereum', 'CurrentEthereumTotalMarketValue', 'NumberOfEthereum'],
    'UNI': ['CurrentAskPriceForUniswap', 'CurrentUniswapTotalMarketValue', 'NumberOfUniswap'],
    'GRT': ['CurrentAskPriceForTheGraph', 'CurrentTheGraphTotalMarketValue', 'NumberOfTheGraph'],

    # questrade stock symbol ids
    '19719': ['CurrentAskPriceForGameStop', 'CurrentGameStopTotalMarketValue', 'NumberOfGameStop'],
    '34113874': ['CurrentAskPriceForRoblox', 'CurrentRobloxTotalMarketValue', 'NumberOfRoblox'],
    '32466046': ['CurrentAskPriceForPalantir', 'CurrentPalantirTotalMarketValue', 'NumberOfPalantir'],
    '27116163': ['CurrentAskPriceForCloudflare', 'CurrentCloudflareTotalMarketValue', 'NumberOfCloudflare'],
    '33418187': ['CurrentAskPriceForAirbnb', 'CurrentAirbnbTotalMarketValue', 'NumberOfAirbnb'],
    '25766645': ['CurrentAskPriceForFastly', 'CurrentFastlyTotalMarketValue', 'NumberOfFastly'],
    '32220649': ['CurrentAskPriceForUnity', 'CurrentUnityTotalMarketValue', 'NumberOfUnity']
  }

  try:
    for ticker in tickers:
      res[ticker_and_data_to_telemetry[ticker][0]] = data[ticker][0]

      try:
        res[ticker_and_data_to_telemetry[ticker][1]] += data[ticker][1]
      except:
        res[ticker_and_data_to_telemetry[ticker][1]] = data[ticker][1]

      try:
        res[ticker_and_data_to_telemetry[ticker][2]] += data[ticker][2]
      except:
        res[ticker_and_data_to_telemetry[ticker][2]] = data[ticker][2]
  except:
    pass

  for key in additional_data:
    if additional_data[key] > 0:
      try:
        res[key] += additional_data[key]
      except:
        res[key] = additional_data[key]

  return res

def send_telemetry(data):
  response = requests.post("""%s?code=%s""" % (iotc_config['api_domain'], iotc_config['api_code']), json = {
    'device': {
      'deviceId': iotc_config['device_id']
    },
    "measurements": data
  })
  print("Done sending telemetry data to Azure IoT Central and the result was %s" % response.status_code)

def get_current_exchange_total_market_value_key(exchange):
  available_exchange = {
    'kraken': 'CurrentKrakenTotalMarketValue',
    'poloniex': 'CurrentPoloniexTotalMarketValue',
    'questrade': 'CurrentQuestradeTotalMarketValue'
  }

  return available_exchange[exchange]
