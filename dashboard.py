# pawan_master_algo_full_live.py
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
from streamlit_autorefresh import st_autorefresh
import requests, json, time, threading, websocket

# ===================================
# 1️⃣ AngelOne API + WebSocket
# ===================================
class AngelOneAPI:
    BASE_URL = "https://api.angelbroking.com/rest/secure/"

    def __init__(self, api_key, client_code, access_token):
        self.api_key = api_key
        self.client_code = client_code
        self.access_token = access_token
        self.live_data = {}
        self.candles_data = {}

    def get_latest(self,symbol):
        try:
            url=f"https://api.angelbroking.com/rest/secure/marketdata/ltp?exchange=NSE&tradingsymbol={symbol}"
            headers={"Authorization":f"Bearer {self.access_token}"}
            resp=requests.get(url,headers=headers,timeout=2)
            data=resp.json()
            return {'ltp':data.get('data',{}).get('ltp',0),'ai_confidence':0.75}
        except: return {'ltp':0,'ai_confidence':0}

    def get_candles(self,symbol,timeframe='5m',limit=200):
        try:
            url=f"https://api.angelbroking.com/rest/secure/marketdata/candle?exchange=NSE&tradingsymbol={symbol}&interval={timeframe}&count={limit}"
            headers={"Authorization":f"Bearer {self.access_token}"}
            resp=requests.get(url,headers=headers,timeout=2)
            df=pd.DataFrame(resp.json())
            df.index=pd.to_datetime(df['time'])
            df=df[['open','high','low','close']]
            self.candles_data[symbol]=df
            return df
        except: return pd.DataFrame()

    def place_order(self,symbol,side,quantity,price_type="MARKET"):
        try:
            url=self.BASE_URL+"order/placed"
            payload={
                "variety":"regular",
                "tradingsymbol":symbol,
                "symboltoken":"TOKEN",
                "transactiontype":side,
                "exchange":"NSE",
                "ordertype":price_type,
                "quantity":quantity,
                "producttype":"INTRADAY",
                "duration":"DAY"
            }
            headers={"Authorization":f"Bearer {self.access_token}","Content-Type":"application/json"}
            return requests.post(url,headers=headers,data=json.dumps(payload)).json()
        except: return None

    def start_ws(self,symbols):
        ws_url="wss://websocket.angelbroking.com/live"
        def on_message(ws,msg):
            try:
                data=json.loads(msg)
                symbol=data.get("symbol")
                ltp=data.get("ltp")
                if symbol and ltp: self.live_data[symbol]=ltp
            except: pass
        def on_error(ws,err): print("WS Error:",err)
        def on_close(ws,code,msg): print("WS Closed")
        def on_open(ws):
            for s in symbols: ws.send(json.dumps({"action":"subscribe","symbol":s}))
            print("WS Subscribed:",symbols)
        ws=websocket.WebSocketApp(ws_url,on_message=on_message,on_error=on_error,on_close=on_close,on_open=on_open)
        t=threading.Thread(target=ws.run_forever)
        t.daemon=True
        t.start()
        print("WS Thread Started")

# ===================================
# 2️⃣ Indicator Calculation
# ===================================
def calculate_indicators(prices):
    last=prices[-1]
    return {
        'Supertrend': True,
        'MACD': True,
        'MACD_Line': 0.5,
        'RSI': 72,
        'UpperBand': last+1,
        'Supertrend_MidCross': True,
        'Squeeze_Slope':0.3,
        'Spot_ATM': True
    }

# ===================================
# 3️⃣ Glassmorphism CSS
# ===================================
st.markdown("""
<style>
body {background: linear-gradient(135deg,#1e1e2f,#2c2c3e);color:white;font-family:Arial;}
.frosted-panel{background:rgba(255,255,255,0.1);backdrop-filter:blur(10px);
border-radius:15px;padding:20px;margin-bottom:20px;box-shadow:0 8px 32px 0 rgba(31,38,135,0.37);}
.supertrend{color:#00FF00;} .macd{color:#00FF00;} .rsi{color:#0000FF;}
.upperband{color:#FFFF00;} .midband{color:#FF69B4;} .squeeze{color:#00FF00;}
.diamond{color:#FFD700;}
</style>
""",unsafe_allow_html=True)

# ===================================
# 4️⃣ Initialize API & Signal Lab
# ===================================
api_key= "RKhSk9KM"
client_code="P362706"
PASSWORD = "5555"
TOTP_KEY  =  "SWO6GQESTOBCAWU5B5XAZ2U634"
symbols=["NIFTY","BANKNIFTY", ]
signal_lab=[]
api.start_ws(symbols)

