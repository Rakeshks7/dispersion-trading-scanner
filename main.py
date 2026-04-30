import matplotlib.pyplot as plt
from data.synthetic_data import generate_synthetic_market_data
from engine.signal_generator import DispersionScanner
from engine.backtester import DeltaHedger
from config import COMPONENTS

def main():
    print("1. Fetching Market Data (Synthetic Generation)...")
    spot_df, iv_df = generate_synthetic_market_data(days=252)
    
    print("2. Scanning for Dispersion Signals...")
    scanner = DispersionScanner(spot_df, iv_df, COMPONENTS)
    signals = scanner.generate_signals()
    
    print("3. Executing Delta-Hedged Backtest...")
    hedger = DeltaHedger(spot_df, iv_df, signals, COMPONENTS)
    pnl = hedger.run_simulation()

    trade_count = (signals['Position'] != 0).sum()
    print(f"Total Trades Identified: {trade_count}")
    print(f"Final Hedging PnL: ${pnl.iloc[-1]:.2f}")

    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 10), sharex=True)
    
    ax1.plot(signals.index, signals['Implied_Corr'], label="Implied Correlation", color="blue")
    ax1.set_title("Implied Correlation")
    ax1.legend()
    ax1.grid(True)
    
    ax2.plot(signals.index, signals['Z_Score'], label="Z-Score", color="orange")
    ax2.axhline(1.5, color='red', linestyle='--')
    ax2.axhline(-1.5, color='green', linestyle='--')
    ax2.set_title("Signal Generation (Z-Score)")
    ax2.legend()
    ax2.grid(True)
    
    ax3.plot(pnl.index, pnl, label="Cumulative PnL (Hedged)", color="purple")
    ax3.set_title("Delta Hedging Portfolio PnL")
    ax3.legend()
    ax3.grid(True)
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()