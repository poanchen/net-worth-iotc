def get_current_price(tickers_info_res, Exchange, ticker):
  i = 0
  for ticker_info in tickers_info_res:
    if str(ticker_info['symbolId']) == str(ticker):
      break
    i+=1
  
  if tickers_info_res[i]['askPrice'] == None:
    return float(tickers_info_res[i]['lastTradePrice'])

  return float(tickers_info_res[i]['askPrice'])
