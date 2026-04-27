import pandas as pd
from utils.math_tools import calculate_implied_correlation
from config import Z_SCORE_THRESHOLD

class DispersionScanner:
    def __init__(self, spot_df, iv_df, weights):
        self.spot_df = spot_df
        self.iv_df = iv_df
        self.weights = weights
        
    def generate_signals(self, window=21):
        index_iv = self.iv_df['SPX']
        component_ivs = self.iv_df.drop(columns=['SPX'])
        
        implied_corr = calculate_implied_correlation(index_iv, component_ivs, self.weights)

        rolling_mean = implied_corr.rolling(window=window).mean()
        rolling_std = implied_corr.rolling(window=window).std()
        z_score = (implied_corr - rolling_mean) / rolling_std
        
        signals = pd.DataFrame(index=implied_corr.index)
        signals['Implied_Corr'] = implied_corr
        signals['Z_Score'] = z_score

        signals['Position'] = 0
        signals.loc[z_score > Z_SCORE_THRESHOLD, 'Position'] = 1
        signals.loc[z_score < -Z_SCORE_THRESHOLD, 'Position'] = -1
        
        return signals