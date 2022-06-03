#This is config for ccxt BINANCE  
#MAKE SURE TO SYNC WINDOWS TIME 
BINANCE_API_KEY = ''
BINANCE_SECRET_KEY = ''

#Trading config
COINPAIR = 'ETH/USDT'
EXCHANGE = 'binance'
EXCHANGECONFIG = {
    'apiKey': BINANCE_API_KEY,
    'secret': BINANCE_SECRET_KEY,
    'options': {
        'defaultType': 'future'#enables futures market
    },
    'marginType': 'ISOLATED'
}
