#Notes: 
#1.Have to sync windows time
#2.Have to $ pip install -r requirements.txt

#Useful Links:
#1. https://mrjbq7.github.io/ta-lib/
#2. https://vectorbt.pro/api/indicators/#vectorbtpro.indicators.ta
#3. https://github.com/bukosabino/ta
#4. https://technical-analysis-library-in-python.readthedocs.io/en/latest/
#5. https://vectorbt.dev/api/indicators/basic/
from datetime import datetime, timezone
import string
import vectorbt as vbt
import pandas as pd
import config
from manager import manager
import schedule
import time

def data_setup(reset = False):
    #TODO: Set up data collection from specified exchange
    #If no prev data get X amount of Y timeframe candles and put in csv
    #If further session calls keep adding 1 row at Y timeframe to csv
    starttime = "10 minutes ago UTC"
    if reset: 
        dt_string = datetime.now(timezone.utc).strftime("%d/%m/%Y %H:%M:%S")
        print("STARTING AT UTC: ", dt_string)
        starttime = "2 days ago UTC"
    coindata = vbt.CCXTData.download_symbol(
        symbol=config.COINPAIR,
        exchange = config.EXCHANGE,
        config = config.EXCHANGECONFIG, 
        start = starttime, 
        timeframe = "5m"
    )
    coindata = coindata[:-1]
    if reset:
        coindata.to_csv('data/ExchangeData.csv')
    else:         
        coindata.to_csv('data/ExchangeData.csv', mode = "a", header = False)        

def get_data(filepath:string):
    df = pd.read_csv(filepath).tail(500)
    return df

def technical_strategy(data):
    #Technical indicators
    ema1 = vbt.ta("EMAIndicator").run(data['Close'], window=1)
    ema100 = vbt.ta("EMAIndicator").run(data['Close'], window=100)
    psar = vbt.ta("PSARIndicator").run(data['High'], data['Low'], data['Close'], 0.06, 0.5)
    macd = vbt.MACD.run(data['Close'], fast_window = 7, slow_window = 24, signal_window = 9)
    atr = vbt.ATR.run(data['High'], data['Low'], data['Close'], window = 5)
    frame = {
             'ema1': ema1.ema_indicator,
             'ema100': ema100.ema_indicator,
             'macd_macd': macd.macd,
             'macd_signal': macd.signal,
             'psar': psar.psar,
             'atr': atr.atr
             }
    data_technicals = pd.DataFrame(frame, index=data.index)
    return data_technicals

if False:    
    def run():
        data_setup()
        data = get_data('data/ExchangeData.csv').reset_index()
        data_tech = technical_strategy(data)
        acc = manager(data_tech)
        print(acc.order_test_df())

    if __name__ == '__main__':
        data_setup(reset = True)
        schedule.every(1).minutes.do(run)

    #Scheduler init
    while(True):
        schedule.run_pending()
        time.sleep(1)
    
    
