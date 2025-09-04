# agents.py (DEFINITIVE FINAL VERSION 2)

from crewai import Agent
from langchain_groq import ChatGroq
from config import Config
import logging

logger = logging.getLogger(__name__)

class MarketAgents:
    def __init__(self):
        # We will use ONE stable, powerful model for all agents to ensure success.
        self.main_llm = ChatGroq(
            groq_api_key=Config.GROQ_API_KEY,
            model_name="groq/llama-3.3-70b-versatile"
        )

    def create_search_agent(self):
        """Create agent responsible for searching financial news"""
        return Agent(
            role="Financial News Researcher",
            goal="Find the latest and most relevant US financial market news from the past few hours",
            backstory="You are an expert financial news researcher.",
            verbose=True,
            allow_delegation=False,
            llm=self.main_llm,  # Use the main model
            tools=[]
        )

    def create_summary_agent(self):
        """Create agent responsible for summarizing financial news"""
        return Agent(
            role="Financial Market Analyst",
            goal="Create a comprehensive yet concise daily market summary under 250 words",
            backstory="You are a senior financial analyst with 15+ years of experience.",
            verbose=True,
            allow_delegation=False,
            llm=self.main_llm,  # Use the main model
            tools=[]
        )

    def create_formatting_agent(self):
        """Create agent responsible for formatting and adding visual elements"""
        return Agent(
            role="Content Formatter and Visual Designer",
            goal="Enhance the market summary with professional formatting and one relevant image.",
            backstory="You are a financial content designer.",
            verbose=True,
            allow_delegation=False,
            llm=self.main_llm,  # Use the main model
            tools=[]
        )

    def create_translation_agent(self):
        """Create agent responsible for translating content"""
        return Agent(
            role="Multilingual Financial Translator",
            goal="Accurately translate financial content while preserving meaning and context",
            backstory="You are a professional translator specializing in financial content.",
            verbose=True,
            allow_delegation=False,
            llm=self.main_llm,  # Use the main model
            tools=[]
        )

    def create_send_agent(self):
        """Create agent responsible for delivering content to Telegram"""
        return Agent(
            role="Content Delivery Specialist",
            goal="Successfully deliver the formatted market summary to the designated Telegram channel",
            backstory="You are a technical specialist responsible for content delivery.",
            verbose=True,
            allow_delegation=False,
            llm=self.main_llm,  # Use the main model
            tools=[]
        )