# ===================================
# 5️⃣ Sidebar
# ===================================
st.sidebar.title("Pawan Master Algo System")
page=st.sidebar.radio("Navigation",[
    "Indicator Values","Signal Validator","Visual Validator","Orderbook & Positions",
    "Heatmap","Monitoring Room","Signal Lab","Settings"
])
st_autorefresh(interval=2000,key="dashboard_refresh")

# ===================================
# 6️⃣ Utility
# ===================================
def get_ltp(symbol): return api.live_data.get(symbol,api.get_latest(symbol)['ltp'])

# ===================================
# 7️⃣ Pages
# ===================================
def indicator_values_page():
    st.header("Live Indicator Values")
    table_data=[]
    for s in symbols:
        ltp=get_ltp(s)
        ind=calculate_indicators([ltp]*50)
        table_data.append({'Symbol':s,'LTP':ltp,
                           'Supertrend':"🟢" if ind['Supertrend'] else "🔴",
                           'MACD':"🟢" if ind['MACD'] else "🔴",
                           'MACD Line':round(ind['MACD_Line'],2),
                           'RSI':round(ind['RSI'],2),
                           'UpperBand':round(ind['UpperBand'],2),
                           'Midband Cross':"🌸" if ind['Supertrend_MidCross'] else "⚪",
                           'Squeeze Slope':round(ind['Squeeze_Slope'],2),
                           'Spot ATM':"💎" if ind['Spot_ATM'] else "⚪"})
    df=pd.DataFrame(table_data)
    st.markdown('<div class="frosted-panel">',unsafe_allow_html=True)
    st.write(df.to_html(escape=False),unsafe_allow_html=True)
    st.markdown('</div>',unsafe_allow_html=True)

def signal_validator_page():
    st.header("Signal Validator - 9 Entry Conditions")
    table_data=[]
    for s in symbols:
        ltp=get_ltp(s)
        ind=calculate_indicators([ltp]*50)
        cond1=ind['Supertrend']; cond2=ind['MACD']; cond3=ind['MACD_Line']>0; cond4=ind['RSI']>70
        cond5=ind['UpperBand']>ltp; cond6=ind['Supertrend_MidCross']; cond7=ind['Squeeze_Slope']>0; cond8=ind['Spot_ATM']
        cond9=cond1 and cond2 and cond3 and cond4 and cond5 and cond6 and cond7 and cond8
        timestamp=datetime.now().strftime("%H:%M:%S")
        signal_lab.append({'Symbol':s,'LTP':ltp,'Supertrend':timestamp if cond1 else None,'MACD':timestamp if cond2 else None,
                           'MACD_Line':timestamp if cond3 else None,'RSI':timestamp if cond4 else None,
                           'UpperBand':timestamp if cond5 else None,'Midband':timestamp if cond6 else None,
                           'Squeeze':timestamp if cond7 else None,'Spot_ATM':timestamp if cond8 else None,'Diamond':timestamp if cond9 else None})
        if cond9:
            api.place_order(symbol=s,side="BUY",quantity=1)
            api.place_order(symbol=s,side="SELL",quantity=1)
        table_data.append({'Symbol':s,'LTP':ltp,
                           'Supertrend':"🟢" if cond1 else "🔴",
                           'MACD':"🟢" if cond2 else "🔴",
                           'MACD Line':round(ind['MACD_Line'],2),
                           'RSI>70':"🔵" if cond4 else "⚪",
                           'UpperBand Rising':"🟡" if cond5 else "⚪",
                           'Midband Cross':"🌸" if cond6 else "⚪",
                           'Squeeze Slope':round(ind['Squeeze_Slope'],2),
                           'Spot ATM':"🟠" if cond8 else "⚪",
                           'Diamond':"💎" if cond9 else "⚪"})
    df=pd.DataFrame(table_data)
    st.markdown('<div class="frosted-panel">',unsafe_allow_html=True)
    st.write(df.to_html(escape=False),unsafe_allow_html=True)
    st.markdown('</div>',unsafe_allow_html=True)

