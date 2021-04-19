execfile("configs/iotc_config.py")
execfile("configs/config.py")

import utils.exchange as Exchange_utils
import utils.iotc as Iotc_utils
from time import sleep

def query_exchange(res, Exchange, Exchange_specific_utils, exchange):
  balance_res = Exchange.get_balance()
  
  tickers = []
  for ticker in balance_res:
    if float(balance_res[ticker]) > 0:
      tickers.append(ticker)
  
  tickers_info_res = Exchange.get_tickers_info(tickers)

  available_tickers = []
  tickers_data = {}
  current_crypto_total_market_value = 0
  current_stock_total_market_value = 0

  for ticker in tickers:
    try:
      if ticker == 'USDT':
        current_price = 1.0
      else:
        current_price = Exchange_specific_utils.get_current_price(tickers_info_res, Exchange, ticker)

      current_market_value = float(balance_res[ticker]) * current_price
      print(ticker + ' is now worth USD$' + str(current_market_value))
      
      if current_market_value >= config['minimum_value'] and (ticker in iotc_config['available_cryptocurrency'] or ticker in iotc_config['available_stock']):
        available_tickers.append(ticker)
        tickers_data[ticker] = [current_price, current_market_value, float(balance_res[ticker])]
        
        if ticker in iotc_config['available_cryptocurrency']:
          current_crypto_total_market_value += current_market_value
        else:
          current_stock_total_market_value += current_market_value
    except:
      pass

  if Exchange_utils.include_cryptocurrency(exchange):
    res[Iotc_utils.get_current_exchange_total_market_value_key(exchange)] = current_crypto_total_market_value
  else:
    res[Iotc_utils.get_current_exchange_total_market_value_key(exchange)] = current_stock_total_market_value

  return Iotc_utils.transform_tickers_and_data_to_telemetries(res, available_tickers, tickers_data, {
    'CurrentCryptoTotalMarketValue': current_crypto_total_market_value,
    'CurrentStockTotalMarketValue': current_stock_total_market_value,
    'CurrentTotalMarketValue': current_crypto_total_market_value + current_stock_total_market_value
  })

while(True):
  res = {}

  for exchange in config['exchange_to_be_run']:
    if exchange in config['available_exchange']:
      res = query_exchange(res, Exchange_utils.get_exchange_client(exchange), Exchange_utils.get_exchange_utils(exchange), exchange)
  
  Iotc_utils.send_telemetry(res)
  sleep(10)
