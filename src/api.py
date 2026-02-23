from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from typing import List

from src.database import create_engine_connection, query_stock_data, get_all_tickers
from src.features import FeatureEngine
from src.preprocessor import TimeSeriesPreprocessor
from src.model import TradingModel
from src.backtester import Backtester
from src.schemas import TickerInfo, BacktestResponse, StockDataResponse, PerformanceMetrics

app = FastAPI(title="Algo Trading ML API")

# Enable CORS for frontend development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify the frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

engine = create_engine_connection()

@app.get("/")
def read_root():
    return {"status": "healthy", "service": "Algo Trading ML API"}

@app.get("/tickers", response_model=List[str])
def get_tickers():
    try:
        tickers = get_all_tickers(engine)
        return tickers
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/backtest/{ticker}", response_model=BacktestResponse)
def run_backtest(ticker: str, initial_capital: float = 100000.0, transaction_cost: float = 0.001):
    try:
        # 1. Fetch Data
        df = query_stock_data(engine, ticker, '2020-01-01', '2025-12-26')
        if df.empty:
            raise HTTPException(status_code=404, detail=f"No data found for ticker {ticker}")
        
        # Ensure date is the index and sorted
        df['date'] = pd.to_datetime(df['date'])
        df = df.sort_values('date').set_index('date')

        # 2. Feature Engineering
        fe = FeatureEngine()
        df_features = fe.transform(df)
        
        # 3. Model Logic (Simplified for the API demo, matches dashboard logic)
        feature_list = ['rsi_14', 'macd', 'atr', 'obv']
        preprocessor = TimeSeriesPreprocessor()
        X_train_scaled, X_test_scaled, y_train, y_test = preprocessor.prepare_data(df_features, feature_list)
        
        model = TradingModel()
        model.train(X_train_scaled, y_train)
        
        # Predict on full set
        X_full = df_features[feature_list]
        X_full_scaled = preprocessor.scaler.transform(X_full)
        signals = model.predict(X_full_scaled)
        signals_series = pd.Series(signals, index=df_features.index)
        
        # 4. Run Backtest
        backtester = Backtester(initial_capital, transaction_cost)
        equity_curve_df = backtester.run_backtest(signals_series, df_features['close'])
        metrics_dict = backtester.get_performance_metrics()
        
        # 5. Format Response
        equity_curve = []
        for d, row in equity_curve_df.iterrows():
            equity_curve.append({"date": d.strftime('%Y-%m-%d'), "total_value": row["total_value"]})
            
        trades = []
        for t in backtester.trades:
            equity_curve_date = t["date"]
            if hasattr(equity_curve_date, 'strftime'):
                formatted_date = equity_curve_date.strftime('%Y-%m-%d')
            else:
                formatted_date = str(equity_curve_date)

            trades.append({
                "date": formatted_date,
                "side": t["side"],
                "price": float(t["price"]),
                "quantity": float(t["quantity"])
            })

        return {
            "ticker": ticker,
            "metrics": metrics_dict,
            "equity_curve": equity_curve,
            "trades": trades
        }
    except Exception as e:
        import traceback
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/data/{ticker}", response_model=StockDataResponse)
def get_stock_data(ticker: str):
    try:
        df = query_stock_data(engine, ticker, '2020-01-01', '2025-12-26')
        if df.empty:
            raise HTTPException(status_code=404, detail=f"No data found for ticker {ticker}")
        
        # Convert to list of dicts for schema validation
        data_list = df.to_dict(orient="records")
        return {"ticker": ticker, "data": data_list}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
