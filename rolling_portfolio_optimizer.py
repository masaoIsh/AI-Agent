"""
Rolling Portfolio Optimizer with Walk-Forward Out-of-Sample Testing

This module implements proper out-of-sample backtesting by:
1. Dividing the timeline into rebalancing periods
2. At each rebalancing date, using ONLY past data to optimize
3. Applying optimized weights to future periods until next rebalance

This avoids look-ahead bias and provides realistic performance estimates.
"""

from __future__ import annotations
from typing import Dict, List, Optional, Tuple
import numpy as np
import pandas as pd
from datetime import datetime

from backtester import compute_returns
from optimizer_mpt import (
    wassim_confidence,
    yugo_confidence_from_prices,
    combine_confidence,
    map_scores_to_expected_returns_from_confidence,
    sample_covariance,
    max_sharpe_long_only,
)
from portfolio_constructor import inverse_vol_weights, equal_weight_weights


def get_rebalancing_dates(index: pd.DatetimeIndex, frequency: str = "M") -> pd.DatetimeIndex:
    """
    Get rebalancing dates from a datetime index based on frequency.
    
    Parameters:
    - index: DatetimeIndex of the full dataset
    - frequency: 'D', 'W', 'M', 'Q', 'Y'
    
    Returns:
    - DatetimeIndex of rebalancing dates that exist in the original index
    """
    # Map deprecated frequency aliases to new ones
    freq_map = {'M': 'ME', 'Q': 'QE', 'Y': 'YE', 'A': 'YE'}
    freq = freq_map.get(frequency, frequency)
    
    # Create rebalancing dates by resampling to given frequency
    rebal_series = pd.Series(1.0, index=index).resample(freq).last()
    return rebal_series.index


