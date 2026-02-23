import pandas as pd
from src.data_fetcher import fetch_stock_data
from src.database import insert_stock_data, create_engine_connection
import time

def main():
    ticker_list = ["SPY", "QQQ", "AAPL", "MSFT", "GOOGL", "TSLA", "NVDA", "JPM", "JNJ", "XOM", "DIS", "BA", "IWM", "AMZN", "META"]
    start_date = '2020-01-01'
    end_date = '2025-12-26'
    
    engine = create_engine_connection()
    
    print(f"Starting bulk download for {len(ticker_list)} tickers...")
    
    for i, ticker in enumerate(ticker_list):
        print(f"[{i+1}/{len(ticker_list)}] Fetching {ticker}...")
        try:
            data = fetch_stock_data(ticker, start_date, end_date)
            if not data.empty:
                # Ensure date is sorted
                data = data.sort_values('date')
                rows = insert_stock_data(engine, data)
                print(f"Successfully inserted {rows} rows for {ticker}")
            else:
                print(f"No data found for {ticker}")
            
            # Simple rate limiting anti-block
            time.sleep(0.5)
            
        except Exception as e:
            print(f"Failed to process {ticker}: {e}")
            continue

    print("Bulk download process completed.")

if __name__ == "__main__":
    main()