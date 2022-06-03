import ccxt
import config
import pandas as pd

#given a dataframe with last candle technicals
class manager:
    exchange = ccxt.binance(config.EXCHANGECONFIG)
    #Recieves a df with technical indicator values
    def __init__(self, df:pd.DataFrame):
        entries, exits = [], []
        data = df.copy(deep=True)
        for index, r in data.iterrows():       
            enter_check = r['ema1'] > r['psar'] and r['macd_macd'] > r['macd_signal'] and r['ema1'] > r['ema100']
            entries.append(enter_check)
            exit_check = r['psar'] > r['ema1'] and r['macd_signal'] > r['macd_macd'] and r['ema100'] > r['ema1']
            exits.append(exit_check)
        data['entry'] = entries
        data['exit'] = exits
        self.data = data
    
    #Return df with entry and exit position times
    def order_test_df(self):
        return pd.concat([self.data['entry'], self.data['exit']], axis=1)     
    
    #print our main df
    def order_print_df(self):
        print(self.data)