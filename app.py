import streamlit as st
import pandas as pd
from sqlalchemy import create_engine , text
import plotly.express as px
import os

# Connection setup
# To check locally
#DB_URL = "postgresql://postgres.ssfznbuiwwjgndphvyrn:Supabase%402026@aws-1-ap-south-1.pooler.supabase.com:6543/postgres"

# production use
if "DB_URL" in st.secrets:
    DB_URL = st.secrets["DB_URL"]
else:
    # fallback to local testing
    st.error("❌ No database connection configured. Set DB_URL in secrets.toml or Streamlit Cloud.")
    st.stop()
    
if DB_URL.startswith("postgres://"):
    DB_URL = DB_URL.replace("postgres://", "postgresql://", 1)


engine = create_engine(DB_URL)

st.set_page_config(page_title="Financial Market Warehouse Dashboard",layout="wide")
st.title("📈 Automated Financial Market Warehouse")
st.markdown("This dashboard pulla live data from a **PostgreSQL Warehouse** automated by Github Actions.")

# Sidebar - Select Stock
with engine.connect() as conn:
    tickers = pd.read_sql("select distinct ticker from stock_prices",conn)

selected_ticker = st.sidebar.selectbox("Select a Ticker",tickers['ticker'])

# Query data for the selected stock
query = text(f"Select * from stock_prices where ticker = '{selected_ticker}' Order by date desc")
df = pd.read_sql(query, engine)

# Metrics
col1 , col2, col3 = st.columns(3)
latest_price = df.iloc[0]['close_price']
prev_price = df.iloc[1]['close_price']
delta = ((latest_price  - prev_price)/ prev_price) * 100

col1.metric("Latest Price",f"${latest_price:,.2f}",f"{delta:,.2f}%")
col2.metric("7D volatility", f"{df.iloc[0]['volatility_7d']:.4f}")
col3.metric("Last Updated", df.iloc[0]['date'].strftime("%d-%m-%Y"))

# Visualizations
st.subheader(f"Price Trend : {selected_ticker}")

# create an interactive chart with close price vs moving average
fig = px.line(df, x='date',y=['close_price','moving_avg_7d'],
              title=f"{selected_ticker} Analysis",
              labels={"value":"Price", "variable": "Indicator"})

st.plotly_chart(fig, use_container_width=True)

# Raw Data View
if st.checkbox("Show Raw Data"):
    st.dataframe(df)