from src.data_fetcher import fetch_multiple_tickers
from src.database import insert_stock_data, create_engine_connection
from scripts.init_database import create_connection
from sqlalchemy import create_engine

ticker_list = ["SPY", "QQQ", "AAPL", "MSFT", "GOOGL", "TSLA", "NVDA", "JPM", "JNJ", "XOM", "DIS", "BA", "IWM", "AMZN", "META"]

start = '2020-01-01'
end = '2025-12-26'


data = fetch_multiple_tickers(ticker_list, start, end)
connection = create_connection()
engine = create_engine_connection()


insert_stock_data(engine, data)