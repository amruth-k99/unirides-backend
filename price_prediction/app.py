import sys
import numpy as np
import joblib

# Recreate LogTransfomer class (with possible typo as seen in the error)
class LogTransfomer:  # Use "LogTransfomer" instead of "LogTransformer"
    def __init__(self):
        pass

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        return np.log1p(X)  # Apply the log transformation

# Add LogTransfomer to sys.modules so pickle can recognize it
sys.modules['__main__.LogTransfomer'] = LogTransfomer

# Load the model
try:
    model = joblib.load('/home/ubuntu/price_prediction/lr_grid.pkl')
    print("✅ Model loaded successfully!")
except Exception as e:
    print(f"❌ Error loading model: {e}")

