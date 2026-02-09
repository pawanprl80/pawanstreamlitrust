# backend_api.py
import random

class AngelOneAPI:
    def __init__(self):
        # Initialize connection to AngelOne API with API key / credentials
        pass
    
    def get_latest(self, symbol):
        # Replace with actual API call
        ltp = random.uniform(100, 200)
        indicators = {
            'Supertrend': random.choice([True, False]),
            'MACD': random.choice([True, False]),
            'MACD_Line': random.uniform(-2,2),
            'RSI': random.uniform(0,100),
            'UpperBand': random.uniform(100,200),
            'Supertrend_MidCross': random.choice([True, False]),
            'Squeeze_Slope': random.uniform(-1,1),
            'Spot_ATM': random.choice([True, False])
        }
        return {'ltp': ltp, 'indicators': indicators}
    
    def get_positions(self):
        # Replace with real positions API call
        return [
            {'Symbol': 'NIFTY', 'Qty': 1, 'Entry': 150, 'LTP': 151, 'P/L': 1.0},
            {'Symbol': 'BANKNIFTY', 'Qty': 1, 'Entry': 350, 'LTP': 348, 'P/L': -2.0}
        ]
    
    def place_order(self, trade_type, symbol, qty):
        print(f"Placing {trade_type} order for {symbol} qty={qty}")
