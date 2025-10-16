"""
Debate Orchestrator for Financial Analysis Multi-Agent System
Implements round-robin debate when agents disagree
"""

import asyncio
from typing import List, Dict, Tuple
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.ollama import OllamaChatCompletionClient
from financial_agents import FundamentalAnalysisAgent, SentimentAnalysisAgent, ValuationStubAgent


class DebateOrchestrator:
    """Orchestrates debate between financial analysis agents"""
    
    def __init__(self, model_client: OllamaChatCompletionClient):
        self.model_client = model_client
        self.agents = {
            'fundamental': FundamentalAnalysisAgent(model_client),
            'sentiment': SentimentAnalysisAgent(model_client),
            'valuation': ValuationStubAgent(model_client)
        }
        self.debate_history = []
        
        # Create a moderator agent for facilitating debates
        self.moderator = AssistantAgent(
            "debate_moderator",
            model_client=model_client,
            system_message="""You are a debate moderator for financial analysis discussions.
            Your role is to:
            - Summarize each agent's position clearly
            - Identify areas of agreement and disagreement
            - Ask probing questions to clarify reasoning
            - Help agents find common ground
            - Facilitate productive discussion
            
            Keep debates focused and professional. Encourage evidence-based arguments.""",
            description="A debate moderator who facilitates discussions between financial analysts.",
            model_client_stream=True,
        )
    
    async def analyze_stock_with_debate(self, stock_symbol: str, max_rounds: int = 3) -> Dict:
        """
        Analyze a stock and run debate if agents disagree
        
        Args:
            stock_symbol: Stock symbol to analyze
            max_rounds: Maximum number of debate rounds
            
        Returns:
            Dictionary containing analysis results and final recommendation
        """
        print(f"\n{'='*60}")
        print(f"FINANCIAL ANALYSIS DEBATE: {stock_symbol}")
        print(f"{'='*60}")
        
        # Get initial recommendations from all agents
        initial_analyses = await self._get_initial_analyses(stock_symbol)
        
        # Check if agents agree
        recommendations = [analysis['recommendation'] for analysis in initial_analyses.values()]
        unique_recommendations = set(recommendations)
        
        if len(unique_recommendations) == 1:
            # All agents agree
            print(f"\n✅ CONSENSUS REACHED: All agents recommend {unique_recommendations.pop()}")
            return {
                'stock_symbol': stock_symbol,
                'consensus': True,
                'final_recommendation': recommendations[0],
                'initial_analyses': initial_analyses,
                'debate_rounds': 0,
                'debate_history': []
            }
        
        # Agents disagree - start debate
        print(f"\n⚠️  DISAGREEMENT DETECTED: {len(unique_recommendations)} different recommendations")
        print("Starting debate process...\n")
        
        debate_result = await self._conduct_debate(stock_symbol, initial_analyses, max_rounds)
        
        return {
            'stock_symbol': stock_symbol,
            'consensus': False,
            'initial_analyses': initial_analyses,
            'debate_rounds': debate_result['rounds'],
            'debate_history': debate_result['history'],
            'final_recommendation': debate_result['final_recommendation'],
            'debate_summary': debate_result['summary']
        }
    
    async def _get_initial_analyses(self, stock_symbol: str) -> Dict:
        """Get initial analyses from all agents"""
        analyses = {}
        
        print("📊 Getting initial analyses from all agents...")
        
        for agent_name, agent in self.agents.items():
            print(f"\n{agent_name.upper()} ANALYSIS:")
            analysis_text = await agent.analyze_stock(stock_symbol)
            print(analysis_text)
            
            # Extract recommendation from analysis text
            recommendation = "BUY" if "BUY" in analysis_text else "SELL"
            
            analyses[agent_name] = {
                'analysis': analysis_text,
                'recommendation': recommendation,
                'agent_name': agent.name
            }
        
        return analyses
    
    async def _conduct_debate(self, stock_symbol: str, initial_analyses: Dict, max_rounds: int) -> Dict:
        """Conduct round-robin debate between agents"""
        debate_history = []
        current_round = 1
        
        # Create debate context
        debate_context = self._create_debate_context(stock_symbol, initial_analyses)
        
        while current_round <= max_rounds:
            print(f"\n🗣️  DEBATE ROUND {current_round}")
            print("-" * 40)
            
            round_result = await self._run_debate_round(
                stock_symbol, 
                debate_context, 
                current_round,
                debate_history
            )
            
            debate_history.append(round_result)
            
            # Check if consensus reached
            if round_result.get('consensus_reached'):
                print(f"\n✅ CONSENSUS REACHED in Round {current_round}!")
                break
            
            current_round += 1
        
        # Determine final recommendation
        final_recommendation = self._determine_final_recommendation(debate_history, initial_analyses)
        
        # Generate debate summary
        summary = await self._generate_debate_summary(stock_symbol, debate_history, final_recommendation)
        
        return {
            'rounds': len(debate_history),
            'history': debate_history,
            'final_recommendation': final_recommendation,
            'summary': summary
        }
    
    def _create_debate_context(self, stock_symbol: str, initial_analyses: Dict) -> str:
        """Create context for the debate"""
        context = f"Stock: {stock_symbol}\n\nInitial Analyses:\n"
        
        for agent_name, analysis in initial_analyses.items():
            context += f"\n{agent_name.upper()}: {analysis['recommendation']}\n"
            context += f"{analysis['analysis']}\n"
        
        return context
    
    async def _run_debate_round(self, stock_symbol: str, context: str, round_num: int, history: List) -> Dict:
        """Run a single round of debate"""
        round_messages = []
        
        # Each agent gets a chance to respond
        for agent_name, agent in self.agents.items():
            # Create debate prompt
            debate_prompt = self._create_debate_prompt(stock_symbol, context, round_num, history, agent_name)
            
            # Get agent response (simulated for this demo)
            response = await self._simulate_debate_response(agent_name, debate_prompt)
            
            round_messages.append({
                'agent': agent_name,
                'message': response,
                'round': round_num
            })
            
            print(f"{agent_name.upper()}: {response}")
        
        # Check for consensus (simplified - in reality would use more sophisticated logic)
        consensus_reached = self._check_consensus(round_messages)
        
        return {
            'round': round_num,
            'messages': round_messages,
            'consensus_reached': consensus_reached
        }
    
    def _create_debate_prompt(self, stock_symbol: str, context: str, round_num: int, history: List, agent_name: str) -> str:
        """Create debate prompt for an agent"""
        prompt = f"""You are participating in a debate about {stock_symbol}.
        
Round {round_num} of the debate.

Previous context:
{context}

"""
        
        if history:
            prompt += "Previous debate rounds:\n"
            for h in history[-2:]:  # Last 2 rounds for context
                prompt += f"Round {h['round']}:\n"
                for msg in h['messages']:
                    prompt += f"- {msg['agent']}: {msg['message']}\n"
        
        prompt += f"\nAs the {agent_name} analyst, respond to the debate. "
        prompt += "Address other agents' points, defend your position, or acknowledge valid counterarguments. "
        prompt += "Be concise but persuasive."
        
        return prompt
    
    async def _simulate_debate_response(self, agent_name: str, prompt: str) -> str:
        """Simulate debate response (in a real implementation, this would use the actual agent)"""
        responses = {
            'fundamental': [
                "I maintain my position based on solid financial metrics. The fundamentals don't lie.",
                "While sentiment is important, we can't ignore the underlying financial health of the company.",
                "I understand the valuation concerns, but strong fundamentals often lead to improved valuations.",
                "The numbers speak for themselves - this is a fundamentally sound investment."
            ],
            'sentiment': [
                "Market sentiment is a powerful driver of short to medium-term price movements.",
                "I respect the fundamental analysis, but sentiment can override fundamentals in the near term.",
                "The current market mood suggests investors are looking beyond traditional metrics.",
                "Sentiment indicators are showing clear directional bias that shouldn't be ignored."
            ],
            'valuation': [
                "From a pure valuation standpoint, the current price doesn't reflect intrinsic value.",
                "Valuation models provide an objective framework that sentiment and fundamentals must eventually align with.",
                "I acknowledge the fundamental strengths, but the math doesn't support the current price.",
                "While sentiment is bullish, valuations are stretched beyond reasonable levels."
            ]
        }
        
        # Simulate some debate dynamics
        import random
        
        # Sometimes agents change their mind
        if random.random() < 0.2:  # 20% chance
            responses[agent_name].append("After considering the arguments, I'm reconsidering my position.")
        
        return random.choice(responses[agent_name])
    
    def _check_consensus(self, round_messages: List) -> bool:
        """Check if consensus has been reached (simplified logic)"""
        # In a real implementation, this would use more sophisticated NLP
        # to detect when agents are converging on a recommendation
        
        # For demo purposes, randomly reach consensus sometimes
        import random
        return random.random() < 0.3  # 30% chance of consensus each round
    
    def _determine_final_recommendation(self, debate_history: List, initial_analyses: Dict) -> str:
        """Determine final recommendation after debate"""
        # Count recommendations
        buy_count = 0
        sell_count = 0
        
        # Count initial recommendations
        for analysis in initial_analyses.values():
            if analysis['recommendation'] == 'BUY':
                buy_count += 1
            else:
                sell_count += 1
        
        # In a real implementation, this would analyze the debate content
        # For now, use majority vote with some debate influence
        import random
        
        # Debate can influence the outcome
        debate_influence = random.choice(['buy', 'sell', 'neutral'])
        
        if debate_influence == 'buy':
            buy_count += 1
        elif debate_influence == 'sell':
            sell_count += 1
        
        return 'BUY' if buy_count > sell_count else 'SELL'
    
    async def _generate_debate_summary(self, stock_symbol: str, debate_history: List, final_recommendation: str) -> str:
        """Generate summary of the debate"""
        summary = f"Debate Summary for {stock_symbol}:\n"
        summary += f"Final Recommendation: {final_recommendation}\n"
        summary += f"Rounds of Debate: {len(debate_history)}\n\n"
        
        summary += "Key Debate Points:\n"
        for i, round_data in enumerate(debate_history, 1):
            summary += f"\nRound {i}:\n"
            for msg in round_data['messages']:
                summary += f"- {msg['agent']}: {msg['message'][:100]}...\n"
        
        return summary


