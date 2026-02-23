from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from datetime import date

class TickerInfo(BaseModel):
    ticker: str

class TradeRecord(BaseModel):
    date: str
    side: str
    price: float
    quantity: float

class PerformanceMetrics(BaseModel):
    total_return: float
    sharpe_ratio: float
    max_drawdown: float
    win_rate: float
    profit_factor: float
    trades_count: int

class BacktestResponse(BaseModel):
    ticker: str
    metrics: PerformanceMetrics
    equity_curve: List[Dict[str, Any]]
    trades: List[TradeRecord]

class StockDataPoint(BaseModel):
    date: date
    open: Optional[float]
    high: Optional[float]
    low: Optional[float]
    close: Optional[float]
    volume: Optional[int]

class StockDataResponse(BaseModel):
    ticker: str
    data: List[StockDataPoint]
