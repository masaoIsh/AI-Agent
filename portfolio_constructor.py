"""
Portfolio construction utilities: equal-weight and inverse-volatility weighting.
"""

from __future__ import annotations

from typing import Optional

import numpy as np
import pandas as pd


def equal_weight_weights(tickers: list[str]) -> pd.Series:
    n = len(tickers)
    w = np.repeat(1.0 / n if n > 0 else 0.0, n)
    return pd.Series(w, index=tickers)


def inverse_vol_weights(price_df: pd.DataFrame, lookback_days: int = 63, min_weight: float = 0.0) -> pd.Series:
    ret = price_df.sort_index().pct_change().dropna(how="all")
    recent = ret.iloc[-lookback_days:]
    vol = recent.std(ddof=0)
    inv_vol = 1.0 / vol.replace(0.0, np.nan)
    inv_vol = inv_vol.replace([np.inf, -np.inf], np.nan).fillna(0.0)
    if inv_vol.sum() == 0:
        return equal_weight_weights(list(price_df.columns))
    w = inv_vol / inv_vol.sum()
    if min_weight > 0:
        w = w.clip(lower=min_weight)
        w = w / w.sum()
    return w


