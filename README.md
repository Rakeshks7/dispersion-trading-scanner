# The Volatility Trader: Dispersion Trading Scanner

![Python Version](https://img.shields.io/badge/python-3.9%2B-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Status](https://img.shields.io/badge/status-Production_Ready-brightgreen)
![Domain](https://img.shields.io/badge/domain-Quantitative_Finance-orange)

An institutional-grade quantitative finance pipeline designed to scan, backtest, and visualize **Dispersion Trading** strategies. This engine exploits the structural pricing discrepancies between an index's implied volatility and the implied volatility of its underlying components.

---

## Disclaimer
**This project is for educational and portfolio demonstration purposes only.** It does not constitute financial advice, investment recommendations, or a solicitation to buy or sell securities. Options trading carries significant risk. The synthetic data and simplified hedging assumptions used in this simulation do not account for slippage, liquidity constraints, or exact execution costs.

---

## Strategy Overview: The "Top Tier" Twist
Dispersion trading is a classic hedge fund volatility arbitrage strategy rarely utilized by retail traders. It capitalizes on the fact that an index is inherently less volatile than its components due to correlation. 

When **Implied Correlation** is priced historically low, options on the Index become cheap relative to options on the underlying stocks. The strategy takes a market-neutral approach by:
1. Selling volatility on the individual components (Short Straddles).
2. Buying volatility on the Index (Long Straddles).
3. **Delta-hedging** the underlying equities daily to isolate pure volatility/correlation exposure (Vega/Vega-bleed).

---

## Core Features
* **Vectorized Option Pricing:** Custom `BlackScholesPricer` for rapid Greeks and theoretical pricing calculation.
* **Implied Correlation Engine:** Calculates the CBOE-style implied correlation proxy weighted by component variance.
* **Statistical Signal Generation:** Uses rolling Z-Scores of implied correlation to trigger Buy/Sell dispersion entry points.
* **Delta-Hedged Backtester:** Simulates trade PnL by strictly hedging underlying delta exposure daily.
* **Synthetic Market Generator:** Fully functional out-of-the-box with correlated Geometric Brownian Motion spot prices and mean-reverting IV surfaces.

---

## Repository Structure

```text
dispersion_scanner/
│
├── main.py                  # Orchestrates data generation, scanning, and backtesting
├── config.py                # Global parameters (Risk-Free Rate, Thresholds, Weights)
├── requirements.txt         # Project dependencies
│
├── utils/
│   ├── pricer.py            # Vectorized Black-Scholes & Greeks calculator
│   └── math_tools.py        # Variance and Implied Correlation mathematics
│
├── data/
│   └── synthetic_data.py    # Generates mock Spot & IV data (Swappable for Live API)
│
└── engine/
    ├── signal_generator.py  # Z-score and threshold entry logic
    └── backtester.py        # Path-dependent PnL and daily delta-hedging simulator

---

## Future Enhancements
[ ] Integrate Live Options Data APIs (e.g., Polygon.io, Databento, OptionMetrics).

[ ] Incorporate Volatility Smile / Skew interpolation.

[ ] Add transaction costs (spreads, commissions) into the DeltaHedger.

[ ] Transition from ATM straddles to Variance Swaps.

---
