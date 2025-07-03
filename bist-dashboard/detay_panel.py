import streamlit as st
import yfinance as yf

def detay_paneli(symbol):
    st.header(f"📊 {symbol} Hisse Detayları")

    try:
        data = yf.Ticker(symbol)
        info = data.info
        hist = data.history(period="1d")

        st.subheader("📋 Günlük Özet")
        col1, col2, col3 = st.columns(3)
        col1.metric("Açılış", f"{hist['Open'][0]:.2f}")
        col2.metric("Yüksek", f"{hist['High'][0]:.2f}")
        col3.metric("Düşük", f"{hist['Low'][0]:.2f}")

        col4, col5 = st.columns(2)
        col4.metric("Kapanış", f"{hist['Close'][0]:.2f}")
        col5.metric("Hacim", f"{hist['Volume'][0]:,.0f}")

        st.divider()

        st.subheader("📊 Temel Finansal Oranlar")
        col6, col7, col8 = st.columns(3)
        col6.metric("F/K", info.get("trailingPE", "N/A"))
        col7.metric("PD/DD", info.get("priceToBook", "N/A"))
        col8.metric("Piyasa Değeri", f"{info.get('marketCap', 'N/A'):,}")

        col9, col10 = st.columns(2)
        col9.metric("EPS", info.get("trailingEps", "N/A"))
        col10.metric("Beta", info.get("beta", "N/A"))

        st.divider()

        st.subheader("📥 Ham Veriyi İndir")
        csv = hist.to_csv().encode('utf-8')
        st.download_button(
            label="Veriyi CSV olarak indir",
            data=csv,
            file_name=f"{symbol}_veri.csv",
            mime='text/csv'
        )

    except Exception as e:
        st.error(f"Bir hata oluştu: {e}")

