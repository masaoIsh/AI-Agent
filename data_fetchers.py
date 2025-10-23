"""
Unified data fetchers for Yahoo Finance and FRED.

Functions:
- fetch_yahoo_prices(symbols, start, end, interval)
- fetch_fred_series(series_ids, start, end, api_key_env="FRED_API_KEY")
"""

from __future__ import annotations

import os
from datetime import datetime
from typing import Dict, List, Optional

import pandas as pd


def fetch_yahoo_prices(
    symbols: List[str],
    start: Optional[str] = None,
    end: Optional[str] = None,
    interval: str = "1d",
) -> Dict[str, pd.DataFrame]:
    """
    Fetch adjusted OHLCV data for symbols from Yahoo Finance.
    Returns dict[symbol] -> DataFrame indexed by datetime with columns including 'Adj Close'.
    """
    try:
        import yfinance as yf
    except ImportError as e:
        raise ImportError("yfinance is required. Install with `pip install yfinance`. ") from e

    if start is None:
        start = "2000-01-01"
    if end is None:
        end = datetime.today().strftime("%Y-%m-%d")

    result: Dict[str, pd.DataFrame] = {}
    for sym in symbols:
        data = yf.download(sym, start=start, end=end, interval=interval, auto_adjust=False, progress=False)
        if not isinstance(data, pd.DataFrame) or data.empty:
            result[sym] = pd.DataFrame()
            continue
        # Standardize column names
        data = data.rename(columns={
            "Adj Close": "adj_close",
            "Close": "close",
            "Open": "open",
            "High": "high",
            "Low": "low",
            "Volume": "volume",
        })
        data.index = pd.to_datetime(data.index)
        result[sym] = data
    return result


def fetch_fred_series(
    series_ids: List[str],
    start: Optional[str] = None,
    end: Optional[str] = None,
    api_key_env: str = "FRED_API_KEY",
) -> pd.DataFrame:
    """
    Fetch multiple FRED series and return a single DataFrame indexed by datetime with columns per series id.
    Requires fredapi with API key in environment variable specified by `api_key_env`.
    """
    try:
        from fredapi import Fred
    except ImportError as e:
        raise ImportError("fredapi is required. Install with `pip install fredapi`. ") from e

    api_key = os.environ.get(api_key_env)
    if not api_key:
        raise EnvironmentError(f"Set {api_key_env} environment variable with your FRED API key.")

    fred = Fred(api_key=api_key)

    if start is None:
        start = "1990-01-01"
    if end is None:
        end = datetime.today().strftime("%Y-%m-%d")

    frames: List[pd.Series] = []
    for sid in series_ids:
        s = fred.get_series(sid, observation_start=start, observation_end=end)
        if s is None or len(s) == 0:
            ser = pd.Series(dtype=float, name=sid)
        else:
            ser = pd.Series(s, name=sid)
        frames.append(ser)

    df = pd.concat(frames, axis=1)
    df.index = pd.to_datetime(df.index)
    return df


def fetch_fundamentals(symbols: List[str]) -> pd.DataFrame:
    """
    Fetch fundamental metrics for given symbols using yfinance.
    Returns DataFrame with columns: symbol, sector, pb_ratio, roe, roa, market_cap, pe_ratio
    """
    try:
        import yfinance as yf
    except ImportError as e:
        raise ImportError("yfinance is required. Install with `pip install yfinance`. ") from e
    
    import time
    
    results = []
    for i, sym in enumerate(symbols):
        try:
            # Add delay to avoid rate limiting (wait 0.5 seconds between requests)
            if i > 0:
                time.sleep(0.5)
            
            ticker = yf.Ticker(sym)
            info = ticker.info
            
            # Extract key fundamentals
            row = {
                'symbol': sym,
                'sector': info.get('sector', 'Unknown'),
                'industry': info.get('industry', 'Unknown'),
                'market_cap': info.get('marketCap', None),
                'pb_ratio': info.get('priceToBook', None),
                'pe_ratio': info.get('trailingPE', None),
                'roe': info.get('returnOnEquity', None),
                'roa': info.get('returnOnAssets', None),
                'profit_margin': info.get('profitMargins', None),
                'debt_to_equity': info.get('debtToEquity', None),
                'current_ratio': info.get('currentRatio', None),
            }
            results.append(row)
        except Exception as e:
            print(f"⚠️ Could not fetch fundamentals for {sym}: {e}")
            results.append({
                'symbol': sym,
                'sector': 'Unknown',
                'industry': 'Unknown',
                'market_cap': None,
                'pb_ratio': None,
                'pe_ratio': None,
                'roe': None,
                'roa': None,
                'profit_margin': None,
                'debt_to_equity': None,
                'current_ratio': None,
            })
    
    return pd.DataFrame(results)