def visual_validator_page():
    st.header("Visual Validator - Candlestick Overlay")
    for s in symbols:
        st.subheader(f"{s} Chart")
        candles=api.get_candles(s)
        if candles.empty: st.warning(f"No candles for {s}"); continue
        ltp=candles['close'].iloc[-1]
        ind=calculate_indicators(candles['close'].tolist())
        cond1=ind['Supertrend']; cond2=ind['MACD']; cond3=ind['MACD_Line']>0; cond4=ind['RSI']>70
        cond5=ind['UpperBand']>ltp; cond6=ind['Supertrend_MidCross']; cond7=ind['Squeeze_Slope']>0; cond8=ind['Spot_ATM']
        cond9=cond1 and cond2 and cond3 and cond4 and cond5 and cond6 and cond7 and cond8
        fig=go.Figure(data=[go.Candlestick(x=candles.index[-200:],open=candles['open'][-200:],
                                           high=candles['high'][-200:],low=candles['low'][-200:],
                                           close=candles['close'][-200:])])
        last_time=candles.index[-1]
        cond_list=[(cond1,'Supertrend','lime'),(cond2,'MACD','green'),(cond3,'MACD Line','green'),
                   (cond4,'RSI','blue'),(cond5,'UpperBand Rising','yellow'),(cond6,'Midband Cross','pink'),
                   (cond7,'Squeeze Slope','green'),(cond8,'Spot ATM','orange')]
        for c,name,color in cond_list:
            if c: fig.add_trace(go.Scatter(x=[last_time],y=[candles['high'].iloc[-1]*1.01],text=[name],
                                           mode='text',textfont=dict(color=color,size=12),showlegend=False))
        if cond9: fig.add_trace(go.Scatter(x=[last_time],y=[candles['high'].iloc[-1]*1.05],
                                           text=["💎"],mode='text',textfont=dict(color='gold',size=18),showlegend=False))
        st.markdown('<div class="frosted-panel">',unsafe_allow_html=True)
        st.plotly_chart(fig,use_container_width=True)
        st.markdown('</div>',unsafe_allow_html=True)

# ---------------- Other Pages ----------------
def orderbook_positions_page():
    st.header("Orderbook & Live Positions")
    table_data=[]
    for s in symbols:
        ltp=get_ltp(s)
        position=1
        pnl=round((ltp-100)*position,2)
        table_data.append({'Symbol':s,'Position':position,'LTP':ltp,'P&L':pnl})
    df=pd.DataFrame(table_data)
    st.markdown('<div class="frosted-panel">',unsafe_allow_html=True)
    st.dataframe(df)
    st.markdown('</div>',unsafe_allow_html=True)

def heatmap_page():
    st.header("Heatmap")
    table_data=[]
    for s in symbols:
        ltp=get_ltp(s)
        ind=calculate_indicators([ltp]*50)
        confidence=sum([cond for cond in [ind['Supertrend'],ind['MACD'],ind['MACD_Line']>0,
                                          ind['RSI']>70,ind['UpperBand']>ltp,ind['Supertrend_MidCross'],
                                          ind['Squeeze_Slope']>0,ind['Spot_ATM']]])/8
        table_data.append({'Symbol':s,'Confidence':confidence})
    df=pd.DataFrame(table_data)
    st.markdown('<div class="frosted-panel">',unsafe_allow_html=True)
    st.dataframe(df.style.background_gradient(cmap='Viridis'))
    st.markdown('</div>',unsafe_allow_html=True)

def monitoring_room_page():
    st.header("Monitoring Room")
    table_data=[]
    for s in symbols:
        ltp=get_ltp(s)
        ind=calculate_indicators([ltp]*50)
        table_data.append({'Symbol':s,'LTP':ltp,
                           'Supertrend':ind['Supertrend'],'MACD':ind['MACD'],
                           'MACD_Line':ind['MACD_Line'],'RSI>70':ind['RSI']>70,
                           'UpperBand Rising':ind['UpperBand']>ltp,'Midband Cross':ind['Supertrend_MidCross'],
                           'Squeeze Slope':ind['Squeeze_Slope'],'Spot ATM':ind['Spot_ATM']})
    df=pd.DataFrame(table_data)
    st.markdown('<div class="frosted-panel">',unsafe_allow_html=True)
    st.dataframe(df)
    st.markdown('</div>',unsafe_allow_html=True)

def signal_lab_page():
    st.header("Signal Lab - Timestamps")
    if len(signal_lab)==0: st.info("No signals yet."); return
    df=pd.DataFrame(signal_lab)
    st.markdown('<div class="frosted-panel">',unsafe_allow_html=True)
    st.dataframe(df)
    st.markdown('</div>',unsafe_allow_html=True)

def settings_page():
    st.header("Settings")
    st.markdown('<div class="frosted-panel">',unsafe_allow_html=True)
    bg_color=st.color_picker("Background Start","#1e1e2f")
    text_color=st.color_picker("Text Color","white")
    st.markdown(f"<style>body{{background:linear-gradient(135deg,{bg_color},#2c2c3e);color:{text_color};}}</style>",unsafe_allow_html=True)
    st.markdown('</div>',unsafe_allow_html=True)

# ===================================
# 8️⃣ Page Routing
# ===================================
if page=="Indicator Values": indicator_values_page()
elif page=="Signal Validator": signal_validator_page()
elif page=="Visual Validator": visual_validator_page()
elif page=="Orderbook & Positions": orderbook_positions_page()
elif page=="Heatmap": heatmap_page()
elif page=="Monitoring Room": monitoring_room_page()
elif page=="Signal Lab": signal_lab_page()
elif page=="Settings": settings_page()
else: st.info("Select a page from sidebar")
