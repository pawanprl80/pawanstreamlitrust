# signal_utils.py

def bullish_conditions_met(conds):
    # Check if all 8 conditions are bullish
    return all([
        conds['Supertrend'], conds['MACD'], conds['MACD_ZeroCross'],
        conds['Price_RSI_Cross'], conds['UpperBand_Rising'],
        conds['Supertrend_MidBand'], conds['Squeeze_Slope'],
        conds['SpotPrice_ATM']
    ])

def bearish_conditions_met(conds):
    # Inverse logic for bearish
    return all([
        not conds['Supertrend'], not conds['MACD'], not conds['MACD_ZeroCross'],
        not conds['Price_RSI_Cross'], not conds['UpperBand_Rising'],
        not conds['Supertrend_MidBand'], conds['Squeeze_Slope']<0,
        not conds['SpotPrice_ATM']
    ])

def calculate_qty(symbol):
    # Replace with position sizing logic
    return 1

def check_mismatch(symbol, local, angel):
    mismatches = []
    for k in local.keys():
        if k in angel and local[k] != angel[k]:
            mismatches.append(k)
    return mismatches
