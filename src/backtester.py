


class Backtester:
    def __init__(self, initial_capital, transaction_cost):
        self.capital = initial_capital
        self.positions = {}
        self.trades = []
        
    def run_backtest(self, signals, prices):
        # For each day:
        #   - Get prediction
        #   - Execute trades
        #   - Update portfolio
        #   - Track cash and holdings
        pass
        
    def calculate_metrics(self):
        # Returns, Sharpe ratio, max drawdown
        # Win rate, avg win/loss
        pass
    
    def plot_results(self):
        # Equity curve
        # Drawdown chart
        # Trade distribution
        pass