import numpy as np
import pandas as pd

def calculate_implied_correlation(index_iv: pd.Series, component_ivs: pd.DataFrame, weights: dict) -> pd.Series:
    var_index = index_iv ** 2

    weighted_var_sum = pd.Series(0.0, index=index_iv.index)
    weighted_vol_sum = pd.Series(0.0, index=index_iv.index)
    
    for ticker, weight in weights.items():
        iv = component_ivs[ticker]
        weighted_var_sum += (weight ** 2) * (iv ** 2)
        weighted_vol_sum += weight * iv
        
    numerator = var_index - weighted_var_sum
    denominator = (weighted_vol_sum ** 2) - weighted_var_sum

    implied_corr = numerator / denominator.replace(0, np.nan)
    implied_corr = implied_corr.clip(0.0, 1.0).fillna(0)
    
    return implied_corr