"""
ARIMA Forecasting Module for Financial Time Series Analysis
Provides Yugo_Valuation_Agent with advanced time series forecasting capabilities
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.stattools import adfuller
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.seasonal import seasonal_decompose
import warnings
from datetime import datetime, timedelta
import os

warnings.filterwarnings('ignore')

class ARIMAForecaster:
    """
    Advanced ARIMA forecasting class for financial time series analysis
    """
    
    def __init__(self):
        self.data = None
        self.model = None
        self.forecast_results = None
        self.diagnostics = {}
        
    def load_csv_data(self, file_path, date_column=None, value_column=None):
        """
        Load time series data from CSV file
        
        Args:
            file_path (str): Path to CSV file
            date_column (str): Name of date column (auto-detected if None)
            value_column (str): Name of value column (auto-detected if None)
        """
        try:
            # Load the CSV file with better error handling
            try:
                self.data = pd.read_csv(file_path)
                # Check if the first column looks like a title rather than data
                if len(self.data.columns) == 1 and self.data.columns[0].startswith(('Bitcoin', 'Stock', 'Data')):
                    print("⚠️  Detected title row, skipping first row...")
                    self.data = pd.read_csv(file_path, skiprows=1)
            except Exception as e:
                # Try reading with skiprows=1 in case there's a malformed header
                print(f"⚠️  Initial CSV read failed: {str(e)}")
                print("🔄 Trying to read with skiprows=1...")
                self.data = pd.read_csv(file_path, skiprows=1)
            
            # Auto-detect date and value columns if not specified
            print(f"📋 Available columns: {list(self.data.columns)}")
            if date_column is None:
                date_column = self._detect_date_column()
            if value_column is None:
                value_column = self._detect_value_column()
            
            print(f"🔍 Detected date column: {date_column}")
            print(f"🔍 Detected value column: {value_column}")
            
            # Convert date column to datetime with better error handling
            try:
                self.data[date_column] = pd.to_datetime(self.data[date_column])
            except Exception as e:
                print(f"⚠️  Date parsing failed for column '{date_column}': {str(e)}")
                print("🔄 Trying alternative date parsing...")
                # Try parsing with different formats
                try:
                    self.data[date_column] = pd.to_datetime(self.data[date_column], errors='coerce')
                except:
                    print(f"❌ Could not parse date column '{date_column}'")
                    return False
            
            # Set date as index and sort
            self.data = self.data.set_index(date_column).sort_index()
            
            # Store column names
            self.date_column = date_column
            self.value_column = value_column
            
            # Extract the time series
            self.time_series = self.data[value_column].dropna()
            
            print(f"✅ Successfully loaded {len(self.time_series)} data points")
            print(f"📅 Date range: {self.time_series.index.min()} to {self.time_series.index.max()}")
            print(f"📊 Value column: {value_column}")
            
            return True
            
        except Exception as e:
            print(f"❌ Error loading CSV file: {str(e)}")
            return False
    
    def _detect_date_column(self):
        """Auto-detect date column from CSV"""
        date_keywords = ['date', 'time', 'timestamp', 'day', 'month', 'year', 'timeopen', 'timeclose']
        for col in self.data.columns:
            if any(keyword in col.lower() for keyword in date_keywords):
                return col
        
        # If no date column found, return first column
        return self.data.columns[0]
    
    def _detect_value_column(self):
        """Auto-detect value column from CSV"""
        # Look for common financial data columns, prioritizing close price
        value_keywords = ['close', 'price', 'value', 'open', 'high', 'low', 'volume', 'amount']
        
        # First, try to find 'close' specifically
        for col in self.data.columns:
            if col.lower() == 'close':
                return col
        
        # Then try other value keywords
        for keyword in value_keywords:
            for col in self.data.columns:
                if keyword in col.lower() and 'time' not in col.lower():
                    return col
        
        # If no value column found, return last numeric column
        numeric_cols = self.data.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 0:
            return numeric_cols[-1]
        
        return self.data.columns[-1]
    
    def check_stationarity(self):
        """Check if the time series is stationary using Augmented Dickey-Fuller test"""
        try:
            result = adfuller(self.time_series)
            
            self.diagnostics['adf_statistic'] = result[0]
            self.diagnostics['adf_pvalue'] = result[1]
            self.diagnostics['adf_critical_values'] = result[4]
            self.diagnostics['is_stationary'] = result[1] < 0.05
            
            print(f"📊 Stationarity Test Results:")
            print(f"   ADF Statistic: {result[0]:.4f}")
            print(f"   p-value: {result[1]:.4f}")
            print(f"   Stationary: {'Yes' if result[1] < 0.05 else 'No'}")
            
            return result[1] < 0.05
            
        except Exception as e:
            print(f"❌ Error checking stationarity: {str(e)}")
            return False
    
    def make_stationary(self):
        """Make the time series stationary using differencing"""
        try:
            # Try first difference
            diff_series = self.time_series.diff().dropna()
            
            # Check if first difference is stationary
            result = adfuller(diff_series)
            
            if result[1] < 0.05:
                self.time_series = diff_series
                self.diagnostics['differencing'] = 1
                print("✅ Series made stationary with first difference")
                return True
            else:
                # Try second difference
                diff2_series = diff_series.diff().dropna()
                result2 = adfuller(diff2_series)
                
                if result2[1] < 0.05:
                    self.time_series = diff2_series
                    self.diagnostics['differencing'] = 2
                    print("✅ Series made stationary with second difference")
                    return True
                else:
                    print("⚠️  Series may still not be fully stationary")
                    self.time_series = diff_series
                    self.diagnostics['differencing'] = 1
                    return False
                    
        except Exception as e:
            print(f"❌ Error making series stationary: {str(e)}")
            return False
    
    def find_optimal_arima_params(self, max_p=5, max_d=2, max_q=5):
        """Find optimal ARIMA parameters using AIC"""
        try:
            best_aic = float('inf')
            best_params = None
            
            print("🔍 Searching for optimal ARIMA parameters...")
            
            for p in range(max_p + 1):
                for d in range(max_d + 1):
                    for q in range(max_q + 1):
                        try:
                            model = ARIMA(self.time_series, order=(p, d, q))
                            fitted_model = model.fit()
                            
                            if fitted_model.aic < best_aic:
                                best_aic = fitted_model.aic
                                best_params = (p, d, q)
                                
                        except:
                            continue
            
            self.diagnostics['optimal_params'] = best_params
            self.diagnostics['best_aic'] = best_aic
            
            print(f"✅ Optimal ARIMA parameters: {best_params}")
            print(f"📊 Best AIC: {best_aic:.2f}")
            
            return best_params
            
        except Exception as e:
            print(f"❌ Error finding optimal parameters: {str(e)}")
            return (1, 1, 1)  # Default fallback
    
    def fit_arima_model(self, order=None):
        """Fit ARIMA model to the time series"""
        try:
            if order is None:
                order = self.find_optimal_arima_params()
            
            print(f"🔧 Fitting ARIMA{order} model...")
            
            self.model = ARIMA(self.time_series, order=order)
            self.fitted_model = self.model.fit()
            
            print("✅ ARIMA model fitted successfully")
            print(f"📊 Model Summary:")
            print(f"   AIC: {self.fitted_model.aic:.2f}")
            print(f"   BIC: {self.fitted_model.bic:.2f}")
            print(f"   Log Likelihood: {self.fitted_model.llf:.2f}")
            
            return True
            
        except Exception as e:
            print(f"❌ Error fitting ARIMA model: {str(e)}")
            return False
    
    def forecast(self, periods=30, confidence_level=0.95):
        """Generate forecasts using the fitted ARIMA model"""
        try:
            if self.fitted_model is None:
                print("❌ No model fitted. Please fit a model first.")
                return None
            
            print(f"🔮 Generating {periods}-period forecast...")
            
            # Generate forecast
            forecast_result = self.fitted_model.get_forecast(steps=periods)
            forecast_mean = forecast_result.predicted_mean
            forecast_ci = forecast_result.conf_int()
            
            # Create forecast dates
            last_date = self.time_series.index[-1]
            forecast_dates = pd.date_range(
                start=last_date + timedelta(days=1),
                periods=periods,
                freq='D'
            )
            
            # Store results
            self.forecast_results = {
                'forecast_dates': forecast_dates,
                'forecast_values': forecast_mean,
                'confidence_interval': forecast_ci,
                'confidence_level': confidence_level,
                'periods': periods
            }
            
            print(f"✅ Forecast generated for {periods} periods")
            print(f"📅 Forecast period: {forecast_dates[0]} to {forecast_dates[-1]}")
            
            return self.forecast_results
            
        except Exception as e:
            print(f"❌ Error generating forecast: {str(e)}")
            return None
    
    def generate_analysis_report(self):
        """Generate comprehensive analysis report"""
        if self.forecast_results is None:
            return "No forecast available. Please generate forecast first."
        
        report = []
        report.append("=" * 60)
        report.append("📈 ARIMA FORECASTING ANALYSIS REPORT")
        report.append("=" * 60)
        
        # Data summary
        report.append(f"\n📊 DATA SUMMARY:")
        report.append(f"   Total data points: {len(self.time_series)}")
        report.append(f"   Date range: {self.time_series.index.min()} to {self.time_series.index.max()}")
        report.append(f"   Mean value: {self.time_series.mean():.4f}")
        report.append(f"   Standard deviation: {self.time_series.std():.4f}")
        
        # Model diagnostics
        if 'optimal_params' in self.diagnostics:
            report.append(f"\n🔧 MODEL PARAMETERS:")
            report.append(f"   ARIMA order: {self.diagnostics['optimal_params']}")
            report.append(f"   AIC: {self.diagnostics.get('best_aic', 'N/A'):.2f}")
        
        if self.fitted_model:
            report.append(f"\n📈 MODEL PERFORMANCE:")
            report.append(f"   AIC: {self.fitted_model.aic:.2f}")
            report.append(f"   BIC: {self.fitted_model.bic:.2f}")
            report.append(f"   Log Likelihood: {self.fitted_model.llf:.2f}")
        
        # Forecast summary
        forecast_values = self.forecast_results['forecast_values']
        report.append(f"\n🔮 FORECAST SUMMARY:")
        report.append(f"   Forecast periods: {len(forecast_values)}")
        report.append(f"   Mean forecast value: {forecast_values.mean():.4f}")
        report.append(f"   Forecast range: {forecast_values.min():.4f} to {forecast_values.max():.4f}")
        
        # Trend analysis
        if len(forecast_values) > 1:
            trend = forecast_values.iloc[-1] - forecast_values.iloc[0]
            trend_pct = (trend / forecast_values.iloc[0]) * 100
            report.append(f"   Overall trend: {trend:+.4f} ({trend_pct:+.2f}%)")
        
        # Confidence intervals
        ci = self.forecast_results['confidence_interval']
        report.append(f"\n📊 CONFIDENCE INTERVALS ({self.forecast_results['confidence_level']*100:.0f}%):")
        report.append(f"   Lower bound: {ci.iloc[:, 0].mean():.4f}")
        report.append(f"   Upper bound: {ci.iloc[:, 1].mean():.4f}")
        
        # Recommendations
        report.append(f"\n💡 INVESTMENT INSIGHTS:")
        
        if len(forecast_values) > 1:
            short_term = forecast_values.iloc[:5].mean()
            long_term = forecast_values.iloc[-5:].mean()
            
            if long_term > short_term:
                report.append("   📈 Positive trend expected over forecast horizon")
            elif long_term < short_term:
                report.append("   📉 Negative trend expected over forecast horizon")
            else:
                report.append("   ➡️  Stable trend expected over forecast horizon")
        
        # Risk assessment
        volatility = forecast_values.std()
        report.append(f"   ⚠️  Forecast volatility: {volatility:.4f}")
        
        if volatility > self.time_series.std():
            report.append("   🔴 Higher volatility expected in forecast period")
        else:
            report.append("   🟢 Lower volatility expected in forecast period")
        
        report.append("\n" + "=" * 60)
        
        return "\n".join(report)
    
    def save_forecast_plot(self, filename="arima_forecast.png"):
        """Save forecast plot to file"""
        try:
            if self.forecast_results is None:
                print("❌ No forecast available to plot")
                return False
            
            plt.figure(figsize=(12, 8))
            
            # Plot historical data
            plt.plot(self.time_series.index, self.time_series.values, 
                    label='Historical Data', color='blue', linewidth=2)
            
            # Plot forecast
            forecast_dates = self.forecast_results['forecast_dates']
            forecast_values = self.forecast_results['forecast_values']
            
            plt.plot(forecast_dates, forecast_values, 
                    label='ARIMA Forecast', color='red', linewidth=2)
            
            # Plot confidence intervals
            ci = self.forecast_results['confidence_interval']
            plt.fill_between(forecast_dates, 
                           ci.iloc[:, 0], ci.iloc[:, 1], 
                           alpha=0.3, color='red', 
                           label=f'{self.forecast_results["confidence_level"]*100:.0f}% Confidence Interval')
            
            plt.title('ARIMA Time Series Forecast', fontsize=16, fontweight='bold')
            plt.xlabel('Date', fontsize=12)
            plt.ylabel('Value', fontsize=12)
            plt.legend()
            plt.grid(True, alpha=0.3)
            plt.tight_layout()
            
            # Save plot
            plt.savefig(filename, dpi=300, bbox_inches='tight')
            plt.close()
            
            print(f"✅ Forecast plot saved as: {filename}")
            return True
            
        except Exception as e:
            print(f"❌ Error saving plot: {str(e)}")
            return False

def create_sample_data(filename="sample_stock_data.csv"):
    """Create sample stock data for testing"""
    try:
        # Generate sample data
        dates = pd.date_range(start='2020-01-01', end='2024-01-01', freq='D')
        
        # Create realistic stock price data with trend and seasonality
        np.random.seed(42)
        trend = np.linspace(100, 150, len(dates))
        seasonality = 10 * np.sin(2 * np.pi * np.arange(len(dates)) / 365.25)
        noise = np.random.normal(0, 5, len(dates))
        
        prices = trend + seasonality + noise
        
        # Create DataFrame
        data = pd.DataFrame({
            'Date': dates,
            'Close_Price': prices.round(2),
            'Volume': np.random.randint(1000000, 5000000, len(dates))
        })
        
        # Save to CSV
        data.to_csv(filename, index=False)
        
        print(f"✅ Sample data created: {filename}")
        print(f"📊 Data shape: {data.shape}")
        print(f"📅 Date range: {data['Date'].min()} to {data['Date'].max()}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error creating sample data: {str(e)}")
        return False
