

import pandas as pd
import numpy as np
from ta.trend import SMAIndicator, EMAIndicator, MACD
from ta.momentum import RSIIndicator, StochasticOscillator
from ta.volatility import BollingerBands, AverageTrueRange
from ta.volume import OnBalanceVolumeIndicator

# === TREND INDICATORS ===
# Functions that measure trend direction and strength

def calculate_moving_average(df, windows=[5, 10, 20, 50, 200]):
    # Calculate simple moving averages
    for window in windows:
        df[f'sma_{window}'] = SMAIndicator(close=df['close'], window=window).sma_indicator()
    return df

def calculate_exponential_moving_average(df, span=20):
    # Calculate EMA
    df[f'ema_{span}'] = EMAIndicator(close=df['close'], window=span).ema_indicator()
    return df

def calculate_macd(df, short_span=12, long_span=26, signal_span=9):
    # Calculate MACD
    macd = MACD(close=df['close'], window_slow=long_span, window_fast=short_span, window_sign=signal_span)
    df['macd'] = macd.macd()
    df['macd_signal'] = macd.macd_signal()
    df['macd_diff'] = macd.macd_diff()
    return df

# === MOMENTUM INDICATORS ===
# Functions that measure speed of price changes

def calculate_rsi(df, period=14):
    # Calculate Relative Strength Index
    df[f'rsi_{period}'] = RSIIndicator(close=df['close'], window=period).rsi()
    return df

def calculate_stochastic(df, period=14):
    # Calculate Stochastic Oscillator
    stoch = StochasticOscillator(high=df['high'], low=df['low'], close=df['close'], window=period, smooth_window=3)
    df['stoch_k'] = stoch.stoch()
    df['stoch_d'] = stoch.stoch_signal()
    return df

# === VOLATILITY INDICATORS ===
# Functions that measure price variability

def calculate_bollinger_bands(df, window=20, num_std=2):
    # Calculate Bollinger Bands
    indicator_bb = BollingerBands(close=df['close'], window=window, window_dev=num_std)
    df['bb_hband'] = indicator_bb.bollinger_hband()
    df['bb_lband'] = indicator_bb.bollinger_lband()
    df['bb_mavg'] = indicator_bb.bollinger_mavg()
    return df

def calculate_atr(df, period=14):
    # Calculate Average True Range
    df['atr'] = AverageTrueRange(high=df['high'], low=df['low'], close=df['close'], window=period).average_true_range()
    return df

# === VOLUME INDICATORS ===
# Functions that incorporate volume data

def calculate_obv(df):
    # Calculate On-Balance Volume
    df['obv'] = OnBalanceVolumeIndicator(close=df['close'], volume=df['volume']).on_balance_volume()
    return df

# === HELPER FUNCTIONS ===
# Supporting calculations used by multiple indicators

def calculate_returns(df, periods=[1, 3, 5, 10, 20]):
    # Calculate returns over different periods
    for p in periods:
        df[f'return_{p}d'] = df['close'].pct_change(p)
    return df

def calculate_log_returns(df):
    # Calculate log returns
    df['log_return'] = np.log(df['close'] / df['close'].shift(1))
    return df

def create_lag_features(df, features, lags=[1, 2, 3, 5]):
    # Create lagged features for a list of features
    for feature in features:
        for lag in lags:
            df[f'{feature}_lag_{lag}'] = df[feature].shift(lag)
    return df

class FeatureEngine:
    # Object-oriented wrapper for feature engineering operations
    def __init__(self):
        pass
    
    def add_all_indicators(self, df):
        # Apply all indicator functions to the dataframe
        df = df.copy()
        df = calculate_moving_average(df)
        df = calculate_exponential_moving_average(df)
        df = calculate_macd(df)
        df = calculate_rsi(df)
        df = calculate_stochastic(df)
        df = calculate_bollinger_bands(df)
        df = calculate_atr(df)
        df = calculate_obv(df)
        df = calculate_returns(df)
        df = calculate_log_returns(df)
        
        # Drop NaN values created by indicators
        df = df.dropna()
        return df

    def transform(self, df):
        # Main transformation pipeline
        return self.add_all_indicators(df)