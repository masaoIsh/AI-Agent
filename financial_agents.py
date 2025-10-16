"""
Financial Analysis Multi-Agent System
Three specialized agents that debate stock recommendations
"""

import asyncio
import random
from typing import Dict, List, Tuple
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.tools import AgentTool
from autogen_ext.models.ollama import OllamaChatCompletionClient


class FinancialAgent:
    """Base class for financial analysis agents"""
    
    def __init__(self, name: str, model_client: OllamaChatCompletionClient):
        self.name = name
        self.model_client = model_client
        self.agent = None
        self.tool = None
        
    async def analyze_stock(self, stock_symbol: str) -> str:
        """Analyze a stock and return BUY/SELL recommendation"""
        # Randomly choose BUY or SELL for demonstration
        recommendation = random.choice(["BUY", "SELL"])
        return f"{self.name} recommends: {recommendation} for {stock_symbol}"


class FundamentalAnalysisAgent(FinancialAgent):
    """Agent specializing in fundamental analysis"""
    
    def __init__(self, model_client: OllamaChatCompletionClient):
        super().__init__("Fundamental Analyst", model_client)
        self.agent = AssistantAgent(
            "fundamental_analyst",
            model_client=model_client,
            system_message="""You are a fundamental analysis expert specializing in:
            - Financial statement analysis (P&L, Balance Sheet, Cash Flow)
            - Company valuation metrics (P/E, P/B, EV/EBITDA)
            - Industry analysis and competitive positioning
            - Management quality assessment
            - Growth prospects and market opportunities
            
            You provide BUY/SELL recommendations based on fundamental analysis.
            Be concise but provide reasoning for your recommendations.""",
            description="A fundamental analysis expert who evaluates stocks based on financial metrics and business fundamentals.",
            model_client_stream=True,
        )
        self.tool = AgentTool(self.agent, return_value_as_last_message=True)
    
    async def analyze_stock(self, stock_symbol: str) -> str:
        recommendation = random.choice(["BUY", "SELL"])
        reasoning = self._get_fundamental_reasoning(recommendation, stock_symbol)
        return f"FUNDAMENTAL ANALYSIS for {stock_symbol}:\n{reasoning}\nRecommendation: {recommendation}"
    
    def _get_fundamental_reasoning(self, recommendation: str, stock_symbol: str) -> str:
        if recommendation == "BUY":
            reasons = [
                "Strong revenue growth and improving profit margins",
                "Undervalued based on P/E ratio compared to industry average",
                "Solid balance sheet with low debt-to-equity ratio",
                "Market-leading position with competitive moats",
                "Strong cash flow generation and dividend sustainability"
            ]
        else:
            reasons = [
                "Declining revenue and contracting margins",
                "Overvalued based on current P/E and P/B ratios",
                "High debt levels and deteriorating credit metrics",
                "Intense competition eroding market share",
                "Weak cash flow and unsustainable dividend payout ratio"
            ]
        
        return f"• {random.choice(reasons)}\n• {random.choice(reasons)}\n• {random.choice(reasons)}"


class SentimentAnalysisAgent(FinancialAgent):
    """Agent specializing in market sentiment analysis"""
    
    def __init__(self, model_client: OllamaChatCompletionClient):
        super().__init__("Sentiment Analyst", model_client)
        self.agent = AssistantAgent(
            "sentiment_analyst",
            model_client=model_client,
            system_message="""You are a market sentiment analysis expert focusing on:
            - News sentiment and media coverage analysis
            - Social media sentiment (Twitter, Reddit, forums)
            - Analyst ratings and price target changes
            - Institutional investor sentiment and positioning
            - Market momentum and technical sentiment indicators
            
            You provide BUY/SELL recommendations based on market sentiment.
            Consider both positive and negative sentiment factors.""",
            description="A sentiment analysis expert who evaluates market psychology and investor sentiment.",
            model_client_stream=True,
        )
        self.tool = AgentTool(self.agent, return_value_as_last_message=True)
    
    async def analyze_stock(self, stock_symbol: str) -> str:
        recommendation = random.choice(["BUY", "SELL"])
        reasoning = self._get_sentiment_reasoning(recommendation, stock_symbol)
        return f"SENTIMENT ANALYSIS for {stock_symbol}:\n{reasoning}\nRecommendation: {recommendation}"
    
    def _get_sentiment_reasoning(self, recommendation: str, stock_symbol: str) -> str:
        if recommendation == "BUY":
            reasons = [
                "Positive news coverage and upbeat analyst commentary",
                "Strong social media sentiment with increasing mentions",
                "Recent analyst upgrades and raised price targets",
                "Institutional buying pressure and insider purchases",
                "Bullish momentum with increasing trading volume"
            ]
        else:
            reasons = [
                "Negative news cycle and bearish media coverage",
                "Deteriorating social media sentiment and increased criticism",
                "Recent analyst downgrades and lowered price targets",
                "Institutional selling pressure and insider sales",
                "Bearish momentum with declining trading volume"
            ]
        
        return f"• {random.choice(reasons)}\n• {random.choice(reasons)}\n• {random.choice(reasons)}"


class ValuationStubAgent(FinancialAgent):
    """Agent specializing in valuation analysis (stub implementation)"""
    
    def __init__(self, model_client: OllamaChatCompletionClient):
        super().__init__("Valuation Analyst", model_client)
        self.agent = AssistantAgent(
            "valuation_analyst",
            model_client=model_client,
            system_message="""You are a valuation analysis expert specializing in:
            - Discounted Cash Flow (DCF) modeling
            - Comparable company analysis (Comps)
            - Precedent transaction analysis
            - Asset-based valuation methods
            - Risk-adjusted valuation scenarios
            
            You provide BUY/SELL recommendations based on valuation analysis.
            Focus on whether the stock is trading above or below intrinsic value.""",
            description="A valuation expert who determines if stocks are overvalued or undervalued.",
            model_client_stream=True,
        )
        self.tool = AgentTool(self.agent, return_value_as_last_message=True)
    
    async def analyze_stock(self, stock_symbol: str) -> str:
        recommendation = random.choice(["BUY", "SELL"])
        reasoning = self._get_valuation_reasoning(recommendation, stock_symbol)
        return f"VALUATION ANALYSIS for {stock_symbol}:\n{reasoning}\nRecommendation: {recommendation}"
    
    def _get_valuation_reasoning(self, recommendation: str, stock_symbol: str) -> str:
        if recommendation == "BUY":
            reasons = [
                "DCF model shows 20%+ upside to current price",
                "Trading at significant discount to peer group multiples",
                "Sum-of-parts analysis indicates undervaluation",
                "Conservative scenarios still show attractive valuation",
                "Asset-based valuation suggests strong margin of safety"
            ]
        else:
            reasons = [
                "DCF model indicates 15%+ downside risk",
                "Trading at premium to historical valuation multiples",
                "Sum-of-parts analysis shows overvaluation",
                "Optimistic scenarios required to justify current price",
                "Asset-based valuation provides limited downside protection"
            ]
        
        return f"• {random.choice(reasons)}\n• {random.choice(reasons)}\n• {random.choice(reasons)}"


