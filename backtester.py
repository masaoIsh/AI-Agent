"""
Portfolio backtesting utilities: compute returns, rebalance, and evaluate performance.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Optional

import numpy as np
import pandas as pd


@dataclass
class BacktestResult:
    equity_curve: pd.Series
    weights_history: pd.DataFrame
    metrics: Dict[str, float]


def compute_returns(price_df: pd.DataFrame) -> pd.DataFrame:
    prices = price_df.sort_index()
    returns = prices.pct_change().dropna(how="all")
    return returns


def rebalance_weights(
    target_weights: pd.Series,
    index: pd.DatetimeIndex,
    frequency: str = "M",
) -> pd.DataFrame:
    # Map deprecated frequency aliases to new ones
    freq_map = {'M': 'ME', 'Q': 'QE', 'Y': 'YE', 'A': 'YE'}
    freq = freq_map.get(frequency, frequency)
    
    # Create rebalancing dates by resampling index to given frequency on last available day
    # This gives us the actual dates in our index that correspond to period ends
    rebal_series = pd.Series(1.0, index=index).resample(freq).last()
    rebal_dates = rebal_series.index
    
    # Create weights dataframe
    weights = pd.DataFrame(index=index, columns=target_weights.index, dtype=float)
    
    # Set weights at rebalancing dates (these are guaranteed to be in the index)
    for date in rebal_dates:
        if date in weights.index:
            weights.loc[date] = target_weights.values
    
    # Forward fill and handle NaN
    weights = weights.ffill().fillna(0.0)
    return weights


def run_backtest(
    price_df: pd.DataFrame,
    weights_schedule: Optional[pd.DataFrame] = None,
    target_weights: Optional[pd.Series] = None,
    rebalance_frequency: str = "M",
    cash_rate_daily: float = 0.0,
    trading_cost_bps: float = 0.0,
) -> BacktestResult:
    """
    Run a simple backtest on price history with either a static weights schedule or target weights with periodic rebalancing.
    price_df: columns are tickers, index is datetime, values are prices (use adj close for equities).
    """
    assert (weights_schedule is not None) or (target_weights is not None), "Provide weights_schedule or target_weights"

    # Ensure price_df has a simple Index (not MultiIndex) on columns
    if isinstance(price_df.columns, pd.MultiIndex):
        price_df = price_df.copy()
        price_df.columns = price_df.columns.get_level_values(-1)
    
    ret = compute_returns(price_df)
    ret = ret.reindex(price_df.index).fillna(0.0)

    if weights_schedule is None:
        weights_schedule = rebalance_weights(target_weights, price_df.index, frequency=rebalance_frequency)

    weights_schedule = weights_schedule.reindex(price_df.index).ffill().fillna(0.0)
    
    # Ensure column alignment between weights and returns
    common_cols = list(set(weights_schedule.columns) & set(ret.columns))
    if len(common_cols) == 0:
        raise ValueError("No overlapping columns between weights and returns")
    weights_schedule = weights_schedule[common_cols]
    ret = ret[common_cols]

    # Normalize weights row-wise to sum to 1 (allow cash via shortfall)
    row_sums = weights_schedule.sum(axis=1).replace(0.0, np.nan)
    norm_weights = weights_schedule.div(row_sums, axis=0).fillna(0.0)

    # Transaction costs applied on weight changes (naive proxy)
    weight_changes = norm_weights.diff().abs().fillna(0.0)
    daily_cost = (weight_changes.sum(axis=1) * (trading_cost_bps / 10000.0)).clip(lower=0.0)

    # Portfolio daily return
    port_ret_gross = (norm_weights.shift(1).fillna(0.0) * ret).sum(axis=1)
    port_ret_net = port_ret_gross - daily_cost + cash_rate_daily

    equity_curve = (1.0 + port_ret_net).cumprod()

    metrics = compute_metrics(port_ret_net, equity_curve)
    return BacktestResult(equity_curve=equity_curve, weights_history=norm_weights, metrics=metrics)


def compute_metrics(daily_returns: pd.Series, equity_curve: pd.Series) -> Dict[str, float]:
    daily_returns = daily_returns.astype(float)
    n_days = len(daily_returns)
    if n_days == 0:
        return {"CAGR": 0.0, "Vol": 0.0, "Sharpe": 0.0, "MaxDD": 0.0}

    total_return = float(equity_curve.iloc[-1] - 1.0)
    years = max(n_days / 252.0, 1e-9)
    cagr = float((1.0 + total_return) ** (1.0 / years) - 1.0)

    vol = float(daily_returns.std(ddof=0) * np.sqrt(252))
    sharpe = float((daily_returns.mean() * 252) / (vol if vol != 0 else np.nan))
    if np.isnan(sharpe):
        sharpe = 0.0

    roll_max = equity_curve.cummax()
    drawdown = equity_curve / roll_max - 1.0
    max_dd = float(drawdown.min())

    return {"CAGR": cagr, "Vol": vol, "Sharpe": sharpe, "MaxDD": max_dd}


