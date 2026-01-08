import os
import datetime as dt
import pandas as pd
import yfinance as yf
from sqlalchemy import create_engine, text

# --- 1. SETTINGS & CONNECTION ---
TICKERS = ['CBA.AX', 'NAB.AX', 'WBC.AX', 'ANZ.AX']

def get_engine():
    # Priority 1: GitHub Secret / Environment Variable (For Cloud)
    # Priority 2: Docker Localhost (For your PC)
    conn_url = os.getenv('DB_URL')
    if not conn_url:
        conn_url = 'postgresql+psycopg2://myuser:mypassword@localhost:5432/market_data'
    return create_engine(conn_url)

# --- 2. EXTRACT & TRANSFORM (From your Notebook) ---
def fetch_and_process():
    end = dt.datetime.now()
    start = end - dt.timedelta(days=100)
    df_raw = yf.download(TICKERS, start=start, end=end)
    
    close_prices = df_raw['Close']
    processed_list = []

    for stock in close_prices.columns:
        temp_df = close_prices[[stock]].copy()
        temp_df.columns = ['close_price']
        temp_df['ticker'] = stock
        temp_df['moving_avg_7d'] = temp_df['close_price'].rolling(window=7).mean()
        temp_df['daily_return'] = temp_df['close_price'].pct_change()
        temp_df['volatility_7d'] = temp_df['daily_return'].rolling(window=7).std()
        temp_df['extracted_at'] = dt.datetime.now()
        processed_list.append(temp_df)

    final_df = pd.concat(processed_list).dropna()
    return final_df

# --- 3. LOAD & UPSERT (Professional Logic) ---
def load_to_postgres(df, engine):
    # Step A: Ensure Table Exists
    with engine.connect() as conn:
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS stock_prices (
                date TIMESTAMP,
                ticker TEXT,
                close_price DECIMAL,
                moving_avg_7d DECIMAL,
                daily_return DECIMAL,
                volatility_7d DECIMAL,
                extracted_at TIMESTAMP,
                PRIMARY KEY (date, ticker)
            );
        """))
        conn.commit()

    # Step B: Upsert via Staging Table
    df.to_sql('temp_staging', engine, if_exists='replace', index=True)
    
    upsert_query = text("""
        INSERT INTO stock_prices (date, ticker, close_price, moving_avg_7d, daily_return, volatility_7d, extracted_at)
        SELECT "Date", ticker, close_price, moving_avg_7d, daily_return, volatility_7d, extracted_at
        FROM temp_staging
        ON CONFLICT (date, ticker) DO UPDATE SET 
            close_price = EXCLUDED.close_price,
            moving_avg_7d = EXCLUDED.moving_avg_7d,
            daily_return = EXCLUDED.daily_return,
            volatility_7d = EXCLUDED.volatility_7d,
            extracted_at = EXCLUDED.extracted_at;
    """)

    with engine.connect() as conn:
        conn.execute(upsert_query)
        conn.execute(text("DROP TABLE temp_staging;"))
        conn.commit()

# --- 4. MAIN EXECUTION ---
if __name__ == "__main__":
    print("Starting ETL Process...")
    db_engine = get_engine()
    data = fetch_and_process()
    load_to_postgres(data, db_engine)
    print("ETL Process Completed Successfully!")