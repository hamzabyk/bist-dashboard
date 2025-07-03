import yfinance as yf
import pandas as pd
import streamlit as st

st.set_page_config(page_title="BIST Dashboard", layout="wide")
st.title("📊 Borsa İstanbul Dashboard")

tickers = ["ASELS.IS", "THYAO.IS", "SISE.IS", "KRDMD.IS", "BIMAS.IS"]
ticker = st.selectbox("Hisse Seçin", tickers)

# Veri çek
df = yf.download(ticker, period="6mo")

# 👉 Çok katmanlı sütunları düzleştir
if isinstance(df.columns, pd.MultiIndex):
    df.columns = df.columns.droplevel(1)

# Test: tablo göster
st.write("Son 5 Günlük Veri:")
st.write(df.tail())

# Teknik göstergeler
df["MA20"] = df["Close"].rolling(window=20).mean()

delta = df["Close"].diff()
gain = delta.where(delta > 0, 0)
loss = -delta.where(delta < 0, 0)
avg_gain = gain.rolling(window=14).mean()
avg_loss = loss.rolling(window=14).mean()
rs = avg_gain / avg_loss
df["RSI"] = 100 - (100 / (1 + rs))

# Grafikler
st.subheader("📈 Kapanış ve MA20")
st.line_chart(df[["Close", "MA20"]])

st.subheader("📊 Hacim")
st.bar_chart(df["Volume"])

st.subheader("📉 RSI")
st.line_chart(df["RSI"])


