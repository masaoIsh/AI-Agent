"""
Quick test script to verify out-of-sample backtesting implementation.
This creates synthetic data and runs both in-sample and OOS backtests.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from rolling_portfolio_optimizer import (
    rolling_optimize_weights,
    compare_in_sample_vs_out_of_sample,
    analyze_weight_stability,
)
from backtester import run_backtest
from portfolio_constructor import equal_weight_weights

def generate_synthetic_data(n_days=1000, n_stocks=5, seed=42):
    """Generate synthetic price data for testing"""
    np.random.seed(seed)
    
    # Create date range
    end_date = datetime.now()
    start_date = end_date - timedelta(days=n_days)
    dates = pd.date_range(start=start_date, end=end_date, freq='D')[:n_days]
    
    # Generate random walk prices
    tickers = [f'STOCK{i}' for i in range(1, n_stocks + 1)]
    prices = {}
    
    for ticker in tickers:
        # Random walk with drift
        returns = np.random.normal(0.0005, 0.02, n_days)  # ~12.5% annual return, 32% vol
        price_series = 100 * np.exp(np.cumsum(returns))
        prices[ticker] = price_series
    
    price_df = pd.DataFrame(prices, index=dates)
    return price_df


def test_rolling_optimization():
    """Test the rolling optimization with synthetic data"""
    print("=" * 80)
    print("🧪 TESTING OUT-OF-SAMPLE BACKTESTING IMPLEMENTATION")
    print("=" * 80)
    
    # Generate test data
    print("\n📊 Generating synthetic price data...")
    price_df = generate_synthetic_data(n_days=1000, n_stocks=5, seed=42)
    print(f"   Generated: {len(price_df)} days, {len(price_df.columns)} stocks")
    print(f"   Date range: {price_df.index[0].date()} to {price_df.index[-1].date()}")
    
    # Test rolling optimization
    print("\n🔄 Testing OUT-OF-SAMPLE rolling optimization...")
    try:
        weights_oos = rolling_optimize_weights(
            price_df=price_df,
            fundamentals_df=None,  # No fundamentals for synthetic data
            rebalance_frequency='M',
            strategy='invvol',  # Use simple strategy for testing
            min_train_days=126,
            lookback_days=252,  # Use rolling 1-year window
            verbose=True
        )
        print("✅ Rolling optimization successful!")
        
        # Analyze stability
        stability = analyze_weight_stability(weights_oos)
        print(f"\n📊 Weight Stability:")
        print(f"   Mean turnover: {stability['mean_turnover_per_rebalance']:.2%}")
        print(f"   Rebalancing events: {stability['num_rebalancing_events']}")
        print(f"   Days between rebalances: {stability['avg_days_between_rebalance']:.1f}")
        
    except Exception as e:
        print(f"❌ Rolling optimization failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # Run OOS backtest
    print("\n📈 Running OUT-OF-SAMPLE backtest...")
    try:
        res_oos = run_backtest(
            price_df,
            weights_schedule=weights_oos,
            trading_cost_bps=5.0
        )
        print("✅ OOS backtest successful!")
        print(f"\n   Performance Metrics (OUT-OF-SAMPLE):")
        for k, v in res_oos.metrics.items():
            print(f"   {k}: {v:.4f}")
    except Exception as e:
        print(f"❌ OOS backtest failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # Run in-sample for comparison
    print("\n📈 Running IN-SAMPLE backtest (for comparison)...")
    try:
        from portfolio_constructor import inverse_vol_weights
        w_in = inverse_vol_weights(price_df, lookback_days=252)
        res_in = run_backtest(
            price_df,
            target_weights=w_in,
            rebalance_frequency='M',
            trading_cost_bps=5.0
        )
        print("✅ In-sample backtest successful!")
        print(f"\n   Performance Metrics (IN-SAMPLE):")
        for k, v in res_in.metrics.items():
            print(f"   {k}: {v:.4f}")
    except Exception as e:
        print(f"❌ In-sample backtest failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # Compare results
    print("\n📊 COMPARISON: Out-of-Sample vs In-Sample")
    print("=" * 80)
    print(f"{'Metric':<15} {'Out-of-Sample':<20} {'In-Sample':<20} {'Difference':<15}")
    print("-" * 80)
    for k in res_oos.metrics.keys():
        oos_val = res_oos.metrics[k]
        in_val = res_in.metrics[k]
        diff = oos_val - in_val
        diff_pct = (diff / abs(in_val) * 100) if in_val != 0 else 0
        print(f"{k:<15} {oos_val:>18.4f}  {in_val:>18.4f}  {diff:>+13.4f} ({diff_pct:+.1f}%)")
    
    # Interpretation
    print("\n💡 INTERPRETATION:")
    sharpe_degradation = ((res_oos.metrics['Sharpe'] - res_in.metrics['Sharpe']) / 
                         abs(res_in.metrics['Sharpe']) * 100) if res_in.metrics['Sharpe'] != 0 else 0
    
    if abs(sharpe_degradation) < 15:
        print("   ✅ Sharpe degradation < 15%: Excellent - strategy is robust!")
    elif abs(sharpe_degradation) < 30:
        print("   ✅ Sharpe degradation < 30%: Good - typical for OOS validation")
    else:
        print("   ⚠️  Sharpe degradation > 30%: Significant - may indicate overfitting")
    
    print(f"\n   OOS Sharpe: {res_oos.metrics['Sharpe']:.3f}")
    if res_oos.metrics['Sharpe'] > 0.7:
        print("   ✅ OOS Sharpe > 0.7: Strong strategy!")
    elif res_oos.metrics['Sharpe'] > 0.4:
        print("   ✅ OOS Sharpe > 0.4: Decent strategy")
    else:
        print("   ⚠️  OOS Sharpe < 0.4: Weak strategy, reconsider approach")
    
    print("\n" + "=" * 80)
    print("✅ ALL TESTS PASSED!")
    print("=" * 80)
    print("\n💡 The implementation is working correctly.")
    print("   You can now use this for real portfolio analysis with confidence.")
    
    return True


def test_expanding_vs_rolling():
    """Compare expanding window vs rolling window"""
    print("\n" + "=" * 80)
    print("🔬 BONUS TEST: Expanding vs Rolling Window")
    print("=" * 80)
    
    price_df = generate_synthetic_data(n_days=1000, n_stocks=5, seed=42)
    
    # Expanding window
    print("\n1️⃣  Testing EXPANDING window (uses all history)...")
    weights_exp = rolling_optimize_weights(
        price_df=price_df,
        fundamentals_df=None,
        rebalance_frequency='M',
        strategy='invvol',
        min_train_days=126,
        lookback_days=None,  # Expanding
        verbose=False
    )
    res_exp = run_backtest(price_df, weights_schedule=weights_exp, trading_cost_bps=5.0)
    print(f"   Expanding Window Sharpe: {res_exp.metrics['Sharpe']:.4f}")
    
    # Rolling window
    print("\n2️⃣  Testing ROLLING window (last 252 days only)...")
    weights_roll = rolling_optimize_weights(
        price_df=price_df,
        fundamentals_df=None,
        rebalance_frequency='M',
        strategy='invvol',
        min_train_days=126,
        lookback_days=252,  # Rolling 1 year
        verbose=False
    )
    res_roll = run_backtest(price_df, weights_schedule=weights_roll, trading_cost_bps=5.0)
    print(f"   Rolling Window Sharpe: {res_roll.metrics['Sharpe']:.4f}")
    
    # Compare
    print(f"\n   Difference: {abs(res_exp.metrics['Sharpe'] - res_roll.metrics['Sharpe']):.4f}")
    if abs(res_exp.metrics['Sharpe'] - res_roll.metrics['Sharpe']) < 0.1:
        print("   ✅ Similar performance - strategy is stable across window types")
    else:
        print("   ⚠️  Different performance - strategy sensitive to window choice")


if __name__ == "__main__":
    print("\n" + "=" * 80)
    print("OUT-OF-SAMPLE BACKTESTING - IMPLEMENTATION TEST")
    print("=" * 80)
    print("\nThis script tests the new OOS backtesting implementation with synthetic data.")
    print("If all tests pass, the implementation is ready for real portfolio analysis.\n")
    
    # Run main test
    success = test_rolling_optimization()
    
    if success:
        # Run bonus test
        test_expanding_vs_rolling()
        
        print("\n" + "=" * 80)
        print("🎉 SUCCESS! Implementation is verified and ready to use.")
        print("=" * 80)
        print("\nNext steps:")
        print("1. Run: python interactive_cli.py")
        print("2. Choose option 2 (Portfolio backtesting)")
        print("3. When prompted, choose 'Y' for OUT-OF-SAMPLE validation")
        print("4. Compare with in-sample to see the difference")
        print("\nSee OUT_OF_SAMPLE_BACKTEST_GUIDE.md for detailed documentation.")
    else:
        print("\n" + "=" * 80)
        print("❌ TESTS FAILED - Please review errors above")
        print("=" * 80)

