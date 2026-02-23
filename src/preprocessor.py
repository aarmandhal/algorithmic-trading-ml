import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler

def create_target_variable(df, horizon=1):
    # Create target variable: 1 if price in 'horizon' days > current price, else 0
    # Predict direction of next day's close
    df['target'] = (df['close'].shift(-horizon) > df['close']).astype(int)
    # Drop the last 'horizon' rows as they won't have a target
    return df.dropna()

def split_time_series_data(df, train_ratio=0.8):
    # Split data into train and test sets without shuffling (preserving time order)
    split_idx = int(len(df) * train_ratio)
    train_df = df.iloc[:split_idx]
    test_df = df.iloc[split_idx:]
    return train_df, test_df

def scale_features(X_train, X_test):
    # Scale features using StandardScaler, fitting ONLY on training data
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    return X_train_scaled, X_test_scaled, scaler

class TimeSeriesPreprocessor:
    # Object-oriented wrapper for preprocessing operations
    def __init__(self, train_ratio=0.8):
        self.train_ratio = train_ratio
        self.scaler = None
        self.features = None
    
    def prepare_data(self, df, feature_list):
        # Full pipeline: target creation, feature selection, splitting, scaling
        self.features = feature_list
        
        # 1. Create target
        df = create_target_variable(df)
        
        # 2. Extract X and y
        X = df[self.features]
        y = df['target']
        
        # 3. Split
        split_idx = int(len(df) * self.train_ratio)
        X_train, X_test = X.iloc[:split_idx], X.iloc[split_idx:]
        y_train, y_test = y.iloc[:split_idx], y.iloc[split_idx:]
        
        # 4. Scale
        X_train_scaled, X_test_scaled, self.scaler = scale_features(X_train, X_test)
        
        return X_train_scaled, X_test_scaled, y_train, y_test
