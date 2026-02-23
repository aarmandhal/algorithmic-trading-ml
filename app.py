import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from src.database import create_engine_connection, query_stock_data
from src.features import FeatureEngine
from src.preprocessor import TimeSeriesPreprocessor
from src.model import TradingModel
from src.backtester import Backtester

st.set_page_config(page_title="Algo Trading ML Dashboard", layout="wide")

st.title("Algorithmic Trading ML Dashboard")

# Sidebar for configuration
st.sidebar.header("Configuration")
ticker = st.sidebar.selectbox("Select Ticker", ["AAPL", "MSFT", "SPY", "QQQ", "TSLA"])
initial_capital = st.sidebar.number_input("Initial Capital", value=100000)
transaction_cost = st.sidebar.slider("Transaction Cost", 0.0, 0.01, 0.001, format="%.3f")

# Load Data
engine = create_engine_connection()
df = query_stock_data(engine, ticker, '2020-01-01', '2025-12-26')

if not df.empty:
    st.subheader(f"Strategy Performance for {ticker}")
    
    # 1. Feature Engineering
    fe = FeatureEngine()
    df_features = fe.transform(df)
    
    # 2. Preprocessing & Model (Simplification for demo)
    feature_list = ['rsi_14', 'macd', 'atr', 'obv']
    preprocessor = TimeSeriesPreprocessor()
    X_train_scaled, X_test_scaled, y_train, y_test = preprocessor.prepare_data(df_features, feature_list)
    
    model = TradingModel()
    model.train(X_train_scaled, y_train)
    
    # 3. Backtesting
    # Generate signals on full dataset for visualization
    X_full = df_features[feature_list]
    # Scaling full set for prediction (simplified)
    # In practice, use transform only
    X_full_scaled = preprocessor.scaler.transform(X_full)
    signals = model.predict(X_full_scaled)
    signals_series = pd.Series(signals, index=df_features.index)
    
    backtester = Backtester(initial_capital, transaction_cost)
    equity_curve = backtester.run_backtest(signals_series, df_features['close'])
    metrics = backtester.get_performance_metrics()
    
    # Display Metrics
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Return", f"{metrics['total_return']:.2%}")
    col2.metric("Sharpe Ratio", f"{metrics['sharpe_ratio']:.2f}")
    col3.metric("Max Drawdown", f"{metrics['max_drawdown']:.2%}")
    col4.metric("Trades", metrics['trades_count'])
    
    # Plot Equity Curve
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=equity_curve.index, y=equity_curve['total_value'], mode='lines', name='Strategy Equity'))
    fig.update_layout(title="Equity Curve", xaxis_title="Date", yaxis_title="Portfolio Value")
    st.plotly_chart(fig, use_container_width=True)
    
    st.dataframe(df.tail(10))
else:
    st.warning("No data found in database. Please run the data download script first.")
