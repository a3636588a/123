import requests
import talib
import numpy as np
import  matplotlib as mpl
mpl.use('tkagg')
import  matplotlib.pyplot as plt
import asyncio
import keyboard

API_KEY = "9eIgMtPBxAHlK40ixEhm2Hk5xTI4nihBrXDys1FIDmEvs1a3URLi70w8jaXW23Wi"
BASE_URL = "https://api.binance.com/api/v3/"


class GETPRICE:

    def __init__(self,symbol,BASE_URL):#獲取交易對
        self.symbol = symbol
        self.BASE_URL = BASE_URL

    def price(self):
        base_url = BASE_URL+"ticker/price"
        params = {"symbol": self.symbol}
        response = requests.get(base_url, params=params)
        data = response.json()
    
        if "price" in data:                         
            return data["price"]
        else:
            return None

    def get_hourly_klines(self, interval, limit):
        base_url= BASE_URL+"klines"
        params={
            "symbol" : self.symbol,
            "interval": interval,
            "limit" : limit
        }
        response = requests.get(base_url, params=params)
        data = response.json()

        close_price = np.array([np.around(float(kline[4]), 2) for kline in data])
        return close_price




class MACD4C:
    
    def __init__(self,close_price,fast=9,slow=11,signal=9):
        self.close_price = close_price
        self.fast = fast 
        self.slow =slow
        self.signal = signal

    def calculate_macd(self): #macd產生
        macd, signal, hist = talib.MACD(self.close_price, 
                                        fastperiod=self.fast, 
                                        slowperiod=self.slow, 
                                        signalperiod=self.signal)
        return macd, signal, hist

    def bullish_divergence(self): #底背離
        macd, signal, _ = self.calculate_macd()
        prev_macd = np.roll(macd, 1)
        bullish_divergence_indices = np.where((macd > 0) & (macd > prev_macd))[0]
        return bullish_divergence_indices

def plt_all():
    plt.figure(figsize=(10, 8))

    plt.subplot(3, 1, 1)
    plt.plot(close_price, label="Close Prices")
    plt.title("BTC/USDT Close Prices")
    plt.legend()

    plt.subplot(3, 1, 2)
    plt.plot(cal_macd4c[0], label="MACD")
    plt.plot(cal_macd4c[1], label="Signal Line")
    plt.title("MACD Indicator")
    plt.legend()

    plt.subplot(3, 1, 3)
    macd_histogram = cal_macd4c[2]
    plt.bar(range(len(macd_histogram)), macd_histogram, color=['red' if val >= 0 else 'black' for val in macd_histogram])
    plt.axhline(0, color='black', linewidth=0.8, linestyle='--')
    plt.title("MACD Histogram")

    plt.tight_layout()
    plt.show()

        
if __name__ == "__main__":
    BTC =GETPRICE("BTCUSDT",BASE_URL)  # 比特幣對美元的交易對                                        
    price = BTC.price()                                                                              
    print(f"{BTC.symbol} :最新價格{price}")                                                          
    close_price = BTC.get_hourly_klines(interval="1h", limit=720)
    print(close_price)
    macd4c = MACD4C(close_price)
    cal_macd4c = macd4c.calculate_macd()
    #print(cal_macd4c)

                                                                                  
                                                                                                        
                                                                                                        
                                                              

    
    
    