def rolling_optimize_weights(
    price_df: pd.DataFrame,
    fundamentals_df: Optional[pd.DataFrame],
    rebalance_frequency: str = "M",
    strategy: str = "mpt",
    min_train_days: int = 252,
    lookback_days: Optional[int] = None,
    max_weight: float = 0.20,
    w_wassim: float = 0.5,
    w_yugo: float = 0.5,
    ann_low: float = 0.02,
    ann_high: float = 0.15,
    verbose: bool = True,
) -> pd.DataFrame:
    """
    Perform rolling portfolio optimization with proper out-of-sample methodology.
    
    At each rebalancing date:
    1. Use only data UP TO that date (expanding or rolling window)
    2. Calculate statistics (returns, covariance, confidence)
    3. Optimize portfolio weights
    4. Apply these weights going forward until next rebalance
    
    Parameters:
    - price_df: DataFrame with datetime index, columns are tickers
    - fundamentals_df: DataFrame with fundamentals data (for Wassim confidence)
    - rebalance_frequency: How often to rebalance ('D', 'W', 'M', 'Q', 'Y')
    - strategy: 'mpt', 'invvol', or 'equal'
    - min_train_days: Minimum days of history before first rebalance
    - lookback_days: If provided, use rolling window; otherwise use expanding window
    - max_weight: Maximum weight per position (for MPT)
    - w_wassim, w_yugo: Weights for combining agent confidences
    - ann_low, ann_high: Expected return band for mapping confidence to mu
    - verbose: Print progress
    
    Returns:
    - DataFrame with weights schedule (index=dates, columns=tickers)
    """
    price_df = price_df.sort_index()
    symbols = list(price_df.columns)
    
    # Get rebalancing dates
    rebal_dates = get_rebalancing_dates(price_df.index, frequency=rebalance_frequency)
    
    # Filter to dates with sufficient history
    rebal_dates = [d for d in rebal_dates if (d - price_df.index[0]).days >= min_train_days]
    
    if len(rebal_dates) == 0:
        raise ValueError(f"No rebalancing dates found with min_train_days={min_train_days}")
    
    if verbose:
        print(f"\n🔄 Rolling Optimization (OUT-OF-SAMPLE)")
        print(f"   Strategy: {strategy.upper()}")
        print(f"   Rebalance frequency: {rebalance_frequency}")
        print(f"   Number of rebalancing periods: {len(rebal_dates)}")
        print(f"   First rebalance: {rebal_dates[0].strftime('%Y-%m-%d')}")
        print(f"   Last rebalance: {rebal_dates[-1].strftime('%Y-%m-%d')}")
        print(f"   Window type: {'Rolling (%d days)' % lookback_days if lookback_days else 'Expanding'}")
        print()
    
    # Initialize weights schedule
    weights_schedule = pd.DataFrame(index=price_df.index, columns=symbols, dtype=float)
    
    # Track rebalancing history for analysis
    rebal_history = []
    
    for i, rebal_date in enumerate(rebal_dates, 1):
        if verbose and (i % max(1, len(rebal_dates) // 10) == 0):
            print(f"   Optimizing at rebalance {i}/{len(rebal_dates)}: {rebal_date.strftime('%Y-%m-%d')}")
        
        # Extract training data: everything UP TO and including rebal_date
        # Use nearest date if exact match doesn't exist
        if lookback_days:
            # Rolling window: use last N days
            # Find the closest date in the index (rebal_date should already be in index from get_rebalancing_dates)
            try:
                train_end_idx = price_df.index.get_loc(rebal_date)
            except KeyError:
                # If exact date not found, get the nearest preceding date
                train_end_idx = price_df.index.get_indexer([rebal_date], method='ffill')[0]
                if train_end_idx == -1:
                    continue  # Skip if no valid date
            train_start_idx = max(0, train_end_idx - lookback_days + 1)
            train_data = price_df.iloc[train_start_idx:train_end_idx + 1]
        else:
            # Expanding window: use all data from start
            # loc with slicing handles missing exact dates gracefully
            train_data = price_df.loc[:rebal_date]
        
        # Skip if insufficient data
        if len(train_data) < min_train_days // 2:
            continue
        
        # Optimize weights based on strategy
        try:
            if strategy == 'equal':
                w = equal_weight_weights(symbols)
            
            elif strategy == 'invvol':
                w = inverse_vol_weights(train_data, lookback_days=min(63, len(train_data) // 4))
            
            elif strategy == 'mpt':
                # Build confidence scores using ONLY training data
                c_wassim = pd.Series(0.5, index=symbols)  # Default neutral
                if fundamentals_df is not None:
                    try:
                        c_wassim = wassim_confidence(fundamentals_df)
                    except Exception:
                        pass
                
                c_yugo = yugo_confidence_from_prices(
                    train_data, 
                    lookback=min(126, len(train_data) // 2),
                    method="ema"
                )
                
                c = combine_confidence(c_wassim, c_yugo, w_wassim=w_wassim, w_yugo=w_yugo)
                c = c.reindex(symbols).fillna(0.5)
                
                # Map confidence to expected returns
                mu = map_scores_to_expected_returns_from_confidence(c, ann_low=ann_low, ann_high=ann_high)
                
                # Compute covariance from training data returns
                returns = compute_returns(train_data)
                Sigma = sample_covariance(returns, lookback=min(252, len(returns)))
                
                # Align and optimize
                common = mu.index.intersection(Sigma.columns)
                if len(common) < 2:
                    # Fallback to inverse vol
                    w = inverse_vol_weights(train_data)
                else:
                    mu = mu.loc[common]
                    Sigma = Sigma.loc[common, common]
                    w = max_sharpe_long_only(mu, Sigma, max_weight=max_weight)
                    # Ensure full symbol coverage
                    w = w.reindex(symbols).fillna(0.0)
                    w = w / w.sum() if w.sum() > 0 else pd.Series(1.0 / len(symbols), index=symbols)
            
            else:
                raise ValueError(f"Unknown strategy: {strategy}")
            
            # Record this rebalancing
            rebal_history.append({
                'date': rebal_date,
                'train_size': len(train_data),
                'weights': w.copy(),
            })
            
            # Apply weights from rebal_date forward until next rebalance (or end)
            # Find the next rebalancing date
            next_rebal_idx = i if i < len(rebal_dates) else None
            if next_rebal_idx and next_rebal_idx < len(rebal_dates):
                next_rebal_date = rebal_dates[next_rebal_idx]
                mask = (weights_schedule.index >= rebal_date) & (weights_schedule.index < next_rebal_date)
            else:
                mask = weights_schedule.index >= rebal_date
            
            # Assign weights to this period
            for symbol in symbols:
                weights_schedule.loc[mask, symbol] = w.get(symbol, 0.0)
        
        except Exception as e:
            if verbose:
                print(f"   ⚠️  Warning: Failed to optimize at {rebal_date}: {e}")
            continue
    
    # Fill any remaining NaN with 0
    weights_schedule = weights_schedule.fillna(0.0)
    
    if verbose:
        print(f"\n✅ Rolling optimization complete: {len(rebal_history)} rebalancing events")
        print(f"   Coverage: {(weights_schedule.sum(axis=1) > 0).sum()}/{len(weights_schedule)} days")
    
    # Store rebalancing history as metadata
    weights_schedule.attrs['rebal_history'] = rebal_history
    weights_schedule.attrs['strategy'] = strategy
    weights_schedule.attrs['oos_validated'] = True
    
    return weights_schedule


def compare_in_sample_vs_out_of_sample(
    price_df: pd.DataFrame,
    fundamentals_df: Optional[pd.DataFrame],
    rebalance_frequency: str = "M",
    strategy: str = "mpt",
    **kwargs
) -> Tuple[pd.DataFrame, pd.DataFrame, Dict]:
    """
    Compare in-sample (look-ahead bias) vs out-of-sample (proper) backtesting.
    
    Returns:
    - weights_in_sample: Weights computed using ALL data (biased)
    - weights_out_of_sample: Weights computed using rolling optimization (proper)
    - comparison_dict: Dictionary with comparative metrics
    """
    from portfolio_constructor import inverse_vol_weights, equal_weight_weights
    from optimizer_mpt import max_sharpe_long_only
    
    symbols = list(price_df.columns)
    
    # IN-SAMPLE: Use ALL data to optimize (this is what the current code does)
    print("\n📊 Computing IN-SAMPLE weights (uses future data - BIASED)...")
    if strategy == 'equal':
        w_in_sample = equal_weight_weights(symbols)
    elif strategy == 'invvol':
        w_in_sample = inverse_vol_weights(price_df)
    elif strategy == 'mpt':
        c_w = wassim_confidence(fundamentals_df) if fundamentals_df is not None else pd.Series(0.5, index=symbols)
        c_y = yugo_confidence_from_prices(price_df, lookback=126, method="ema")
        c = combine_confidence(c_w, c_y, w_wassim=0.5, w_yugo=0.5)
        c = c.reindex(symbols).fillna(0.5)
        mu = map_scores_to_expected_returns_from_confidence(c)
        returns = compute_returns(price_df)
        Sigma = sample_covariance(returns, lookback=252)
        common = mu.index.intersection(Sigma.columns)
        if len(common) >= 2:
            mu = mu.loc[common]
            Sigma = Sigma.loc[common, common]
            w_in_sample = max_sharpe_long_only(mu, Sigma, max_weight=kwargs.get('max_weight', 0.20))
        else:
            w_in_sample = equal_weight_weights(symbols)
    else:
        w_in_sample = equal_weight_weights(symbols)
    
    # Create static weights schedule
    weights_in_sample = pd.DataFrame(
        index=price_df.index,
        columns=symbols,
        data=np.tile(w_in_sample.values, (len(price_df), 1))
    )
    weights_in_sample.attrs['oos_validated'] = False
    
    # OUT-OF-SAMPLE: Use rolling optimization
    print("\n📊 Computing OUT-OF-SAMPLE weights (proper walk-forward)...")
    weights_out_of_sample = rolling_optimize_weights(
        price_df=price_df,
        fundamentals_df=fundamentals_df,
        rebalance_frequency=rebalance_frequency,
        strategy=strategy,
        verbose=True,
        **kwargs
    )
    
    comparison = {
        'in_sample_static': w_in_sample.to_dict(),
        'out_of_sample_dynamic': len(weights_out_of_sample.attrs.get('rebal_history', [])),
        'method': strategy,
    }
    
    return weights_in_sample, weights_out_of_sample, comparison


def analyze_weight_stability(weights_schedule: pd.DataFrame) -> Dict:
    """
    Analyze how stable the portfolio weights are over time.
    High turnover indicates unstable optimization.
    """
    # Calculate weight changes at each rebalancing
    weight_changes = weights_schedule.diff().abs()
    
    # Sum across all positions to get total turnover per day
    daily_turnover = weight_changes.sum(axis=1)
    
    # Only consider rebalancing days (where turnover > 0)
    rebal_turnover = daily_turnover[daily_turnover > 0]
    
    metrics = {
        'mean_turnover_per_rebalance': float(rebal_turnover.mean()),
        'max_turnover': float(daily_turnover.max()),
        'num_rebalancing_events': int((daily_turnover > 0).sum()),
        'avg_days_between_rebalance': float(len(weights_schedule) / max((daily_turnover > 0).sum(), 1)),
    }
    
    return metrics

