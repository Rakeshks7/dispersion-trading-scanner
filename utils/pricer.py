import numpy as np
from scipy.stats import norm
import logging

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

class BlackScholesPricer:
    
    @staticmethod
    def _d1_d2(S, K, T, r, sigma):
        T = np.maximum(T, 1e-5)
        d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
        d2 = d1 - sigma * np.sqrt(T)
        return d1, d2

    @classmethod
    def price(cls, S, K, T, r, sigma, option_type='call'):
        d1, d2 = cls._d1_d2(S, K, T, r, sigma)
        if option_type == 'call':
            return S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
        elif option_type == 'put':
            return K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
        else:
            raise ValueError("option_type must be 'call' or 'put'")

    @classmethod
    def delta(cls, S, K, T, r, sigma, option_type='call'):
        d1, _ = cls._d1_d2(S, K, T, r, sigma)
        if option_type == 'call':
            return norm.cdf(d1)
        elif option_type == 'put':
            return norm.cdf(d1) - 1.0
        else:
            raise ValueError("option_type must be 'call' or 'put'")