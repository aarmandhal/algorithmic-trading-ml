import pandas as pd
import numpy as np

class Backtester:
    # Object-oriented wrapper for backtesting operations
    def __init__(self, initial_capital=100000, transaction_cost=0.001, slippage=0.0005):
        self.initial_capital = initial_capital
        self.transaction_cost = transaction_cost
        self.slippage = slippage
        self.cash = initial_capital
        self.positions = {} # {ticker: quantity}
        self.trades = []
        self.equity_curve = []
    
    def run_backtest(self, signals, prices):
        # signals: Series or DF with index=date, values=signal (1: buy, -1: sell, 0: hold)
        # prices: Series or DF with index=date, values=price
        
        self.cash = self.initial_capital
        self.positions = {}
        self.trades = []
        self.equity_curve = []
        
        dates = signals.index
        
        for date in dates:
            signal = signals.loc[date]
            price = prices.loc[date]
            
            # 1. Execute Signal
            if signal == 1: # Buy
                self.execute_trade(date, 'BUY', price)
            elif signal == -1: # Sell
                self.execute_trade(date, 'SELL', price)
            
            # 2. Record Equity
            total_value = self.calculate_portfolio_value(date, price)
            self.equity_curve.append({'date': date, 'total_value': total_value})
            
        return pd.DataFrame(self.equity_curve).set_index('date')

    def execute_trade(self, date, side, price):
        if side == 'BUY' and self.cash > 0:
            # Simple position sizing: use all cash for one ticker (can be expanded)
            # Adjust price for slippage
            executed_price = price * (1 + self.slippage)
            # Apply transaction cost
            quantity = (self.cash * (1 - self.transaction_cost)) / executed_price
            self.cash = 0
            self.positions['portfolio'] = self.positions.get('portfolio', 0) + quantity
            self.trades.append({'date': date, 'side': 'BUY', 'price': executed_price, 'quantity': quantity})
            
        elif side == 'SELL' and self.positions.get('portfolio', 0) > 0:
            executed_price = price * (1 - self.slippage)
            quantity = self.positions['portfolio']
            # Receive cash minus transaction cost
            self.cash = quantity * executed_price * (1 - self.transaction_cost)
            self.positions['portfolio'] = 0
            self.trades.append({'date': date, 'side': 'SELL', 'price': executed_price, 'quantity': quantity})
    
    def calculate_portfolio_value(self, date, current_price):
        portfolio_value = self.positions.get('portfolio', 0) * current_price
        return self.cash + portfolio_value
    
    def get_performance_metrics(self):
        equity_df = pd.DataFrame(self.equity_curve).set_index('date')
        equity_df['returns'] = equity_df['total_value'].pct_change()
        
        total_return = (equity_df['total_value'].iloc[-1] / self.initial_capital) - 1
        sharpe_ratio = (equity_df['returns'].mean() / equity_df['returns'].std()) * np.sqrt(252) if len(equity_df) > 1 and equity_df['returns'].std() != 0 else 0
        
        # Max Drawdown
        equity_df['cum_max'] = equity_df['total_value'].cummax()
        equity_df['drawdown'] = (equity_df['total_value'] / equity_df['cum_max']) - 1
        max_drawdown = equity_df['drawdown'].min()
        
        # Win Rate and Profit Factor (assuming paired trades)
        profits = []
        for i in range(1, len(self.trades), 2):
            buy = self.trades[i-1]
            sell = self.trades[i]
            if buy['side'] == 'BUY' and sell['side'] == 'SELL':
                profit = (sell['price'] * sell['quantity']) - (buy['price'] * buy['quantity'])
                profits.append(profit)
        
        win_rate = sum(1 for p in profits if p > 0) / len(profits) if profits else 0
        
        gross_profits = sum(p for p in profits if p > 0)
        gross_losses = abs(sum(p for p in profits if p < 0))
        profit_factor = gross_profits / gross_losses if gross_losses > 0 else (gross_profits if gross_profits > 0 else 0)

        return {
            'total_return': total_return,
            'sharpe_ratio': sharpe_ratio,
            'max_drawdown': max_drawdown,
            'win_rate': win_rate,
            'profit_factor': profit_factor,
            'trades_count': len(self.trades)
        }
