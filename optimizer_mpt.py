"""
MPT optimizer and signal-to-mu mapping utilities.

Includes:
- Confidence construction for agents:
  - Yugo: inverse of forecast error via MAPE on simple 1-step forecasts
  - Wassim: fundamentals composite using z(ROE) + z(ROA) mapped via normal CDF
- Score to expected return mapping (annual band -> daily mu)
- Sample covariance and Max Sharpe long-only optimizer with per-name cap
"""

from __future__ import annotations

import numpy as np
import pandas as pd
from typing import Dict, List, Optional


def cross_sectional_z(series: pd.Series) -> pd.Series:
    mu = series.mean()
    sd = series.std(ddof=0)
    if sd == 0 or np.isnan(sd):
        return pd.Series(0.0, index=series.index)
    return (series - mu) / sd


def wassim_confidence(fundamentals_df: pd.DataFrame) -> pd.Series:
    """
    Compute Wassim's confidence per symbol from fundamentals.
    Expects columns: 'symbol','roe','roa'. Returns values in [0,1].
    """
    from scipy.stats import norm  # optional; if missing, fallback handled below

    df = fundamentals_df.set_index('symbol')
    roe = pd.to_numeric(df.get('roe'), errors='coerce').fillna(0.0)
    roa = pd.to_numeric(df.get('roa'), errors='coerce').fillna(0.0)
    z_comp = cross_sectional_z(roe) + cross_sectional_z(roa)
    try:
        conf = pd.Series(norm.cdf(z_comp.values), index=z_comp.index)
    except Exception:
        # Fallback: rank-scale to [0,1]
        ranks = z_comp.rank(method="average", ascending=False)
        conf = (ranks.max() - ranks) / max(ranks.max() - ranks.min(), 1e-9)
    return conf.clip(lower=0.0, upper=1.0)


def _mape(actual: pd.Series, forecast: pd.Series) -> float:
    a = actual.align(forecast, join='inner')[0]
    f = forecast.reindex_like(a)
    denom = np.clip(a.abs(), 1e-8, None)
    return float(((a - f).abs() / denom).mean())


def yugo_confidence_from_prices(price_df: pd.DataFrame, lookback: int = 126, method: str = "ema") -> pd.Series:
    """
    Compute Yugo's confidence per symbol as a decreasing function of MAPE
    for a simple 1-step forecast over the last `lookback` days.
    Methods: 'persistence' or 'ema' (~20-day EMA).
    Returns values in [0,1]. Lower error -> higher confidence.
    """
    prices = price_df.sort_index().dropna(how="all").iloc[-(lookback + 1):]
    errs: Dict[str, float] = {}
    for sym in prices.columns:
        p = prices[sym].dropna()
        if len(p) < max(20, lookback // 2):
            errs[sym] = np.nan
            continue
        if method == "persistence":
            fcast = p.shift(1)
        else:
            alpha = 2.0 / 21.0  # ~20-day EMA
            ema = p.ewm(alpha=alpha, adjust=False).mean()
            fcast = ema.shift(1)
        errs[sym] = _mape(p, fcast)

    err_series = pd.Series(errs)
    # Handle all-NaN or constant
    if err_series.isna().all():
        return pd.Series(0.5, index=prices.columns)
    err_series = err_series.fillna(err_series.median())
    ranks = err_series.rank(method="average", ascending=True)  # low error = rank 1
    conf = 1.0 - (ranks - 1) / max(len(ranks) - 1, 1)
    return conf.clip(lower=0.0, upper=1.0)


def combine_confidence(c_wassim: pd.Series, c_yugo: pd.Series, w_wassim: float = 0.5, w_yugo: float = 0.5) -> pd.Series:
    idx = sorted(set(c_wassim.index) | set(c_yugo.index))
    cw = c_wassim.reindex(idx).fillna(0.5)
    cy = c_yugo.reindex(idx).fillna(0.5)
    s = w_wassim * cw + w_yugo * cy
    return s.clip(lower=0.0, upper=1.0)


def map_scores_to_expected_returns_from_confidence(
    confidence: pd.Series,
    ann_low: float = 0.02,
    ann_high: float = 0.15,
) -> pd.Series:
    """
    Convert confidence scores in [0,1] to annual expected returns via rank mapping
    then to daily mean returns for the optimizer.
    """
    if confidence.max() == confidence.min():
        ann = pd.Series(ann_low, index=confidence.index)
    else:
        ranks = confidence.rank(method="average", ascending=False)
        scaled = (ranks.max() - ranks) / max(ranks.max() - ranks.min(), 1e-9)
        ann = ann_low + scaled * (ann_high - ann_low)
    mu_daily = (1.0 + ann) ** (1.0 / 252.0) - 1.0
    return mu_daily


def sample_covariance(returns: pd.DataFrame, lookback: int = 252) -> pd.DataFrame:
    r = returns.dropna(how="all").iloc[-lookback:]
    return r.cov(ddof=0)


def tangency_unconstrained(mu: pd.Series, cov: pd.DataFrame) -> pd.Series:
    Sigma = cov.values
    mu_vec = mu.values.reshape(-1, 1)
    inv = np.linalg.pinv(Sigma)
    w = (inv @ mu_vec).flatten()
    w = np.maximum(w, 0.0)
    if w.sum() == 0:
        w = np.ones_like(w)
    w = w / w.sum()
    return pd.Series(w, index=mu.index)


def max_sharpe_long_only(mu: pd.Series, cov: pd.DataFrame, max_weight: float = 0.20) -> pd.Series:
    tickers = list(mu.index)
    n = len(tickers)
    mu_v = mu.values
    Sigma = cov.values

    try:
        from scipy.optimize import minimize

        def neg_sharpe(w: np.ndarray) -> float:
            r = float(w @ mu_v)
            v = float(w @ Sigma @ w)
            if v <= 0:
                return 1e6
            return - r / np.sqrt(v)

        cons = [{'type': 'eq', 'fun': lambda w: np.sum(w) - 1.0}]
        bnds = [(0.0, max_weight)] * n
        w0 = np.repeat(1.0 / n, n)

        res = minimize(neg_sharpe, w0, method='SLSQP', bounds=bnds, constraints=cons,
                       options={'maxiter': 200, 'ftol': 1e-9})
        if res.success:
            w = np.clip(res.x, 0.0, max_weight)
            w = w / w.sum()
            return pd.Series(w, index=tickers)
        return tangency_unconstrained(mu, cov)
    except Exception:
        return tangency_unconstrained(mu, cov)


