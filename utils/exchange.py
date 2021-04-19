import exchanges.kraken as Kraken
import exchanges.poloniex as Poloniex
import exchanges.questrade as Questrade
import utils.kraken as Kraken_utils
import utils.poloniex as Poloniex_utils
import utils.questrade as Questrade_utils

def get_exchange_client(exchange):
  available_exchange = {
    'kraken': Kraken,
    'poloniex': Poloniex,
    'questrade': Questrade
  }

  return available_exchange[exchange]

def get_exchange_utils(exchange):
  utils = {
    'kraken': Kraken_utils,
    'poloniex': Poloniex_utils,
    'questrade': Questrade_utils
  }

  return utils[exchange]

def include_cryptocurrency(exchange):
  cryptocurrency_exchange = {
    'kraken': Kraken,
    'poloniex': Poloniex
  }

  return exchange in cryptocurrency_exchange
