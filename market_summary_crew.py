# market_summary_crew.py (FINAL, FINAL VERSION)

import os
import logging
import time
from typing import Dict

from crewai import Crew, Task
from agents import MarketAgents
from tasks import MarketTasks
from tools import tavily_search_tool, market_data_tool, image_search_tool, telegram_send_tool, BASETOOL_AVAILABLE
from pdf_generator import PDFGenerator
from config import Config
from utils import setup_logging

logger = setup_logging()

class MarketSummaryCrew:
    def __init__(self):
        Config.validate()
        if not os.getenv("GROQ_API_KEY"):
            os.environ["GROQ_API_KEY"] = Config.GROQ_API_KEY

        self.agents = MarketAgents()
        self.tasks = MarketTasks()
        self.pdf_generator = PDFGenerator()
        os.makedirs(Config.OUTPUT_DIR, exist_ok=True)

        self.search_agent = self.agents.create_search_agent()
        self.summary_agent = self.agents.create_summary_agent()
        self.formatting_agent = self.agents.create_formatting_agent()
        self.translation_agent = self.agents.create_translation_agent()
        self.send_agent = self.agents.create_send_agent()

        if BASETOOL_AVAILABLE:
            self.search_agent.tools = [tavily_search_tool, market_data_tool]
            self.formatting_agent.tools = [image_search_tool, market_data_tool]
            self.send_agent.tools = [telegram_send_tool]
        else:
            logger.warning("crewai_tools.BaseTool not available; skipping tool attachment.")
        logger.info("Market Summary Crew initialized successfully")

    def run_daily_summary(self):
        """
        Runs the workflow by executing tasks MANUALLY with delays.
        This is the key fix to avoid rate limiting.
        """
        try:
            logger.info("Starting manual task execution to avoid rate limits.")

            # --- Step 1: Search ---
            logger.info("Executing Search Task...")
            search_task = self.tasks.create_search_task(self.search_agent)
            search_result = search_task.execute_sync(agent=self.search_agent)
            logger.info("Search Task completed.")
            time.sleep(25)

            # --- Step 2: Summarize ---
            logger.info("Executing Summary Task...")
            summary_task = self.tasks.create_summary_task(self.summary_agent)
            summary_result = summary_task.execute_sync(
                agent=self.summary_agent,
                context=search_result.raw  # <-- ADDED .raw
            )
            logger.info("Summary Task completed.")
            time.sleep(25)

            # --- Step 3: Format ---
            logger.info("Executing Formatting Task...")
            formatting_task = self.tasks.create_formatting_task(self.formatting_agent)
            formatted_result = formatting_task.execute_sync(
                agent=self.formatting_agent,
                context=summary_result.raw  # <-- ADDED .raw
            )
            logger.info("Formatting Task completed.")

            # --- Step 4: Translate (in a loop with delays) ---
            translations = {'en': formatted_result.raw} # <-- ADDED .raw
            for lang in Config.TRANSLATION_LANGUAGES:
                time.sleep(25)
                logger.info(f"Executing Translation Task for: {lang.upper()}")
                translation_task = self.tasks.create_translation_task(self.translation_agent, lang=lang)
                translated_text = translation_task.execute_sync(
                    agent=self.translation_agent,
                    context=formatted_result.raw  # <-- ADDED .raw
                )
                translations[lang] = translated_text.raw # <-- ADDED .raw
                logger.info(f"Translation to {lang.upper()} completed.")

            # --- Step 5: Finalize & Generate PDF ---
            final_output = "\n\n---\n\n".join([f"Language: {lang}\n\n{text}" for lang, text in translations.items()])

            logger.info("Generating PDF output")
            self.generate_pdf_output(translations)

            logger.info("Daily market summary workflow finished successfully.")
            return final_output

        except Exception as e:
            logger.error(f"Error in daily summary workflow: {e}")
            raise

    def generate_pdf_output(self, all_translations: Dict):
        """Generate PDF output from the collected translation results."""
        try:
            pdf_path = self.pdf_generator.generate_pdf(all_translations)
            logger.info(f"PDF generated: {pdf_path}")
            return pdf_path
        except Exception as e:
            logger.error(f"PDF generation failed: {e}")
            raise

    def cleanup(self):
        """Clean up temporary files"""
        try:
            self.pdf_generator.cleanup_temp_files()
            logger.info("Cleanup completed")
        except Exception as e:
            logger.warning(f"Cleanup failed: {e}")