"""
VECM (Vector Error Correction Model) Analyzer for cointegration and long-run equilibrium analysis.

Uses statsmodels VECM to test for cointegration among FRED macro series and asset returns,
then reports cointegration rank, adjustment coefficients (alpha), and long-run relationships (beta).
"""

from __future__ import annotations

from typing import Optional, Dict, List
import numpy as np
import pandas as pd
from statsmodels.tsa.vector_ar.vecm import VECM, coint_johansen


class VECMAnalyzer:
    def __init__(self):
        self.data: Optional[pd.DataFrame] = None
        self.vecm_result = None
        self.johansen_result = None
        
    def load_data(self, data: pd.DataFrame) -> bool:
        """
        Load multivariate time series data for VECM analysis.
        data: DataFrame indexed by datetime with columns for each series.
        """
        try:
            if data.empty or len(data.columns) < 2:
                raise ValueError("VECM requires at least 2 series")
            self.data = data.dropna()
            return True
        except Exception as e:
            print(f"❌ Error loading VECM data: {e}")
            return False
    
    def test_cointegration(self, det_order: int = 0, k_ar_diff: int = 1) -> Dict:
        """
        Run Johansen cointegration test and return results.
        det_order: -1 (no trend), 0 (constant in coint), 1 (linear trend in coint)
        k_ar_diff: number of lagged differences in VECM
        Returns dict with rank, trace stats, and critical values.
        """
        if self.data is None or self.data.empty:
            raise ValueError("No data loaded")
        
        # Johansen test
        joh = coint_johansen(self.data.values, det_order=det_order, k_ar_diff=k_ar_diff)
        self.johansen_result = joh
        
        # Determine cointegration rank by comparing trace statistic to 95% critical value
        trace_stats = joh.lr1  # trace statistics
        crit_vals_95 = joh.cvt[:, 1]  # 95% critical values for trace test
        
        rank = 0
        for i in range(len(trace_stats)):
            if trace_stats[i] > crit_vals_95[i]:
                rank = i + 1
            else:
                break
        
        result = {
            'rank': rank,
            'trace_stats': trace_stats.tolist(),
            'critical_values_95': crit_vals_95.tolist(),
            'max_eigen_stats': joh.lr2.tolist(),
            'series_names': list(self.data.columns)
        }
        return result
    
    def fit_vecm(self, rank: Optional[int] = None, k_ar_diff: int = 1, det_order: int = 0) -> Dict:
        """
        Fit VECM model with specified cointegration rank.
        If rank is None, auto-detect using Johansen test.
        Returns dict with alpha (adjustment), beta (cointegration vectors), and summary.
        """
        if self.data is None or self.data.empty:
            raise ValueError("No data loaded")
        
        if rank is None:
            coint_res = self.test_cointegration(det_order=det_order, k_ar_diff=k_ar_diff)
            rank = coint_res['rank']
            if rank == 0:
                print("⚠️ No cointegration detected. Setting rank=1 for demonstration.")
                rank = 1
        
        # Fit VECM
        vecm_model = VECM(self.data, k_ar_diff=k_ar_diff, coint_rank=rank, deterministic='ci')
        self.vecm_result = vecm_model.fit()
        
        # Extract key components
        alpha = self.vecm_result.alpha  # adjustment coefficients (n_series x rank)
        beta = self.vecm_result.beta    # cointegration vectors (n_series x rank)
        
        result = {
            'rank': rank,
            'alpha': alpha,
            'beta': beta,
            'series_names': list(self.data.columns),
            'summary': str(self.vecm_result.summary())
        }
        return result
    
    def format_vecm_report(self, vecm_result: Dict) -> str:
        """Format VECM results into a readable report for agents."""
        rank = vecm_result['rank']
        alpha = vecm_result['alpha']
        beta = vecm_result['beta']
        series_names = vecm_result['series_names']
        
        report = f"VECM Analysis Results\n{'='*60}\n"
        report += f"Cointegration Rank: {rank}\n"
        report += f"Series: {', '.join(series_names)}\n\n"
        
        report += "Cointegration Vectors (Beta - Long-run relationships):\n"
        beta_df = pd.DataFrame(beta, index=series_names, columns=[f'CV{i+1}' for i in range(rank)])
        report += beta_df.to_string() + "\n\n"
        
        report += "Adjustment Coefficients (Alpha - Speed of adjustment to equilibrium):\n"
        alpha_df = pd.DataFrame(alpha, index=series_names, columns=[f'CV{i+1}' for i in range(rank)])
        report += alpha_df.to_string() + "\n"
        
        return report
    
    @staticmethod
    def format_cointegration_test(coint_result: Dict) -> str:
        """Format Johansen cointegration test results."""
        report = f"Johansen Cointegration Test\n{'='*60}\n"
        report += f"Series: {', '.join(coint_result['series_names'])}\n"
        report += f"Detected Cointegration Rank: {coint_result['rank']}\n\n"
        
        report += "Trace Statistics vs 95% Critical Values:\n"
        for i, (trace, crit) in enumerate(zip(coint_result['trace_stats'], coint_result['critical_values_95'])):
            sig = "***" if trace > crit else ""
            report += f"  r ≤ {i}: Trace={trace:.2f}, Crit={crit:.2f} {sig}\n"
        
        return report




