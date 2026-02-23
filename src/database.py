import psycopg2
from src.config import get_database_config
from scripts.init_database import create_connection
from sqlalchemy import create_engine, text, types
import pandas as pd


def create_engine_connection():
    db_config = get_database_config()
    connection = db_config['database_url']
    engine = create_engine(connection)
    return engine

def insert_stock_data(engine, df):
    if df.empty:
        print("Dataframe is empty")
        return 0
    
    insert_query = text("""
        INSERT INTO stocks (ticker, date, open, high, low, close, adjusted_close, volume)
        SELECT t.ticker, t.date, t.open, t.high, t.low, t.close, t.adjusted_close, t.volume
        FROM temp_table AS t
        ON CONFLICT (ticker, date) DO NOTHING;
    """)

    with engine.begin() as conn:
        df.to_sql( "temp_table", conn, if_exists="replace", index=False,   
        dtype={
            "ticker": types.String,
            "date": types.Date,
            "open": types.Float,
            "high": types.Float,
            "low": types.Float,
            "close": types.Float,
            "adjusted_close": types.Float,
            "volume": types.BigInteger,
        }
    )

        conn.execute(insert_query)
        conn.execute(text("DROP TABLE IF EXISTS temp_table"))

    print(f"Attempted insert of {len(df)} rows")
    return len(df)

def query_stock_data(engine, ticker, start_date, end_date):
    # Query stock data for a given ticker and date range
    query = """
        SELECT ticker, date, open, low, high, close, adjusted_close, volume 
        FROM stocks 
        WHERE ticker = %(ticker)s 
        AND date BETWEEN %(start)s AND %(end)s
    """
    params = {'ticker': ticker, "start": start_date, 'end': end_date}
    results = pd.read_sql(sql=query, con=engine, params=params)
    return results
    

def query_latest_date(conn, ticker):
    # Query the latest date for which data is available for a ticker
    cur = conn.cursor()
    query = """
        SELECT date
        FROM stocks
        WHERE ticker = %s
        ORDER BY date
        DESC 
        LIMIT 1
    """
    try:
        cur.execute(query, (ticker, ))
        date = cur.fetchone()
        
        if date:
            return date[0]
        else:
            return None
    finally:
        conn.commit()
        cur.close()
        conn.close()

def get_all_tickers(engine):
    query = """
        SELECT DISTINCT ticker
        FROM stocks
        ORDER BY ticker
    """
    df = pd.read_sql(query, engine)
    return df['ticker'].tolist()

def get_date_range(conn, ticker):
    cur = conn.cursor()
    query = """
        SELECT MIN(date) as start_date, MAX (date) as end_date
        FROM stocks
        WHERE ticker = %s
    """
    try:
        cur.execute(query, (ticker, ))
        results = cur.fetchone()
        
        if results:
            return results[0], results[1]
        else:
            return None, None
    finally:
        conn.commit()
        cur.close()
        conn.close()
        
def delete_ticker_data(conn, ticker):
    cur = conn.cursor()
    query = """
        DELETE FROM stocks
        WHERE ticker = %s
    """
    try:
        cur.execute(query, (ticker, ))
        deleted = cur.rowcount
        conn.commit()
        print(f"Deleted {deleted} rows from database for ticker symbol {ticker}")
        return deleted
    except Exception as e:
        conn.rollback()
        print(f"Error in deletion, Error: {e}")
        return 0
    finally:
        cur.close()
        conn.close()   

def execute_vacuum(conn):
    # Perform database vacuuming to optimize performance
    pass

def create_partition_by_date(conn, table_name, start_date, end_date):
    # Create partitioned tables by date ranges
    pass

def setup_continuous_aggregation(conn, view_name, source_table):
    # Setup continuous aggregation views for faster queries
    pass

def check_table_exists(conn, table_name, schemema='public'):
    # Check if a table exists in the database
    pass

def get_table_size(conn, table_name):
    # Get size of a table in the database
    pass

def backup_database(conn, backup_path):
    # Backup the database to a specified path
    pass

def create_user_permissions(conn, user, password, permissions):
    # Create user permissions for database access
    pass

def enable_row_level_security(conn, table_name):
    # Enable row-level security on a table
    pass

class DatabaseManager:
    # Object-oriented wrapper for database operations
    def __init__(self):
        # Initialize connection parameters from config
        self.config = get_database_config()
        self.engine = create_engine(self.config['database_url'])
        self._connection = None

    def get_connection(self):
        # Get a database connection
        if self._connection is None or self._connection.closed:
            self._connection = psycopg2.connect(
                dbname=self.config["name"],
                user=self.config["user"],
                password=self.config["password"],
                host=self.config["host"],
                port=self.config["port"]
            )
        return self._connection
    
    def release_connection(self):
        # Close the connection
        if self._connection and not self._connection.closed:
            self._connection.close()
            self._connection = None
    
    def insert_data(self, table_name, df, method='append'):
        # Insert data method using SQLAlchemy
        if df.empty:
            return 0
        try:
            df.to_sql(table_name, self.engine, if_exists=method, index=False)
            return len(df)
        except Exception as e:
            print(f"Error inserting data into {table_name}: {e}")
            return 0
    
    def query_data(self, query, params=None):
        # Query data method using pandas and SQLAlchemy
        try:
            return pd.read_sql(query, self.engine, params=params)
        except Exception as e:
            print(f"Error querying data: {e}")
            return pd.DataFrame()

    def execute_raw_sql(self, sql, params=None):
        # Execute raw SQL command
        conn = self.get_connection()
        cur = conn.cursor()
        try:
            cur.execute(sql, params)
            conn.commit()
            return cur.rowcount
        except Exception as e:
            conn.rollback()
            print(f"Error executing raw SQL: {e}")
            return 0
        finally:
            cur.close()
    
class TimeSeriesDB:
    # Specialized class for time-series data operations
    def __init__(self, connection_params):
        # Initialize with connection parameters
        pass
    
    def create_hypertable(self, table_name, time_column='date'):
        # Create a hypertable for time-series data
        pass
    
    def add_retention_policy(self, table_name, duration):
        # Add retention policy to a hypertable
        pass
    
    def create_continuous_aggregate(self, view_name, query, refresh_interval):
        # Create continuous aggregate view
        pass
        
    def compress_chunks(self, table_name, older_than):
        # Compress chunks older than a certain time
        pass
    

def load_database_config_from_env():
    # Load database configuration from a env
    pass

def create_connection_string(host, port, database, user, password):
    # Create a connection string for the database
    pass

def test_connection(host, port, database, user, password):
    # Test database connection
    pass