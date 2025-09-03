from crewai import Agent
from langchain_openai import ChatOpenAI
from config import Config
import logging

logger = logging.getLogger(__name__)

class MarketAgents:
    def __init__(self):
        # Initialize LLM
        self.llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0.1,
            api_key=Config.OPENAI_API_KEY
        )
    
    def create_search_agent(self):
        """Create agent responsible for searching financial news"""
        return Agent(
            role="Financial News Researcher",
            goal="Find the latest and most relevant US financial market news from the past few hours",
            backstory="""You are an expert financial news researcher with access to real-time market data. 
            Your job is to search for the most important financial news that happened today, focusing on:
            - Major stock market movements (Dow, S&P 500, NASDAQ)
            - Federal Reserve announcements
            - Economic indicators and data releases
            - Major corporate earnings or news
            - Sector performance
            - Currency and commodity movements
            - Bond market activity
            
            You prioritize accuracy and relevance, ensuring all information is current and from reputable sources.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm,
            tools=[],  # Will be populated with Tavily search tool
            max_iter=3,
            memory=True
        )
    
    def create_summary_agent(self):
        """Create agent responsible for summarizing financial news"""
        return Agent(
            role="Financial Market Analyst",
            goal="Create a comprehensive yet concise daily market summary under 500 words",
            backstory="""You are a senior financial analyst with 15+ years of experience in market analysis. 
            Your expertise includes equity markets, fixed income, commodities, and macroeconomic analysis.
            
            Your task is to synthesize complex financial information into an accessible daily summary that covers:
            - Market performance overview (major indices)
            - Key sector movements and standout performers
            - Important economic news and policy updates
            - Notable stock movements and earnings
            - Currency and commodity highlights
            - Market sentiment and outlook
            
            You write in a professional yet accessible tone, making complex financial concepts understandable 
            to a broad audience while maintaining accuracy and insight.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm,
            tools=[],
            max_iter=2,
            memory=True
        )
    
    def create_formatting_agent(self):
        """Create agent responsible for formatting and adding visual elements"""
        return Agent(
            role="Content Formatter and Visual Designer",
            goal="Enhance the market summary with appropriate charts, images, and professional formatting",
            backstory="""You are a financial content designer with expertise in data visualization and 
            financial communication. Your role is to enhance written content with visual elements that 
            support and clarify the information.
            
            You excel at:
            - Selecting relevant charts and graphs from financial data
            - Choosing appropriate images that illustrate market concepts
            - Formatting content for maximum readability
            - Ensuring visual elements complement rather than distract from the text
            - Maintaining professional presentation standards
            
            You understand that good visuals can make complex financial information more accessible 
            and engaging for readers.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm,
            tools=[],
            max_iter=2,
            memory=True
        )
    
    def create_translation_agent(self):
        """Create agent responsible for translating content"""
        return Agent(
            role="Multilingual Financial Translator",
            goal="Accurately translate financial content while preserving meaning and context",
            backstory="""You are a professional translator specializing in financial and economic content. 
            You have native-level proficiency in English, Hindi, Arabic, and Hebrew, with deep understanding 
            of financial terminology in each language.
            
            Your expertise includes:
            - Financial and economic terminology translation
            - Cultural adaptation of financial concepts
            - Maintaining professional tone across languages
            - Preserving numerical data and formatting
            - Understanding regional financial market contexts
            
            You ensure that translated content is not just linguistically accurate but also culturally 
            appropriate and maintains the professional standards expected in financial communication.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm,
            tools=[],
            max_iter=2,
            memory=True
        )
    
    def create_send_agent(self):
        """Create agent responsible for delivering content to Telegram"""
        return Agent(
            role="Content Delivery Specialist",
            goal="Successfully deliver the formatted market summary to the designated Telegram channel",
            backstory="""You are a technical specialist responsible for content delivery and distribution. 
            Your expertise lies in understanding various communication platforms and ensuring content 
            reaches its intended audience effectively.
            
            Your responsibilities include:
            - Formatting content appropriately for Telegram
            - Ensuring proper message formatting and structure
            - Handling delivery errors and retries
            - Managing file uploads and media attachments
            - Verifying successful delivery
            
            You are detail-oriented and reliable, ensuring that the carefully crafted market summary 
            reaches subscribers in the best possible format.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm,
            tools=[],
            max_iter=2,
            memory=True
        )
