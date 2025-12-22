import psycopg2
from src.config import get_database_config


def create_connection():
    # Create connection pool to the database
    db_config = get_database_config()
    conn = psycopg2.connect(
        dbname=db_config["name"],
        user=db_config["user"],
        password=db_config["password"],
        host=db_config["host"],
        port=db_config["port"]
    )
    return conn

def create_tables():
    # Create necessary tables in the database
    conn = create_connection()
    cur = conn.cursor()
    # Create stocks table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS stocks (
        id serial PRIMARY KEY,
        ticker varchar(10) NOT NULL,
        date date NOT NULL,
        open float,
        low float,
        high float,
        close float,
        adjusted_close float,
        volume bigint,
        created_at timestamp DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(ticker, date)
    ) 
    """)
    # Create features table
    cur.execute("""CREATE TABLE IF NOT EXISTS features (
        id serial PRIMARY KEY,
        ticker varchar(10) NOT NULL,
        date date NOT NULL,
        sma_5 float,
        sma_20 float,
        sma_50 float,
        rsi_14 float,
        macd float,
        macd_signal float,
        macd_histogram float,
        bb_upper float,
        bb_middle float,
        bb_lower float,
        atr_14 float,
        obv bigint,
        volatility_20 float,
        return_1d float,
        return_5d float,
        return_20d float,
        created_at timestamp DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(ticker, date) 
    )
    """)
    # Create model_predictions table
    cur.execute("""CREATE TABLE IF NOT EXISTS model_predictions (
        id serial PRIMARY KEY,
        ticker varchar(10) NOT NULL,
        date date NOT NULL,
        model_name varchar(50),
        model_version varchar(20),
        signal float,
        confidence float,
        probability_buy float,
        probability_sell float,
        probability_hold float,
        actual_return float,
        correct_prediction boolean,
        created_at timestamp DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(ticker, date)
    )
    """)
    # Create backtest_runs table
    cur.execute("""CREATE TABLE IF NOT EXISTS backtest_runs (
        id serial Primary KEY,
        name varchar(100) NOT NULL,
        model_name varchar(50),
        start_date date,
        end_date date,
        initial_capital float,
        transaction_cost float,
        slippage float,
        total_return float,
        annualized_return float,
        sharpe_ratio float,
        sortino_ratio float,
        max_drawdown float,
        win_rate float,
        total_trades int,
        avg_win float,
        avg_loss float,
        profit_factor float,
        benchmark_return float,
        created_at timestamp DEFAULT CURRENT_TIMESTAMP
    ) 
    """)
    # Create trades table
    cur.execute("""CREATE TABLE IF NOT EXISTS trades (
        id serial Primary KEY,
        backtest_run_id int REFERENCES backtest_runs(id),
        ticker varchar(10) NOT NULL,
        date date NOT NULL,
        side varchar(4),
        quantity int,
        price float,
        fees float,
        signal float,
        transaction_cost float,
        slippage float,
        portfolio_value_before float,
        portfolio_value_after float,
        cash_before float,
        cash_after float,
        profit_loss float,
        holding_period int,
        created_at timestamp DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(ticker, date)
    )
    """)
    # Create portfolio_snapshots table
    cur.execute("""CREATE TABLE IF NOT EXISTS portfolio_snapshots (
        id serial PRIMARY KEY,
        backtest_run_id int REFERENCES backtest_runs(id),
        date date NOT NULL,
        cash float,
        positions_value float,
        total_value float,
        daily_return float,
        cumulative_return float,
        drawdown float,
        created_at timestamp DEFAULT CURRENT_TIMESTAMP
    )
    """)
    # Create positions table
    cur.execute("""CREATE TABLE IF NOT EXISTS positions (
        id serial PRIMARY KEY,
        backtest_run_id int REFERENCES backtest_runs(id),
        ticker varchar(10) NOT NULL,
        date date NOT NULL,
        quantity int,
        entry_price float,
        entry_date date,
        current_price float,
        current_value float,
        unrealized_pnl float,
        created_at timestamp DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(ticker, date)
    )
    """)
    # Commit changes and close connection
    conn.commit()
    cur.close()
    conn.close()
    
def create_indexes():
    # Create indexes to optimize database queries
    pass

create_tables()