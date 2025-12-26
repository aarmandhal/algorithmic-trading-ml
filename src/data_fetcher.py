import yfinance as yf
import pandas as pd


def fetch_stock_data(ticker, start_date, end_date):
    # Use yfinance
    # Return OHLCV dataframe
    try:
        data = yf.download(ticker, start=start_date, end=end_date)
        
        if data.isempty:
            print(f"No data found for ticker: {ticker}")
            return pd.DataFrame()
        
        data = data.reset_index()
        data.rename(columns={"Open": "open", "Low": "low", "High": "high", "Close": "close", "Adj Close": "adjusted_close", "Volume": "volume", "Date": "date"})
        data.insert(0, "ticker", ticker)
        return data
    except Exception as e:
        print(f"Error fetching stock data, Error: {e}")
        return pd.DataFrame()

def fetch_multiple_tickers(ticker_list, start_date, end_date):
    # Fetch data for multiple tickers and concatenate
    # Dataframe with data from all tickers
    dfs = []
    invalid_tickers = []
    for ticker in ticker_list:
        valid_ticker = validate_ticker(ticker)
        if valid_ticker:
            data = fetch_stock_data(ticker, start_date, end_date)
            dfs.append(data)
        else:
            invalid_tickers.append(ticker)    
    data = pd.concat(dfs, ignore_index=True)
    print(f"Failed fetching data for the following ticker(s): {', '.join(invalid_tickers)}")
    return data

def validate_ticker(ticker):
    # Check if ticker is valid using yfinance
    try:
        info = yf.Ticker(ticker).info
        if not info:
            return False
        else:
            return True

    except Exception:
        return False

def handle_missing_data(df):
    # Forward-fill, back-fill, or drop
    pass

def resample_data(df, interval):
    # Resample to different timeframes (e.g., weekly, monthly)
    pass

def get_latest_price(ticker):
    # Fetch latest price for given ticker
    pass

def download_bulk_historical_data(ticker_list, start_date, end_date):
    # Download and save bulk historical data for multiple tickers
    pass

def check_data_quality(df):
    # Check for missing values, anomalies
    pass

class DataFetcher:
    # Object-oriented wrapper for data fetching operations
    def __init__(self, api_key='yfinance'):
        # Initialize with API key or service
        pass
    
    def fetch_data(self, ticker, start_date, end_date):
        # Fetch data method
        pass
    
    def update_data(self, ticker, last_date):
        # Update existing data to new end date
        pass
    
    def get_available_tickers(self):
        # Return list of available tickers from a source
        pass
    
    def validate_date_range(self, start_date, end_date):
        # Validate date range
        pass