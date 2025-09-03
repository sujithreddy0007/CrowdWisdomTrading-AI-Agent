import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    # API Keys - Updated with actual keys, can be overridden by environment variables
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', 'sk-proj-...your_actual_openai_key_here...')
    TAVILY_API_KEY = os.getenv('TAVILY_API_KEY', 'tvly-dev-...your_actual_tavily_key_here...')
    TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '...your_actual_telegram_bot_token_here...')
    TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID', '...your_actual_telegram_chat_id_here...')
    GROQ_API_KEY = os.getenv('GROQ_API_KEY', 'gsk_...your_actual_groq_key_here...')
    
    # Configuration
    MARKET_TIMEZONE = os.getenv('MARKET_TIMEZONE', 'America/New_York')
    SUMMARY_LANGUAGE = os.getenv('SUMMARY_LANGUAGE', 'en')
    TRANSLATION_LANGUAGES = os.getenv('TRANSLATION_LANGUAGES', 'hi,ar,he').split(',')
    
    # Output settings
    MAX_SUMMARY_WORDS = 500
    OUTPUT_DIR = 'outputs'
    PDF_FILENAME = 'daily_market_summary.pdf'
    
    # News search settings
    NEWS_SEARCH_QUERIES = [
        "US stock market news today",
        "S&P 500 NASDAQ Dow Jones market close",
        "Federal Reserve interest rates",
        "US economic indicators",
        "major stock movements today"
    ]
    
    # Validation
    @classmethod
    def validate(cls):
        required_keys = ['GROQ_API_KEY', 'TAVILY_API_KEY', 'TELEGRAM_BOT_TOKEN', 'TELEGRAM_CHAT_ID']
        missing = [key for key in required_keys if not getattr(cls, key)]
        if missing:
            raise ValueError(f"Missing required environment variables: {', '.join(missing)}")
        return True
