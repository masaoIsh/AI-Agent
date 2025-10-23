"""
ARIMA Regime-Switching Forecaster
Detects volatility regimes and fits separate ARIMA models for each regime.
Uses rolling volatility to classify regimes (low/medium/high) and generates forecasts.
"""

from __future__ import annotations

from typing import Optional, Dict, Tuple
import numpy as np
import pandas as pd
import warnings


class ARIMARegimeSwitching:
    def __init__(self, vol_window: int = 20, vol_percentiles: Tuple[float, float] = (33, 67)):
        """
        Initialize ARIMA regime-switching forecaster.
        vol_window: Rolling window for volatility calculation
        vol_percentiles: Percentiles to define low/medium/high vol regimes (e.g., 33, 67)
        """
        self.vol_window = vol_window
        self.vol_percentiles = vol_percentiles
        self.data: Optional[pd.Series] = None
        self.regimes: Optional[pd.Series] = None
        self.models: Dict[str, any] = {}
        self.forecast_results: Dict = {}
    
    def load_data(self, price_series: pd.Series) -> bool:
        """Load price time series for analysis."""
        try:
            if price_series.empty:
                raise ValueError("Price series is empty")
            # Ensure it's a proper Series (not DataFrame) and convert to float
            if isinstance(price_series, pd.DataFrame):
                # If DataFrame, take the first column
                price_series = price_series.iloc[:, 0]
            
            # Create series with proper name (use existing name or default to 'price')
            series_name = price_series.name if price_series.name is not None else 'price'
            self.data = pd.Series(price_series.values, index=price_series.index, dtype=float, name=series_name)
            return True
        except Exception as e:
            print(f"❌ Error loading data: {e}")
            return False
    
    def detect_regimes(self) -> pd.Series:
        """
        Detect volatility regimes based on rolling standard deviation.
        Returns Series with regime labels: 'low_vol', 'medium_vol', 'high_vol'
        """
        if self.data is None or self.data.empty:
            raise ValueError("No data loaded")
        
        # Calculate rolling volatility (annualized)
        returns = self.data.pct_change().dropna()
        rolling_vol = returns.rolling(window=self.vol_window).std() * np.sqrt(252)
        
        # Define regime thresholds based on percentiles
        low_threshold = rolling_vol.quantile(self.vol_percentiles[0] / 100.0)
        high_threshold = rolling_vol.quantile(self.vol_percentiles[1] / 100.0)
        
        # Classify regimes - initialize with default value to avoid index issues
        regimes = pd.Series('unknown', index=rolling_vol.index, dtype=str)
        regimes.loc[rolling_vol <= low_threshold] = 'low_vol'
        regimes.loc[(rolling_vol > low_threshold) & (rolling_vol <= high_threshold)] = 'medium_vol'
        regimes.loc[rolling_vol > high_threshold] = 'high_vol'
        
        self.regimes = regimes
        return regimes
    
    def fit_regime_models(self, order: Tuple[int, int, int] = (2, 1, 2)) -> Dict:
        """
        Fit separate ARIMA models for each regime.
        order: ARIMA (p, d, q) order
        """
        try:
            from statsmodels.tsa.arima.model import ARIMA
        except ImportError as e:
            raise ImportError("statsmodels is required. Install with `pip install statsmodels`.") from e
        
        if self.regimes is None:
            self.detect_regimes()
        
        # Ensure data has a name for DataFrame column access
        data_col_name = self.data.name if self.data.name is not None else 'price'
        aligned_data = pd.concat([self.data.rename(data_col_name), self.regimes.rename('regime')], axis=1).dropna()
        
        results = {}
        for regime in ['low_vol', 'medium_vol', 'high_vol']:
            regime_data = aligned_data[aligned_data['regime'] == regime][data_col_name]
            
            if len(regime_data) < 20:
                print(f"⚠️ Insufficient data for regime '{regime}' ({len(regime_data)} obs), skipping.")
                results[regime] = None
                continue
            
            try:
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore")
                    model = ARIMA(regime_data, order=order)
                    fitted = model.fit()
                    self.models[regime] = fitted
                    results[regime] = {
                        'aic': fitted.aic,
                        'bic': fitted.bic,
                        'n_obs': len(regime_data),
                        'order': order
                    }
            except Exception as e:
                print(f"⚠️ Could not fit ARIMA for regime '{regime}': {e}")
                results[regime] = None
        
        return results
    
    def forecast(self, steps: int = 5, current_regime: Optional[str] = None) -> Dict:
        """
        Forecast future values using the appropriate regime model.
        If current_regime is None, uses the most recent regime detected.
        """
        if not self.models:
            raise ValueError("No models fitted. Call fit_regime_models() first.")
        
        if current_regime is None:
            if self.regimes is None or self.regimes.empty:
                raise ValueError("No regimes detected")
            current_regime = self.regimes.iloc[-1]
        
        if current_regime not in self.models or self.models[current_regime] is None:
            print(f"⚠️ No model available for regime '{current_regime}', using fallback.")
            # Fallback to first available model
            for reg in ['medium_vol', 'low_vol', 'high_vol']:
                if reg in self.models and self.models[reg] is not None:
                    current_regime = reg
                    break
        
        model = self.models.get(current_regime)
        if model is None:
            raise ValueError(f"No valid model available for forecasting")
        
        try:
            forecast_result = model.forecast(steps=steps)
            conf_int = model.get_forecast(steps=steps).conf_int(alpha=0.05)
            
            self.forecast_results = {
                'regime': current_regime,
                'forecast': forecast_result.values if hasattr(forecast_result, 'values') else forecast_result,
                'conf_int_lower': conf_int.iloc[:, 0].values if hasattr(conf_int, 'iloc') else None,
                'conf_int_upper': conf_int.iloc[:, 1].values if hasattr(conf_int, 'iloc') else None,
                'steps': steps
            }
            return self.forecast_results
        except Exception as e:
            print(f"❌ Forecast failed: {e}")
            return {}
    
    def format_report(self) -> str:
        """Format regime-switching analysis into a report for agents."""
        if self.regimes is None:
            return "No regime analysis available."
        
        report = "ARIMA Regime-Switching Analysis\n"
        report += "=" * 80 + "\n"
        
        # Regime distribution
        regime_counts = self.regimes.value_counts()
        total = len(self.regimes)
        report += "Regime Distribution:\n"
        for regime, count in regime_counts.items():
            pct = (count / total) * 100
            report += f"  {regime}: {count} periods ({pct:.1f}%)\n"
        
        report += f"\nCurrent Regime: {self.regimes.iloc[-1]}\n\n"
        
        # Model summaries
        report += "Fitted ARIMA Models by Regime:\n"
        for regime in ['low_vol', 'medium_vol', 'high_vol']:
            if regime in self.models and self.models[regime] is not None:
                model = self.models[regime]
                report += f"  {regime}: AIC={model.aic:.2f}, BIC={model.bic:.2f}\n"
            else:
                report += f"  {regime}: No model fitted\n"
        
        # Forecast
        if self.forecast_results:
            report += "\nForecast Results:\n"
            report += f"  Regime: {self.forecast_results['regime']}\n"
            forecast_vals = self.forecast_results.get('forecast', [])
            for i, val in enumerate(forecast_vals, 1):
                lower = self.forecast_results.get('conf_int_lower', [None] * len(forecast_vals))[i-1]
                upper = self.forecast_results.get('conf_int_upper', [None] * len(forecast_vals))[i-1]
                if lower is not None and upper is not None:
                    report += f"  Step {i}: {val:.4f} (95% CI: [{lower:.4f}, {upper:.4f}])\n"
                else:
                    report += f"  Step {i}: {val:.4f}\n"
        
        return report
    
    def get_regime_metrics(self) -> pd.DataFrame:
        """Get summary metrics for each regime."""
        if self.regimes is None or self.data is None:
            return pd.DataFrame()
        
        aligned = pd.concat([self.data, self.regimes.rename('regime')], axis=1).dropna()
        
        metrics = []
        for regime in ['low_vol', 'medium_vol', 'high_vol']:
            regime_data = aligned[aligned['regime'] == regime][self.data.name]
            if len(regime_data) > 0:
                returns = regime_data.pct_change().dropna()
                metrics.append({
                    'regime': regime,
                    'n_obs': len(regime_data),
                    'mean_price': regime_data.mean(),
                    'std_price': regime_data.std(),
                    'mean_return': returns.mean(),
                    'volatility': returns.std() * np.sqrt(252)
                })
        
        return pd.DataFrame(metrics)


def run_example():
    """Example usage of ARIMA regime-switching."""
    # Generate synthetic data with regime changes
    np.random.seed(42)
    n = 500
    
    # Low vol regime
    low_vol = np.random.normal(100, 2, 200).cumsum() + 100
    # High vol regime
    high_vol = np.random.normal(0, 5, 200).cumsum() + low_vol[-1]
    # Medium vol regime
    med_vol = np.random.normal(0, 3, 100).cumsum() + high_vol[-1]
    
    prices = np.concatenate([low_vol, high_vol, med_vol])
    dates = pd.date_range('2020-01-01', periods=len(prices), freq='D')
    price_series = pd.Series(prices, index=dates, name='price')
    
    # Run analysis
    ars = ARIMARegimeSwitching()
    ars.load_data(price_series)
    regimes = ars.detect_regimes()
    print(ars.get_regime_metrics())
    
    models = ars.fit_regime_models(order=(2, 1, 2))
    forecast = ars.forecast(steps=5)
    print(ars.format_report())


if __name__ == '__main__':
    run_example()

