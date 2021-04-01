import yfinance as yf

msft = yf.Ticker("MSFT")

hist = msft.history(period='1d', interval='1m')
print(hist)
