import numpy as np
import pandas as pd
from config import COMPONENTS, TRADING_DAYS

def generate_synthetic_market_data(days=252):
    np.random.seed(42)
    dates = pd.date_range(end=pd.Timestamp.today(), periods=days, freq='B')

    dt = 1/TRADING_DAYS
    tickers = list(COMPONENTS.keys())

    spot_data = {}
    for ticker in tickers:
        returns = np.random.normal(0.0005, 0.015, days)
        spot_data[ticker] = 100 * np.exp(np.cumsum(returns))

    spot_df = pd.DataFrame(spot_data, index=dates)
    index_spot = sum(spot_df[t] * w for t, w in COMPONENTS.items())
    spot_df['SPX'] = index_spot

    iv_data = {}
    for ticker in tickers:
        base_iv = np.random.normal(0.25, 0.05, days)
        iv_data[ticker] = pd.Series(base_iv).rolling(5, min_periods=1).mean().values
        
    iv_df = pd.DataFrame(iv_data, index=dates)

    index_iv = sum(iv_df[t] * w for t, w in COMPONENTS.items()) * 0.7  # 0.7 simulates base correlation
    index_iv[100:120] = index_iv[100:120] * 0.6 
    iv_df['SPX'] = index_iv
    
    return spot_df, iv_df