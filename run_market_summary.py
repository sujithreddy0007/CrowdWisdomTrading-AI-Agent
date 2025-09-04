# run_market_summary.py

import argparse
import time
from datetime import datetime
import logging
from config import Config
from market_summary_crew import MarketSummaryCrew
from utils import setup_logging, is_market_closed

def setup_environment():
    """Setup environment and validate configuration"""
    try:
        Config.validate()
        return True
    except ValueError as e:
        print(f"Configuration error: {e}")
        print("Ensure the required environment variables are set in your environment or a .env file.")
        return False

def run_summary():
    """Run the market summary generation"""
    logger = logging.getLogger(__name__)

    try:
        logger.info("=" * 50)
        logger.info("Starting Daily Market Summary Generation")
        logger.info(f"Timestamp: {datetime.now()}")
        logger.info("=" * 50)

        # Initialize and run crew
        crew = MarketSummaryCrew()
        result = crew.run_daily_summary()

        logger.info("Market summary generation completed successfully")
        if result:
            logger.info(f"Result preview: {result[:200]}...")

        # Cleanup
        crew.cleanup()

        return True

    except Exception as e:
        logger.error(f"Market summary generation failed: {e}")
        logger.exception("Full traceback:")
        return False

def schedule_daily_run():
    """Schedule the daily run at market close time"""
    try:
        import schedule
    except ModuleNotFoundError:
        print("The 'schedule' package is not installed. Install it with: pip install schedule")
        return

    schedule.every().day.at("16:30").do(run_summary)

    print("Scheduled daily market summary at 4:30 PM EST")
    print("Press Ctrl+C to stop the scheduler")

    try:
        while True:
            schedule.run_pending()
            time.sleep(60)
    except KeyboardInterrupt:
        print("\nScheduler stopped by user")

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description="Daily Market Summary Generator")
    parser.add_argument("--mode", choices=["once", "schedule", "test"], default="once", help="Run mode")
    parser.add_argument("--force", action="store_true", help="Force run even if market is open")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose logging")

    args = parser.parse_args()

    log_level = logging.DEBUG if args.verbose else logging.INFO
    logger = setup_logging()
    logger.setLevel(log_level)

    if not setup_environment():
        return 1

    if args.mode == "test":
        print("Configuration validation passed!")
        return 0

    if not args.force and not is_market_closed():
        print("Warning: US market appears to be open.")
        print("Use --force to run anyway, or wait for market close.")
        response = input("Continue anyway? (y/N): ")
        if response.lower() != 'y':
            return 0

    if args.mode == "once":
        success = run_summary()
        return 0 if success else 1
    elif args.mode == "schedule":
        schedule_daily_run()
        return 0

    return 0

if __name__ == "__main__":
    exit(main())