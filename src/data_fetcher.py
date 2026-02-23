import yfinance as yf
import pandas as pd


def fetch_stock_data(ticker, start_date, end_date):
    # Use yfinance
    # Return OHLCV dataframe
    try:
        data = yf.download(ticker, start=start_date, end=end_date, auto_adjust=False, progress=False,  multi_level_index=False)    
        data = data.reset_index()
        data.rename(columns={"Open": "open", "Low": "low", "High": "high", "Close": "close", "Adj Close": "adjusted_close", "Volume": "volume", "Date": "date"}, inplace=True)
        data.insert(0, "ticker", ticker)
        return data
    except Exception as e:
        print(f"Error fetching stock data, Error: {e}")
        return pd.DataFrame()

def fetch_multiple_tickers(ticker_list, start_date, end_date):
    # Fetch data for multiple tickers and concatenate
    # Dataframe with data from all tickers
    dfs = []
    for ticker in ticker_list:
        data = fetch_stock_data(ticker, start_date, end_date)
        dfs.append(data)  
    data = pd.concat(dfs, ignore_index=True)
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

def handle_missing_data(df, strategy='ffill'):
    # Forward-fill, back-fill, or drop
    if strategy == 'ffill':
        return df.ffill()
    elif strategy == 'bfill':
        return df.bfill()
    elif strategy == 'dropna':
        return df.dropna()
    return df

def resample_data(df, interval='W'):
    # Resample to different timeframes (e.g., weekly, monthly)
    df = df.copy()
    df['date'] = pd.to_datetime(df['date'])
    df.set_index('date', inplace=True)
    
    resampled = df.resample(interval).agg({
        'ticker': 'first',
        'open': 'first',
        'high': 'max',
        'low': 'min',
        'close': 'last',
        'adjusted_close': 'last',
        'volume': 'sum'
    }).dropna()
    
    return resampled.reset_index()

def check_data_quality(df):
    # Check for missing values, anomalies
    issues = []
    if df.isnull().values.any():
        issues.append("Missing values detected")
    
    # Check for negative prices
    if (df[['open', 'high', 'low', 'close']] < 0).any().any():
        issues.append("Negative prices detected")
        
    return issues

class DataFetcher:
    # Object-oriented wrapper for data fetching operations
    def __init__(self):
        # Initialize
        pass
    
    def fetch_data(self, ticker, start_date, end_date):
        # Fetch data method
        return fetch_stock_data(ticker, start_date, end_date)
    
    def update_data(self, ticker, last_date):
        # Update existing data to new end date
        import datetime
        today = datetime.date.today().strftime('%Y-%m-%d')
        return self.fetch_data(ticker, last_date, today)

    def validate_date_range(self, start_date, end_date):
        # Validate date range
        try:
            pd.to_datetime(start_date)
            pd.to_datetime(end_date)
            return True
        except ValueError:
            return False