"""
Sector-based fundamental comparison for relative valuation analysis.
Computes percentile ranks and z-scores for key metrics within a sector.
"""

from __future__ import annotations

from typing import Optional
import numpy as np
import pandas as pd


class SectorComparator:
    def __init__(self):
        self.fundamentals_df: Optional[pd.DataFrame] = None
        self.comparison_df: Optional[pd.DataFrame] = None
    
    def load_fundamentals(self, fundamentals_df: pd.DataFrame) -> bool:
        """Load fundamental data for analysis."""
        try:
            if fundamentals_df.empty:
                raise ValueError("Fundamentals DataFrame is empty")
            self.fundamentals_df = fundamentals_df
            return True
        except Exception as e:
            print(f"❌ Error loading fundamentals: {e}")
            return False
    
    def compute_sector_comparison(self, sector: Optional[str] = None) -> pd.DataFrame:
        """
        Compute sector-relative metrics: percentile ranks and z-scores for PBR, ROE, ROA.
        If sector is None, uses the most common sector in the data.
        """
        if self.fundamentals_df is None or self.fundamentals_df.empty:
            raise ValueError("No fundamentals data loaded")
        
        df = self.fundamentals_df.copy()
        
        # Filter by sector if specified
        if sector is None:
            sector = df['sector'].mode()[0] if not df['sector'].mode().empty else df['sector'].iloc[0]
        
        sector_df = df[df['sector'] == sector].copy()
        
        if len(sector_df) < 2:
            print(f"⚠️ Only {len(sector_df)} stocks in sector '{sector}', comparisons may not be meaningful.")
        
        # Metrics to compare
        metrics = ['pb_ratio', 'pe_ratio', 'roe', 'roa', 'profit_margin', 'debt_to_equity']
        
        for metric in metrics:
            if metric in sector_df.columns:
                # Percentile rank (0-100) - only for non-NaN values
                sector_df[f'{metric}_percentile'] = sector_df[metric].rank(pct=True, na_option='keep') * 100
                
                # Z-score - skip NaN values in calculations
                mean_val = sector_df[metric].mean(skipna=True)
                std_val = sector_df[metric].std(skipna=True)
                
                # Only compute z-score if we have valid data
                if pd.notna(mean_val) and pd.notna(std_val) and std_val > 0:
                    sector_df[f'{metric}_zscore'] = (sector_df[metric] - mean_val) / std_val
                else:
                    sector_df[f'{metric}_zscore'] = np.nan
        
        self.comparison_df = sector_df
        return sector_df
    
    def format_comparison_report(self, symbol: Optional[str] = None) -> str:
        """
        Format a comparison report for agents.
        If symbol is provided, highlights that stock's position in the sector.
        """
        if self.comparison_df is None or self.comparison_df.empty:
            return "No comparison data available."
        
        df = self.comparison_df
        sector = df['sector'].iloc[0] if len(df) > 0 else 'Unknown'
        
        report = f"Sector Comparison Analysis: {sector}\n"
        report += "=" * 80 + "\n"
        report += f"Number of stocks in sector: {len(df)}\n\n"
        
        # Summary statistics
        report += "Sector Averages:\n"
        metrics = ['pb_ratio', 'pe_ratio', 'roe', 'roa', 'profit_margin', 'debt_to_equity']
        for metric in metrics:
            if metric in df.columns:
                mean_val = df[metric].mean()
                median_val = df[metric].median()
                if pd.notna(mean_val):
                    report += f"  {metric.upper()}: Mean={mean_val:.4f}, Median={median_val:.4f}\n"
        
        report += "\n"
        
        # Individual stock comparison
        if symbol:
            stock_row = df[df['symbol'] == symbol]
            if not stock_row.empty:
                report += f"Stock Analysis: {symbol}\n"
                report += "-" * 80 + "\n"
                
                for metric in metrics:
                    if metric in df.columns and f'{metric}_percentile' in df.columns:
                        val = stock_row[metric].iloc[0]
                        pct = stock_row[f'{metric}_percentile'].iloc[0]
                        z = stock_row[f'{metric}_zscore'].iloc[0]
                        
                        if pd.notna(val):
                            # Interpretation
                            if metric in ['roe', 'roa', 'profit_margin']:
                                interpretation = "Above average" if z > 0 else "Below average"
                            elif metric in ['pb_ratio', 'pe_ratio', 'debt_to_equity']:
                                interpretation = "Premium valuation" if z > 0 else "Discount valuation"
                            else:
                                interpretation = ""
                            
                            report += f"  {metric.upper()}: {val:.4f} (Percentile: {pct:.1f}, Z-score: {z:.2f}) {interpretation}\n"
        else:
            # Show all stocks ranked
            report += "Stocks Ranked by ROE:\n"
            report += "-" * 80 + "\n"
            sorted_df = df.sort_values('roe', ascending=False, na_position='last')
            for idx, row in sorted_df.iterrows():
                sym = row['symbol']
                roe = row.get('roe', None)
                roa = row.get('roa', None)
                pbr = row.get('pb_ratio', None)
                
                # Handle None values gracefully
                roe_str = f"{roe:.4f}" if roe is not None and not pd.isna(roe) else "N/A"
                roa_str = f"{roa:.4f}" if roa is not None and not pd.isna(roa) else "N/A"
                pbr_str = f"{pbr:.4f}" if pbr is not None and not pd.isna(pbr) else "N/A"
                
                report += f"  {sym}: ROE={roe_str}, ROA={roa_str}, PBR={pbr_str}\n"
        
        return report
    
    def get_sector_rankings(self) -> pd.DataFrame:
        """
        Get stocks ranked by composite score (ROE + ROA - PBR normalized).
        Higher score = better fundamentals relative to valuation.
        """
        if self.comparison_df is None or self.comparison_df.empty:
            raise ValueError("No comparison data available")
        
        df = self.comparison_df.copy()
        
        # Composite score: higher ROE/ROA is good, lower PBR is good
        df['composite_score'] = 0.0
        if 'roe_zscore' in df.columns:
            df['composite_score'] += df['roe_zscore'].fillna(0)
        if 'roa_zscore' in df.columns:
            df['composite_score'] += df['roa_zscore'].fillna(0)
        if 'pb_ratio_zscore' in df.columns:
            df['composite_score'] -= df['pb_ratio_zscore'].fillna(0)  # Lower PBR is better
        
        ranked = df.sort_values('composite_score', ascending=False)
        return ranked[['symbol', 'pb_ratio', 'roe', 'roa', 'composite_score', 'pb_ratio_percentile', 'roe_percentile', 'roa_percentile']]

