dashboard.py - Full Pawan Master Algo System Single Script

import streamlit as st import pandas as pd import plotly.graph_objects as go import requests import time

=========================

Config & Symbols

=========================

RUST_URL = "http://127.0.0.1:8080" symbols = ["NIFTY", "BANKNIFTY", "BTCUSDT", "ETHUSDT"] timeframes = ['1m','5m','15m','1h'] REFRESH_INTERVAL = 1 ROTATE_INTERVAL = 5

=========================

CSS for Glassmorphism

=========================

st.markdown("""

<style>
body {
    background: linear-gradient(135deg, #1e1e2f, #2c2c3e);
    color: white;
}
.frosted-panel {
    background: rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(10px);
    border-radius: 15px;
    padding: 20px;
    margin-bottom: 20px;
    box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
    transition: all 0.5s ease-in-out;
}
.progress-bar {
    width: 100%;
    background-color: rgba(255,255,255,0.2);
    border-radius: 5px;
    margin-bottom: 10px;
    overflow: hidden;
}
.progress-bar-inner {
    height: 10px;
    background-color: limegreen;
    border-radius: 5px;
    transition: width 0.5s linear;
}
</style>""", unsafe_allow_html=True)

=========================

Helper Functions

=========================

def get_ltp(symbol): try: return requests.get(f"{RUST_URL}/ltp/{symbol}").json() except: return 0

def get_indicators(symbol): try: return requests.get(f"{RUST_URL}/indicators/{symbol}").json() except: return {}

def check_diamond(indicators): return indicators.get('diamond', False)

def log_signal(symbol, indicators): timestamp = time.strftime("%Y-%m-%d %H:%M:%S") row = [timestamp, symbol] + list(indicators.values()) import os os.makedirs('signal_lab', exist_ok=True) with open("signal_lab/signal_log.csv", "a") as f: f.write(",".join(map(str, row)) + "\n")

def auto_trade(symbol, indicators): if check_diamond(indicators): st.toast(f"Diamond Trigger for {symbol} → Execute BUY/SELL", icon="💎") log_signal(symbol, indicators)

=========================

Sidebar Navigation

=========================

st.sidebar.title("Pawan Master Algo System") page = st.sidebar.radio("Navigation", [ 'Visual Validator', 'Signal Validator', 'Heatmap', 'Signal Lab', 'Monitoring', 'Orders', 'Settings' ])

=========================

Pages Implementation

=========================

if page == 'Visual Validator': st.markdown('<div class="frosted-panel">', unsafe_allow_html=True) st.header("Visual Validator - Multi-Symbol Scroll") for symbol in symbols: with st.expander(f"{symbol}", expanded=False): ltp = get_ltp(symbol) indicators = get_indicators(symbol) auto_trade(symbol, indicators) st.write(f"LTP: {ltp}, Diamond: {indicators.get('diamond')}")

elif page == 'Signal Validator': st.markdown('<div class="frosted-panel">', unsafe_allow_html=True) st.header("Signal Validator - 9 Entry Conditions") for symbol in symbols: indicators = get_indicators(symbol) auto_trade(symbol, indicators) st.write(f"{symbol} Indicators:") for k,v in indicators.items(): st.write(f"{k}: {v}")

elif page == 'Heatmap': st.markdown('<div class="frosted-panel">', unsafe_allow_html=True) st.header("AI Confidence Heatmap") data = pd.DataFrame({ "Symbol": symbols, "Diamond": [get_indicators(s).get('diamond') for s in symbols] }) st.dataframe(data.style.background_gradient(cmap="Viridis"))

elif page == 'Signal Lab': st.markdown('<div class="frosted-panel">', unsafe_allow_html=True) st.header("Signal Lab Logs") try: logs = pd.read_csv("signal_lab/signal_log.csv", header=None) st.dataframe(logs) except FileNotFoundError: st.write("No logs yet.")

elif page == 'Monitoring': st.markdown('<div class="frosted-panel">', unsafe_allow_html=True) st.header("Monitoring Room") st.write("Monitoring real-time trades, LTPs and diamond signals...") for symbol in symbols: ltp = get_ltp(symbol) indicators = get_indicators(symbol) st.write(f"{symbol}: LTP={ltp}, Diamond={indicators.get('diamond')}")

elif page == 'Orders': st.markdown('<div class="frosted-panel">', unsafe_allow_html=True) st.header("Order Execution Status") st.write("Placeholder for live orders and execution details")

elif page == 'Settings': st.markdown('<div class="frosted-panel">', unsafe_allow_html=True) st.header("Settings") st.write("API keys, refresh intervals, symbol configuration, and other settings")
