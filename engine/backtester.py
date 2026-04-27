import pandas as pd
import numpy as np
from utils.pricer import BlackScholesPricer
from config import RISK_FREE_RATE, OPTION_MATURITY_DAYS, TRADING_DAYS

class DeltaHedger:
    def __init__(self, spot_df, iv_df, signals, weights):
        self.spot = spot_df
        self.iv = iv_df
        self.signals = signals
        self.weights = weights
        self.bs = BlackScholesPricer()
        
    def run_simulation(self):
        pnl = [0.0]
        active_trade = None

        for i in range(1, len(self.signals)):
            date = self.signals.index[i]
            prev_date = self.signals.index[i-1]
            signal = self.signals['Position'].iloc[i]

            if signal != 0 and active_trade is None:
                active_trade = {
                    'entry_date': date,
                    'direction': signal, 
                    'days_held': 0
                }
                
            daily_pnl = 0.0

            if active_trade is not None:
                ttm = (OPTION_MATURITY_DAYS - active_trade['days_held']) / TRADING_DAYS
                direction = active_trade['direction']

                s_idx = self.spot['SPX'].loc[date]
                iv_idx = self.iv['SPX'].loc[date]
                delta_idx_call = self.bs.delta(s_idx, s_idx, ttm, RISK_FREE_RATE, iv_idx, 'call')
                delta_idx_put = self.bs.delta(s_idx, s_idx, ttm, RISK_FREE_RATE, iv_idx, 'put')
                straddle_delta_idx = delta_idx_call + delta_idx_put

                idx_price_change = self.spot['SPX'].loc[date] - self.spot['SPX'].loc[prev_date]
                daily_pnl += (idx_price_change * -straddle_delta_idx * -direction)

                for ticker, weight in self.weights.items():
                    s_cmp = self.spot[ticker].loc[date]
                    iv_cmp = self.iv[ticker].loc[date]
                    
                    delta_cmp_call = self.bs.delta(s_cmp, s_cmp, ttm, RISK_FREE_RATE, iv_cmp, 'call')
                    delta_cmp_put = self.bs.delta(s_cmp, s_cmp, ttm, RISK_FREE_RATE, iv_cmp, 'put')
                    straddle_delta_cmp = delta_cmp_call + delta_cmp_put
                    
                    cmp_price_change = self.spot[ticker].loc[date] - self.spot[ticker].loc[prev_date]
                    daily_pnl += (cmp_price_change * -straddle_delta_cmp * direction * weight * 100)
                
                active_trade['days_held'] += 1
                if active_trade['days_held'] >= 10:  
                    active_trade = None
            
            pnl.append(pnl[-1] + daily_pnl)
            
        return pd.Series(pnl, index=self.signals.index)