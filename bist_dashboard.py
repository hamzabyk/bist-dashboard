import yfinance as yf
import pandas as pd
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="BIST Dashboard", layout="wide")

# ——— Resmi ve Detaylı Başlık + Açıklama ———
st.markdown("""
# 📈 Borsa İstanbul Hisse Senedi Analiz Paneli

Bu platform, seçili Borsa İstanbul hisselerine ilişkin temel teknik analiz verilerini sade ve anlaşılır bir şekilde sunmayı amaçlamaktadır.  
Kullanıcılar, aşağıdaki seçeneklerden bir hisse senedi seçerek ilgili hisseye ait fiyat, hacim ve teknik göstergeleri takip edebilirler.

---
""")

st.title("📊 Borsa İstanbul Dashboard")

# ——— Sidebar’da Bilgilendirme Kutusu ———
with st.sidebar:
    st.header("📌 Panel Hakkında")
    st.markdown("""
    Bu uygulama **Streamlit** kullanılarak geliştirilmiştir.  
    Veriler **yfinance** kütüphanesi aracılığıyla gerçek zamanlı olarak çekilmektedir.

    Teknik göstergeler:
    - **MA20**: 20 günlük hareketli ortalama
    - **RSI**: Göreceli Güç Endeksi (14 günlük)
    
    Göstergeler yatırım kararı vermek için referans niteliğindedir.
    """)

tickers = ["ASELS.IS", "THYAO.IS", "SISE.IS", "KRDMD.IS", "BIMAS.IS", 
    "GARAN.IS", "EREGL.IS", "FROTO.IS", "ISCTR.IS", "YKBNK.IS",
    "AKBNK.IS", "VAKBN.IS", "TOASO.IS", "PETKM.IS", "SAHOL.IS",
    "TCELL.IS", "TTKOM.IS", "KCHOL.IS", "TUPRS.IS", "KOZAA.IS",
    "PGSUS.IS", "TAVHL.IS", "ARCLK.IS", "ALARK.IS", "MGROS.IS",
    "VESTL.IS"]
ticker = st.selectbox("Hisse Seçiniz", tickers)

# Veri çek
df = yf.download(ticker, period="6mo", auto_adjust=True)

# Çok katmanlı sütunları düzleştir
if isinstance(df.columns, pd.MultiIndex):
    df.columns = df.columns.droplevel(1)

# Tablo gösterimi
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
rs = rs.replace([np.inf, -np.inf], np.nan)
df["RSI"] = 100 - (100 / (1 + rs))

# Grafikler
st.subheader("📈 Kapanış ve MA20")
st.line_chart(df[["Close", "MA20"]])

st.subheader("📊 Hacim")
st.bar_chart(df["Volume"])

st.subheader("📉 RSI")
st.line_chart(df["RSI"])



