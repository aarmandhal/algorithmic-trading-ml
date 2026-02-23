import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

def train_random_forest(X_train, y_train, n_estimators=100, max_depth=None):
    # Train Random Forest model
    model = RandomForestClassifier(n_estimators=n_estimators, max_depth=max_depth, random_state=42)
    model.fit(X_train, y_train)
    return model

def evaluate_model(model, X_test, y_test):
    # Evaluate model performance
    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)
    report = classification_report(y_test, predictions)
    matrix = confusion_matrix(y_test, predictions)
    return {
        'accuracy': accuracy,
        'report': report,
        'confusion_matrix': matrix
    }

def save_model(model, filepath):
    # Save trained model to disk
    joblib.dump(model, filepath)

def load_model(filepath):
    # Load trained model from disk
    return joblib.load(filepath)

class TradingModel:
    # Object-oriented wrapper for trading model operations
    def __init__(self, model_type='RandomForest'):
        self.model_type = model_type
        self.model = None
    
    def train(self, X_train, y_train):
        # Train the model
        if self.model_type == 'RandomForest':
            self.model = train_random_forest(X_train, y_train)
        return self.model
    
    def predict(self, X_new):
        # Predict using the trained model
        if self.model is None:
            raise ValueError("Model not trained yet.")
        return self.model.predict(X_new)

    def predict_proba(self, X_test):
        # Predict probabilities if applicable
        if self.model is None:
            raise ValueError("Model not trained yet.")
        return self.model.predict_proba(X_test)
    
    def evaluate(self, X_test, y_test):
        # Evaluate model performance
        if self.model is None:
            raise ValueError("Model not trained yet.")
        return evaluate_model(self.model, X_test, y_test)
    
    def get_feature_importance(self, feature_names):
        # Get feature importance
        if self.model is None:
            raise ValueError("Model not trained yet.")
        importances = self.model.feature_importances_
        return pd.Series(importances, index=feature_names).sort_values(ascending=False)
    
    def save(self, filepath):
        # Save model to disk
        save_model(self.model, filepath)
    
    def load(self, filepath):
        # Load model from disk
        self.model = load_model(filepath)