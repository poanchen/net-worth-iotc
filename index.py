execfile("configs/iotc_config.py")
execfile("configs/config.py")

from exchanges.kraken import get_balance, get_tickers_info, get_pair
from utils.iotc import send_telemetry, transform_tickers_and_data_to_telemetries
from time import sleep

while(True):
  balance_res = get_balance()
  tickers = []
  for ticker in balance_res['result']:
    tickers.append(ticker)

  tickers_info_res = get_tickers_info(tickers)
  available_tickers = []
  tickers_data = {}
  current_crypto_total_market_value = 0

  for ticker in balance_res['result']:
    try:
      current_price = float(tickers_info_res['result'][get_pair(ticker)]['a'][0])
      current_market_value = float(balance_res['result'][ticker]) * current_price
      print(ticker + ' is now worth USD$' + str(current_market_value))
      
      if current_market_value >= config['minimum_value'] and ticker in iotc_config['available_coins']:
        available_tickers.append(ticker)
        tickers_data[ticker] = [current_price, current_market_value, float(balance_res['result'][ticker])]
        current_crypto_total_market_value = current_crypto_total_market_value + current_market_value
    except:
      pass

  send_telemetry(transform_tickers_and_data_to_telemetries(available_tickers, tickers_data, {
    'CurrentCryptoTotalMarketValue': current_crypto_total_market_value
  }))
  sleep(60)
