"""
Technical Indicator Forecaster (non-ARIMA)
Builds a feature set of technical indicators and trains a ML model with
walk-forward validation to produce 1-day and 1-week ahead forecasts.
Saves metrics (MSE/MAE) and plots with overlays of indicators.
"""

import os
from datetime import timedelta
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error


class IndicatorForecaster:
    """
    Forecast close prices using technical indicators and RandomForest with
    walk-forward validation. Produces 1D and 1W ahead predictions.
    """

    def __init__(self, n_estimators: int = 200, random_state: int = 42):
        self.data = None
        self.date_column = None
        self.value_column = None
        self.features = None
        self.model_1d = RandomForestRegressor(
            n_estimators=n_estimators, random_state=random_state
        )
        self.model_1w = RandomForestRegressor(
            n_estimators=n_estimators, random_state=random_state
        )
        self.results = {}

    # ------------------ Data Loading ------------------
    def load_csv_data(self, file_path: str, date_column: str | None = None, value_column: str | None = None) -> bool:
        try:
            # Initial read
            try:
                df = pd.read_csv(file_path)
                # Handle potential title row as single column
                if len(df.columns) == 1 and df.columns[0].startswith(('Bitcoin', 'Stock', 'Data')):
                    print("⚠️  Detected title row, skipping first row...")
                    df = pd.read_csv(file_path, skiprows=1)
            except Exception as e:
                print(f"⚠️  Initial CSV read failed: {str(e)}")
                print("🔄 Trying to read with skiprows=1...")
                df = pd.read_csv(file_path, skiprows=1)

            # Detect columns if not provided
            print(f"📋 Available columns: {list(df.columns)}")
            if date_column is None:
                date_column = self._detect_date_column(df)
            if value_column is None:
                value_column = self._detect_value_column(df)

            print(f"🔍 Detected date column: {date_column}")
            print(f"🔍 Detected value column: {value_column}")

            # Parse dates robustly
            try:
                df[date_column] = pd.to_datetime(df[date_column])
            except Exception as e:
                print(f"⚠️  Date parsing failed for column '{date_column}': {str(e)}")
                print("🔄 Trying alternative date parsing with coercion...")
                df[date_column] = pd.to_datetime(df[date_column], errors='coerce')

            df = df.dropna(subset=[date_column])
            df = df.sort_values(by=date_column).set_index(date_column)

            # Ensure value column exists after processing
            if value_column not in df.columns:
                # Try to re-detect among remaining columns
                value_column = self._detect_value_column(df.reset_index())
                print(f"🔁 Re-detected value column: {value_column}")
                if value_column not in df.columns:
                    raise KeyError(f"Value column '{value_column}' not found in CSV after parsing")

            self.data = df
            self.date_column = date_column
            self.value_column = value_column
            return True
        except Exception as e:
            print(f"❌ Error loading CSV data: {str(e)}")
            return False

    def _detect_date_column(self, df: pd.DataFrame) -> str:
        date_keywords = ['date', 'time', 'timestamp', 'day', 'month', 'year', 'timeopen', 'timeclose']
        for col in df.columns:
            if any(k in col.lower() for k in date_keywords):
                return col
        return df.columns[0]

    def _detect_value_column(self, df: pd.DataFrame) -> str:
        value_keywords = ['close', 'price', 'value', 'open', 'high', 'low']
        # Prefer exact 'close'
        for col in df.columns:
            if col.lower() == 'close':
                return col
        for col in df.columns:
            if any(k in col.lower() for k in value_keywords) and 'time' not in col.lower():
                return col
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 0:
            return numeric_cols[-1]
        return df.columns[-1]

    # ------------------ Indicators ------------------
    @staticmethod
    def _rsi(series: pd.Series, period: int = 14) -> pd.Series:
        delta = series.diff()
        up = delta.clip(lower=0)
        down = -delta.clip(upper=0)
        roll_up = up.ewm(alpha=1/period, adjust=False).mean()
        roll_down = down.ewm(alpha=1/period, adjust=False).mean()
        rs = roll_up / (roll_down.replace(0, np.nan))
        rsi = 100 - (100 / (1 + rs))
        return rsi

    @staticmethod
    def _bollinger_bands(series: pd.Series, window: int = 20, num_std: float = 2.0):
        ma = series.rolling(window).mean()
        sd = series.rolling(window).std(ddof=0)
        upper = ma + num_std * sd
        lower = ma - num_std * sd
        width = upper - lower
        return ma, upper, lower, width

    @staticmethod
    def _ema(series: pd.Series, span: int) -> pd.Series:
        return series.ewm(span=span, adjust=False).mean()

    def _macd(self, series: pd.Series, fast: int = 12, slow: int = 26, signal: int = 9):
        ema_fast = self._ema(series, fast)
        ema_slow = self._ema(series, slow)
        macd_line = ema_fast - ema_slow
        signal_line = macd_line.ewm(span=signal, adjust=False).mean()
        hist = macd_line - signal_line
        return macd_line, signal_line, hist

    @staticmethod
    def _realized_vol(series: pd.Series, window: int = 20) -> pd.Series:
        returns = np.log(series).diff()
        return returns.rolling(window).std(ddof=0) * np.sqrt(252)

    def _build_features(self) -> pd.DataFrame:
        close = self.data[self.value_column].astype(float)
        df = pd.DataFrame(index=self.data.index)
        df['close'] = close

        # Indicators
        df['rsi_14'] = self._rsi(close, 14)
        ma, bb_u, bb_l, bb_w = self._bollinger_bands(close, 20, 2.0)
        df['bb_ma_20'] = ma
        df['bb_upper_20'] = bb_u
        df['bb_lower_20'] = bb_l
        df['bb_width_20'] = bb_w
        macd, macd_sig, macd_hist = self._macd(close)
        df['macd'] = macd
        df['macd_signal'] = macd_sig
        df['macd_hist'] = macd_hist
        df['rv_20'] = self._realized_vol(close, 20)

        # Lags and returns
        df['ret_1'] = close.pct_change(1)
        df['ret_5'] = close.pct_change(5)
        df['lag_1'] = close.shift(1)
        df['lag_5'] = close.shift(5)

        # Targets
        df['target_1d'] = close.shift(-1)
        df['target_1w'] = close.shift(-7)

        df = df.dropna()
        self.features = df
        return df

    # ------------------ Walk-forward ------------------
    def walk_forward_validate(
        self,
        min_train_size: int | None = None,
        step_size: int = 5,
        retrain_every: int = 5,
        max_steps: int | None = 200,
        verbose: bool = True,
    ):
        if self.features is None:
            self._build_features()

        df = self.features.copy()
        feature_cols = [c for c in df.columns if c not in ['target_1d', 'target_1w']]

        if min_train_size is None:
            min_train_size = max(252, int(len(df) * 0.5))

        preds_1d, truth_1d, dates_1d = [], [], []
        preds_1w, truth_1w, dates_1w = [], [], []

        rng = list(range(min_train_size, len(df) - 1, step_size))
        if max_steps is not None:
            rng = rng[:max_steps]

        for i, end_idx in enumerate(rng, start=1):
            train = df.iloc[:end_idx]
            test_row_next = df.iloc[end_idx]  # for 1D target

            X_train = train[feature_cols]
            y1_train = train['target_1d']
            y7_train = train['target_1w']

            # Fit models periodically to speed up
            if i == 1 or (retrain_every and i % retrain_every == 0):
                self.model_1d.fit(X_train, y1_train)
                self.model_1w.fit(X_train, y7_train)

            # Predict 1D ahead at end_idx
            x_next = pd.DataFrame([test_row_next[feature_cols]], columns=feature_cols)
            p1 = self.model_1d.predict(x_next)[0]
            t1 = test_row_next['target_1d']
            preds_1d.append(p1)
            truth_1d.append(t1)
            dates_1d.append(df.index[end_idx])

            # For 1W ahead, verify target availability
            if not np.isnan(test_row_next['target_1w']):
                p7 = self.model_1w.predict(x_next)[0]
                t7 = test_row_next['target_1w']
                preds_1w.append(p7)
                truth_1w.append(t7)
                dates_1w.append(df.index[end_idx])

            if verbose and (i % max(1, len(rng)//10) == 0):
                print(f"... walk-forward progress: {i}/{len(rng)} steps")

        # Metrics
        mse_1d = mean_squared_error(truth_1d, preds_1d) if preds_1d else np.nan
        mae_1d = mean_absolute_error(truth_1d, preds_1d) if preds_1d else np.nan
        mse_1w = mean_squared_error(truth_1w, preds_1w) if preds_1w else np.nan
        mae_1w = mean_absolute_error(truth_1w, preds_1w) if preds_1w else np.nan

        self.results['walk_forward'] = {
            'dates_1d': pd.Index(dates_1d),
            'preds_1d': np.array(preds_1d),
            'truth_1d': np.array(truth_1d),
            'mse_1d': float(mse_1d),
            'mae_1d': float(mae_1d),
            'dates_1w': pd.Index(dates_1w),
            'preds_1w': np.array(preds_1w),
            'truth_1w': np.array(truth_1w),
            'mse_1w': float(mse_1w),
            'mae_1w': float(mae_1w),
        }

        return self.results['walk_forward']

    # ------------------ Refit and Forecast ------------------
    def forecast_ahead(self, periods_1d: int = 1, periods_1w: int = 7):
        if self.features is None:
            self._build_features()

        df = self.features.copy()
        feature_cols = [c for c in df.columns if c not in ['target_1d', 'target_1w']]

        # Fit on all available history
        X_all = df[feature_cols]
        y1_all = df['target_1d']
        y7_all = df['target_1w']
        self.model_1d.fit(X_all, y1_all)
        self.model_1w.fit(X_all, y7_all)

        # One-step-ahead using last row features
        last_row = pd.DataFrame([df.iloc[-1][feature_cols]], columns=feature_cols)
        pred_1d_next = self.model_1d.predict(last_row)[0]
        pred_1w_next = self.model_1w.predict(last_row)[0]

        # Build forecast dates
        last_date = df.index[-1]
        dates_1d = pd.date_range(start=last_date + timedelta(days=1), periods=periods_1d, freq='D')
        dates_1w = pd.date_range(start=last_date + timedelta(days=1), periods=periods_1w, freq='D')

        self.results['forecast'] = {
            'dates_1d': dates_1d,
            'pred_1d': np.array([pred_1d_next] * periods_1d),
            'dates_1w': dates_1w,
            'pred_1w': np.array([pred_1w_next] * periods_1w),
        }

        return self.results['forecast']

    # ------------------ Plotting ------------------
    def save_plots(self, filename_prefix: str = 'indicator_forecast') -> str:
        if self.features is None:
            self._build_features()
        df = self.features.copy()

        # Plot 1: Price with predictions and Bollinger Bands
        plt.figure(figsize=(14, 8))
        plt.plot(df.index, df['close'], label='Close', color='black', linewidth=1.5)
        plt.plot(df.index, df['bb_ma_20'], label='BB MA(20)', color='blue', alpha=0.8)
        plt.fill_between(df.index, df['bb_lower_20'], df['bb_upper_20'], color='blue', alpha=0.1, label='BBands')

        if 'walk_forward' in self.results and len(self.results['walk_forward']['preds_1d']) > 0:
            wf = self.results['walk_forward']
            plt.plot(wf['dates_1d'], wf['preds_1d'], label='Pred 1D (walk-forward)', color='green')
            plt.plot(wf['dates_1w'], wf['preds_1w'], label='Pred 1W (walk-forward)', color='orange', alpha=0.8)

        if 'forecast' in self.results:
            fc = self.results['forecast']
            plt.scatter(fc['dates_1d'], fc['pred_1d'], label='Forecast next 1D', color='green', marker='x')
            plt.scatter(fc['dates_1w'], fc['pred_1w'], label='Forecast next 1W', color='orange', marker='x')

        plt.title('Close Price with Predictions and Bollinger Bands')
        plt.xlabel('Date')
        plt.ylabel('Price')
        plt.legend()
        plt.grid(alpha=0.3)
        plt.tight_layout()
        out1 = f"{filename_prefix}_price.png"
        plt.savefig(out1, dpi=300, bbox_inches='tight')
        plt.close()

        # Plot 2: RSI and MACD panels
        fig, axes = plt.subplots(2, 1, figsize=(14, 8), sharex=True)

        axes[0].plot(df.index, df['rsi_14'], label='RSI(14)', color='purple')
        axes[0].axhline(70, color='red', linestyle='--', alpha=0.5)
        axes[0].axhline(30, color='green', linestyle='--', alpha=0.5)
        axes[0].set_ylabel('RSI')
        axes[0].legend(); axes[0].grid(alpha=0.3)

        axes[1].plot(df.index, df['macd'], label='MACD', color='brown')
        axes[1].plot(df.index, df['macd_signal'], label='Signal', color='grey')
        axes[1].bar(df.index, df['macd_hist'], label='Hist', color='teal', alpha=0.3)
        axes[1].set_ylabel('MACD')
        axes[1].legend(); axes[1].grid(alpha=0.3)

        plt.xlabel('Date')
        plt.tight_layout()
        out2 = f"{filename_prefix}_indicators.png"
        plt.savefig(out2, dpi=300, bbox_inches='tight')
        plt.close()

        return out1


def run_example(csv_path: str = 'sample_stock_data.csv', date_column: str | None = None, value_column: str | None = None):
    forecaster = IndicatorForecaster()
    assert forecaster.load_csv_data(csv_path, date_column, value_column)
    forecaster._build_features()

    wf = forecaster.walk_forward_validate()
    print(f"1D-ahead -> MSE: {wf['mse_1d']:.4f}, MAE: {wf['mae_1d']:.4f}")
    print(f"1W-ahead -> MSE: {wf['mse_1w']:.4f}, MAE: {wf['mae_1w']:.4f}")

    forecaster.forecast_ahead(periods_1d=1, periods_1w=7)
    out = forecaster.save_plots()
    print(f"Saved plots to: {out} and *_indicators.png")


if __name__ == '__main__':
    # If the repo has a sample CSV, use it by default
    default_csv = 'sample_stock_data.csv'
    if os.path.exists(default_csv):
        run_example(default_csv)
    else:
        raise SystemExit('Please provide a CSV path to run the example.')


