"""
Macro VAR and Granger Causality Analyzer
Loads a macro CSV with columns ['CPI','Unemployment','10Y_Treasury','FedFundsRate','IP_Index'],
aligns with asset returns, fits a VAR, and reports which variables Granger-cause returns.
Outputs a concise table: variable, p_value, direction, strength.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
from typing import Optional, List
from statsmodels.tsa.api import VAR


REQUIRED_COLS = ['CPI', 'Unemployment', '10Y_Treasury', 'FedFundsRate', 'IP_Index']


class MacroVARAnalyzer:
    def __init__(self):
        self.macro_df: Optional[pd.DataFrame] = None
        self.date_column: Optional[str] = None

    def load_macro_csv(self, file_path: str, date_column: Optional[str] = None) -> bool:
        try:
            try:
                df = pd.read_csv(file_path)
            except Exception:
                df = pd.read_csv(file_path, skiprows=1)

            if date_column is None:
                date_column = self._detect_date_column(df)

            df[date_column] = pd.to_datetime(df[date_column], errors='coerce')
            df = df.dropna(subset=[date_column])
            df = df.sort_values(by=date_column).set_index(date_column)

            # Normalize column names to match REQUIRED_COLS case-insensitively
            colmap = {c: c for c in df.columns}
            for req in REQUIRED_COLS:
                for c in df.columns:
                    if c.lower() == req.lower():
                        colmap[c] = req
                        break
            df = df.rename(columns=colmap)

            missing = [c for c in REQUIRED_COLS if c not in df.columns]
            if missing:
                raise ValueError(f"Missing required macro columns: {missing}")

            self.macro_df = df[REQUIRED_COLS].astype(float)
            self.date_column = date_column
            return True
        except Exception as e:
            print(f"❌ Error loading macro CSV: {e}")
            return False

    def _detect_date_column(self, df: pd.DataFrame) -> str:
        date_keywords = ['date', 'time', 'timestamp', 'month', 'year', 'period']
        for col in df.columns:
            if any(k in col.lower() for k in date_keywords):
                return col
        return df.columns[0]

    def analyze(self, returns: pd.Series, maxlags: int = 6) -> pd.DataFrame:
        """
        Align macro data with returns (index must be datetime), fit VAR,
        and test Granger causality of each macro variable on returns.
        Strength is |corr(returns, macro_lag1)| and direction is sign of that corr.
        """
        if self.macro_df is None:
            raise ValueError("Macro data not loaded")

        # Ensure index is datetime and align
        r = returns.copy()
        r.index = pd.to_datetime(r.index)
        df = pd.concat([r.rename('returns'), self.macro_df], axis=1).dropna()

        # Fit VAR with automatic lag selection up to maxlags
        model = VAR(df)
        try:
            sel = model.select_order(maxlags=maxlags)
            k_ar = int(sel.aic or sel.fpe or sel.hqic or sel.bic)
            if k_ar <= 0:
                k_ar = 1
        except Exception:
            k_ar = 1

        res = model.fit(k_ar)

        rows = []
        for var in REQUIRED_COLS:
            try:
                test = res.test_causality('returns', [var], kind='f')
                pval = float(test.pvalue)
            except Exception:
                pval = np.nan

            # Direction/strength via lag-1 correlation
            macro_lag = df[var].shift(1)
            aligned = pd.concat([df['returns'], macro_lag], axis=1).dropna()
            if len(aligned) > 2:
                corr = aligned.corr().iloc[0, 1]
            else:
                corr = np.nan

            direction = 'pos' if pd.notna(corr) and corr >= 0 else 'neg'
            strength = float(abs(corr)) if pd.notna(corr) else np.nan

            rows.append({'variable': var, 'p_value': pval, 'direction': direction, 'strength': strength})

        table = pd.DataFrame(rows).sort_values(by='p_value', na_position='last')
        return table

    @staticmethod
    def format_table(table: pd.DataFrame) -> str:
        # concise string table
        return table.to_string(index=False, float_format=lambda x: f"{x:.4f}")


