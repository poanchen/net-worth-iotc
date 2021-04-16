import exchanges.kraken as Kraken
import exchanges.poloniex as Poloniex
import utils.kraken as Kraken_utils
import utils.poloniex as Poloniex_utils

def get_exchange_client(exchange):
  available_exchange = {
    'kraken': Kraken,
    'poloniex': Poloniex
  }

  return available_exchange[exchange]

def get_exchange_utils(exchange):
  utils = {
    'kraken': Kraken_utils,
    'poloniex': Poloniex_utils
  }

  return utils[exchange]
