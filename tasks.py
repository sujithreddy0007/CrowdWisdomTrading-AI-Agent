from crewai import Task
from typing import List
from config import Config
from utils import validate_summary, clean_text
import logging

logger = logging.getLogger(__name__)

class MarketTasks:
    def __init__(self):
        self.max_summary_words = Config.MAX_SUMMARY_WORDS
        self.translation_languages = Config.TRANSLATION_LANGUAGES
    
    def create_search_task(self, search_agent):
        """Create task for searching financial news"""
        return Task(
            description=f"""
            Search for the latest US financial market news from the past few hours. 
            Focus on finding comprehensive information about:
            
            1. Major stock market indices (Dow Jones, S&P 500, NASDAQ)
            2. Federal Reserve announcements or policy changes
            3. Economic indicators and data releases
            4. Major corporate earnings or significant company news
            5. Sector performance (technology, healthcare, financial, energy, etc.)
            6. Currency movements (USD, EUR, GBP, JPY)
            7. Commodity prices (oil, gold, silver, etc.)
            8. Bond market activity and yields
            
            Use multiple search queries to ensure comprehensive coverage:
            - "US stock market close today"
            - "Federal Reserve interest rates today"
            - "S&P 500 NASDAQ Dow Jones performance"
            - "major earnings announcements today"
            - "economic indicators released today"
            
            Provide detailed, factual information with sources and timestamps.
            Prioritize recent news (last 6-8 hours) and authoritative financial sources.
            """,
            expected_output="""
            A comprehensive JSON object containing:
            - search_results: Array of news articles with title, content, source, and timestamp
            - market_data: Key market metrics and performance data
            - economic_news: Important economic indicators and policy updates
            - corporate_news: Major earnings and company announcements
            - sources: List of all sources used with credibility ratings
            """,
            agent=search_agent,
            tools=[],  # Will be populated with search tools
            context=[],
            output_file="search_results.json"
        )
    
    def create_summary_task(self, summary_agent, search_results):
        """Create task for summarizing financial news"""
        return Task(
            description=f"""
            Create a comprehensive daily market summary based on the search results.
            
            Requirements:
            - Maximum {self.max_summary_words} words
            - Professional, accessible tone
            - Cover all major market segments
            - Include specific data points and percentages
            - Maintain accuracy and objectivity
            
            Structure your summary as follows:
            1. **Market Overview**: Overall market performance and sentiment
            2. **Major Indices**: Performance of Dow, S&P 500, NASDAQ with specific numbers
            3. **Sector Highlights**: Top performing and underperforming sectors
            4. **Key News**: Most important economic or corporate developments
            5. **Currency & Commodities**: Notable movements in FX and commodity markets
            6. **Market Outlook**: Brief analysis of what to watch tomorrow
            
            Use the search results to provide specific, factual information.
            Include relevant statistics, percentages, and concrete data points.
            Avoid speculation and focus on verified information.
            """,
            expected_output="""
            A well-structured market summary in markdown format with:
            - Clear headings and sections
            - Specific data points and percentages
            - Professional formatting
            - Word count under {self.max_summary_words} words
            - Factual, objective tone
            """,
            agent=summary_agent,
            tools=[],
            context=[search_results],
            output_file="market_summary.md"
        )
    
    def create_formatting_task(self, formatting_agent, summary_content):
        """Create task for formatting and adding visual elements"""
        return Task(
            description="""
            Enhance the market summary with appropriate visual elements and formatting.
            
            Your tasks:
            1. **Chart Selection**: Identify 2-3 key data points that would benefit from visual representation
            2. **Image Integration**: Find relevant financial charts or market images
            3. **Formatting**: Ensure professional presentation with proper markdown formatting
            4. **Layout**: Optimize the layout for both PDF and Telegram delivery
            
            Focus on:
            - Stock market performance charts
            - Sector performance visualizations
            - Economic indicator graphs
            - Currency movement charts
            
            Ensure all images are:
            - Relevant to the content
            - High quality and professional
            - Properly sized for different platforms
            - Include appropriate captions
            
            Maintain the original content while enhancing it with visual elements.
            """,
            expected_output="""
            Enhanced market summary with:
            - 2-3 relevant charts or images
            - Professional markdown formatting
            - Optimized layout for multiple platforms
            - Image captions and descriptions
            - Consistent visual style
            """,
            agent=formatting_agent,
            tools=[],  # Will be populated with image and chart tools
            context=[summary_content],
            output_file="formatted_summary.md"
        )
    
    def create_translation_task(self, translation_agent, formatted_content, language):
        """Create task for translating content to specific language"""
        language_names = {
            'hi': 'Hindi',
            'ar': 'Arabic', 
            'he': 'Hebrew'
        }
        
        return Task(
            description=f"""
            Translate the formatted market summary into {language_names.get(language, language)}.
            
            Translation requirements:
            1. **Accuracy**: Maintain all financial data, numbers, and percentages exactly
            2. **Context**: Preserve the professional financial tone and terminology
            3. **Formatting**: Keep all markdown formatting, headings, and structure
            4. **Cultural Adaptation**: Use appropriate financial terminology for the target market
            5. **Completeness**: Translate all text including captions and descriptions
            
            Special considerations:
            - Financial terms should use standard translations in the target language
            - Company names and ticker symbols remain unchanged
            - Numbers, percentages, and dates maintain original format
            - Currency symbols may need localization
            - Maintain the same word count and structure
            
            Ensure the translation is:
            - Grammatically correct and natural
            - Professionally appropriate for financial content
            - Culturally sensitive and relevant
            - Ready for immediate publication
            """,
            expected_output=f"""
            Complete translation of the market summary in {language_names.get(language, language)} with:
            - All text accurately translated
            - Original formatting preserved
            - Financial terminology properly localized
            - Professional tone maintained
            - Ready for publication
            """,
            agent=translation_agent,
            tools=[],
            context=[formatted_content],
            output_file=f"summary_{language}.md"
        )
    
    def create_send_task(self, send_agent, formatted_task, translation_tasks: List):
        """Create task for sending content to Telegram"""
        return Task(
            description=f"""
            Deliver the market summary to the designated Telegram channel.
            
            Delivery requirements:
            1. **Multi-language Support**: Send the summary in all available languages
            2. **Format Optimization**: Ensure proper formatting for Telegram
            3. **Media Handling**: Include charts and images appropriately
            4. **Error Handling**: Implement retry logic for failed deliveries
            5. **Verification**: Confirm successful delivery
            
            For each language version:
            - Format the message with proper Telegram markdown
            - Include relevant images or charts
            - Add appropriate language indicators
            - Ensure message length is within Telegram limits
            - Handle any formatting issues
            
            Delivery sequence:
            1. English version (primary)
            2. Hindi version
            3. Arabic version  
            4. Hebrew version
            
            Each delivery should be:
            - Properly formatted
            - Include visual elements
            - Confirmed as sent successfully
            - Logged for tracking
            """,
            expected_output="""
            Delivery confirmation report with:
            - Status of each language version sent
            - Message IDs for tracking
            - Any errors encountered and resolved
            - Confirmation of successful delivery
            - Summary of content delivered
            """,
            agent=send_agent,
            tools=[],  # Will be populated with Telegram tools
            context=[formatted_task] + translation_tasks,
            output_file="delivery_report.json"
        )
    
    def create_pdf_generation_task(self, pdf_agent, all_content):
        """Create task for generating PDF output"""
        return Task(
            description="""
            Generate a professional PDF document containing the market summary in all languages.
            
            PDF requirements:
            1. **Multi-language Layout**: Include all language versions in a single PDF
            2. **Professional Design**: Clean, corporate-style layout
            3. **Visual Elements**: Integrate charts and images properly
            4. **Navigation**: Table of contents and page numbering
            5. **Branding**: Professional header and footer
            
            Structure:
            - Cover page with date and title
            - Table of contents
            - English version (primary)
            - Hindi version
            - Arabic version (right-to-left layout)
            - Hebrew version (right-to-left layout)
            - Appendix with charts and data
            
            Technical requirements:
            - High-quality image rendering
            - Proper font support for all languages
            - Consistent formatting throughout
            - Print-ready quality
            - File size optimization
            """,
            expected_output="""
            Professional PDF document with:
            - All language versions included
            - High-quality visual elements
            - Professional layout and design
            - Proper language-specific formatting
            - Ready for distribution
            """,
            agent=pdf_agent,
            tools=[],
            context=[all_content],
            output_file=Config.PDF_FILENAME
        )
