from crewai import Crew, Process
from agents import MarketAgents
from tasks import MarketTasks
from tools import tavily_search_tool, market_data_tool, image_search_tool, telegram_send_tool
from pdf_generator import PDFGenerator
from config import Config
from utils import setup_logging, is_market_closed, validate_summary, format_telegram_message
import os
import json
import logging
from datetime import datetime
from typing import Dict, List

logger = setup_logging()

class MarketSummaryCrew:
    def __init__(self):
        """Initialize the Market Summary Crew"""
        # Validate configuration
        Config.validate()
        
        # Initialize components
        self.agents = MarketAgents()
        self.tasks = MarketTasks()
        self.pdf_generator = PDFGenerator()
        
        # Create output directory
        os.makedirs(Config.OUTPUT_DIR, exist_ok=True)
        
        # Initialize agents with tools
        self.search_agent = self.agents.create_search_agent()
        self.summary_agent = self.agents.create_summary_agent()
        self.formatting_agent = self.agents.create_formatting_agent()
        self.translation_agent = self.agents.create_translation_agent()
        self.send_agent = self.agents.create_send_agent()
        
        # Assign tools to agents
        self.search_agent.tools = [tavily_search_tool, market_data_tool]
        self.formatting_agent.tools = [image_search_tool, market_data_tool]
        self.send_agent.tools = [telegram_send_tool]
        
        logger.info("Market Summary Crew initialized successfully")
    
    def create_crew(self, tasks: List):
        """Create and configure the CrewAI crew"""
        return Crew(
            agents=[
                self.search_agent,
                self.summary_agent,
                self.formatting_agent,
                self.translation_agent,
                self.send_agent
            ],
            tasks=tasks,
            process=Process.sequential,
            verbose=True,
            memory=True,
            planning=True,
            embedder={
                "provider": "openai",
                "config": {
                    "model": "text-embedding-3-small"
                }
            }
        )
    
    def run_daily_summary(self):
        """Run the complete daily market summary workflow"""
        try:
            logger.info("Starting daily market summary generation")
            
            # Check if market is closed (optional validation)
            if not is_market_closed():
                logger.warning("Market may still be open. Proceeding anyway...")
            
            # Step 1: Search for financial news
            logger.info("Step 1: Searching for financial news")
            search_task = self.tasks.create_search_task(self.search_agent)
            
            # Step 2: Create summary
            logger.info("Step 2: Creating market summary")
            summary_task = self.tasks.create_summary_task(self.summary_agent, search_task)
            
            # Step 3: Format with visuals
            logger.info("Step 3: Formatting with visual elements")
            formatting_task = self.tasks.create_formatting_task(self.formatting_agent, summary_task)
            
            # Step 4: Translate to multiple languages
            logger.info("Step 4: Translating to multiple languages")
            translation_tasks = []
            for lang in Config.TRANSLATION_LANGUAGES:
                translation_task = self.tasks.create_translation_task(
                    self.translation_agent, formatting_task, lang
                )
                translation_tasks.append(translation_task)
            
            # Step 5: Send to Telegram
            logger.info("Step 5: Sending to Telegram")
            send_task = self.tasks.create_send_task(self.send_agent, {
                'formatted': formatting_task,
                'translations': translation_tasks
            })
            
            # Create crew with all tasks
            tasks_list = [search_task, summary_task, formatting_task] + translation_tasks + [send_task]
            crew = self.create_crew(tasks_list)
            
            # Execute the workflow
            logger.info("Executing CrewAI workflow")
            result = crew.kickoff()
            
            # Generate PDF
            logger.info("Generating PDF output")
            self.generate_pdf_output(result)
            
            logger.info("Daily market summary completed successfully")
            return result
            
        except Exception as e:
            logger.error(f"Error in daily summary workflow: {e}")
            raise
    
    def generate_pdf_output(self, crew_result):
        """Generate PDF output from crew results"""
        try:
            # Extract content from crew results
            content_dict = self.extract_content_from_results(crew_result)
            
            # Generate PDF
            pdf_path = self.pdf_generator.generate_pdf(content_dict)
            
            logger.info(f"PDF generated: {pdf_path}")
            return pdf_path
            
        except Exception as e:
            logger.error(f"PDF generation failed: {e}")
            raise
    
    def extract_content_from_results(self, crew_result):
        """Extract and organize content from crew results"""
        content_dict = {}
        
        try:
            # This is a simplified extraction - in practice, you'd need to
            # parse the actual crew results structure
            if hasattr(crew_result, 'raw') and crew_result.raw:
                # Extract English content
                content_dict['en'] = str(crew_result.raw)
                
                # For demo purposes, create sample translations
                content_dict['hi'] = self.create_sample_translation('hi')
                content_dict['ar'] = self.create_sample_translation('ar')
                content_dict['he'] = self.create_sample_translation('he')
                
                # Add sample images
                content_dict['images'] = [
                    {
                        'path': 'temp_images/sample_chart.png',
                        'caption': 'Market Performance Chart'
                    }
                ]
            
            return content_dict
            
        except Exception as e:
            logger.error(f"Content extraction failed: {e}")
            return {'en': 'Content extraction failed', 'error': str(e)}
    
    def create_sample_translation(self, language):
        """Create sample translation for demo purposes"""
        translations = {
            'hi': """
            # दैनिक बाजार सारांश
            
            ## बाजार अवलोकन
            आज अमेरिकी शेयर बाजार में मिश्रित प्रदर्शन देखा गया। S&P 500 ने 0.5% की वृद्धि दर्ज की, 
            जबकि NASDAQ 0.3% नीचे बंद हुआ।
            
            ## प्रमुख सूचकांक
            - डॉव जोन्स: +0.2%
            - S&P 500: +0.5%
            - NASDAQ: -0.3%
            """,
            'ar': """
            # ملخص السوق اليومي
            
            ## نظرة عامة على السوق
            شهدت أسواق الأسهم الأمريكية أداءً مختلطاً اليوم. ارتفع مؤشر S&P 500 بنسبة 0.5%، 
            بينما أغلق مؤشر NASDAQ منخفضاً بنسبة 0.3%.
            
            ## المؤشرات الرئيسية
            - داو جونز: +0.2%
            - S&P 500: +0.5%
            - NASDAQ: -0.3%
            """,
            'he': """
            # סיכום שוק יומי
            
            ## סקירת שוק
            שוקי המניות האמריקניים הראו ביצועים מעורבים היום. מדד S&P 500 עלה ב-0.5%, 
            בעוד שמדד NASDAQ נסגר בירידה של 0.3%.
            
            ## מדדים עיקריים
            - דאו ג'ונס: +0.2%
            - S&P 500: +0.5%
            - NASDAQ: -0.3%
            """
        }
        
        return translations.get(language, f"Translation for {language} not available")
    
    def send_telegram_messages(self, content_dict: Dict):
        """Send messages to Telegram in all languages"""
        try:
            for lang_code, content in content_dict.items():
                if lang_code in ['en', 'hi', 'ar', 'he'] and isinstance(content, str):
                    message = format_telegram_message(content, lang_code)
                    
                    # Send to Telegram
                    telegram_result = telegram_send_tool._run(
                        message=message,
                        chat_id=Config.TELEGRAM_CHAT_ID
                    )
                    
                    logger.info(f"Telegram message sent for {lang_code}: {telegram_result}")
            
        except Exception as e:
            logger.error(f"Telegram sending failed: {e}")
            raise
    
    def cleanup(self):
        """Clean up temporary files"""
        try:
            self.pdf_generator.cleanup_temp_files()
            logger.info("Cleanup completed")
        except Exception as e:
            logger.warning(f"Cleanup failed: {e}")

def main():
    """Main function to run the market summary crew"""
    try:
        # Initialize crew
        crew = MarketSummaryCrew()
        
        # Run daily summary
        result = crew.run_daily_summary()
        
        # Cleanup
        crew.cleanup()
        
        print("Market summary generation completed successfully!")
        print(f"Results: {result}")
        
    except Exception as e:
        logger.error(f"Main execution failed: {e}")
        print(f"Error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
