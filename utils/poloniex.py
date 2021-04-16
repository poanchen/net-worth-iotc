def get_current_price(tickers_info_res, Exchange, ticker):
  return float(tickers_info_res[Exchange.get_pair(ticker)]['highestBid'])
