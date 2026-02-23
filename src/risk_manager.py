import numpy as np
import pandas as pd

def calculate_value_at_risk(returns, confidence_level=0.95):
    # Calculate Value at Risk (VaR) using historical method
    if len(returns) == 0:
        return 0
    return -np.percentile(returns, (1 - confidence_level) * 100)

def calculate_conditional_value_at_risk(returns, confidence_level=0.95):
    # Calculate CVaR
    var = calculate_value_at_risk(returns, confidence_level)
    tail_losses = returns[returns <= -var]
    return -tail_losses.mean() if len(tail_losses) > 0 else var

def set_stop_loss(entry_price, stop_loss_pct):
    # Calculate stop-loss price
    return entry_price * (1 - stop_loss_pct)

def set_take_profit(entry_price, take_profit_pct):
    # Calculate take-profit price
    return entry_price * (1 + take_profit_pct)

class RiskManager:
    # Object-oriented wrapper for risk management operations
    def __init__(self, max_position_size=0.1, max_portfolio_risk=0.02):
        self.max_position_size = max_position_size # fraction of portfolio
        self.max_portfolio_risk = max_portfolio_risk # VaR limit
    
    def check_position_limit(self, current_capital, price):
        # Return recommended shares based on max position size
        return (current_capital * self.max_position_size) / price

    def get_risk_metrics(self, returns):
        # Return various risk metrics
        return {
            'VaR_95': calculate_value_at_risk(returns, 0.95),
            'CVaR_95': calculate_conditional_value_at_risk(returns, 0.95),
            'volatility': returns.std() * np.sqrt(252)
        }