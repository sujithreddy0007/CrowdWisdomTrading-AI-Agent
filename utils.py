import os
import logging
from datetime import datetime, timezone
import pytz
from typing import List, Dict, Any
import requests
from PIL import Image
import io

def setup_logging():
    """Set up logging configuration"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('market_summary.log'),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)

def get_market_close_time():
    """Get the time when US market closes (4:00 PM EST/EDT)"""
    ny_tz = pytz.timezone('America/New_York')
    now = datetime.now(ny_tz)
    
    # Market closes at 4:00 PM EST/EDT
    market_close = now.replace(hour=16, minute=0, second=0, microsecond=0)
    
    # If it's before market close today, use today's close
    # Otherwise, use tomorrow's close
    if now.time() < market_close.time():
        return market_close
    else:
        from datetime import timedelta
        return market_close + timedelta(days=1)

def is_market_closed():
    """Check if US market is currently closed"""
    ny_tz = pytz.timezone('America/New_York')
    now = datetime.now(ny_tz)
    
    # Market is closed on weekends
    if now.weekday() >= 5:  # Saturday = 5, Sunday = 6
        return True
    
    # Market hours: 9:30 AM - 4:00 PM EST/EDT
    market_open = now.replace(hour=9, minute=30, second=0, microsecond=0)
    market_close = now.replace(hour=16, minute=0, second=0, microsecond=0)
    
    return not (market_open.time() <= now.time() <= market_close.time())

def download_image(url: str, max_size: tuple = (800, 600)) -> str:
    """Download and resize an image from URL"""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        # Open image and resize
        img = Image.open(io.BytesIO(response.content))
        img.thumbnail(max_size, Image.Resampling.LANCZOS)
        
        # Save to local file
        filename = f"temp_image_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
        filepath = os.path.join('temp_images', filename)
        os.makedirs('temp_images', exist_ok=True)
        
        img.save(filepath, 'JPEG', quality=85)
        return filepath
    except Exception as e:
        logging.error(f"Failed to download image from {url}: {e}")
        return None

def clean_text(text: str) -> str:
    """Clean and format text for better readability"""
    if not text:
        return ""
    
    # Remove extra whitespace
    text = ' '.join(text.split())
    
    # Remove special characters that might cause issues
    text = text.replace('\x00', '').replace('\ufffd', '')
    
    return text.strip()

def validate_summary(summary: str, max_words: int = 500) -> bool:
    """Validate that summary meets requirements"""
    if not summary:
        return False
    
    word_count = len(summary.split())
    if word_count > max_words:
        return False
    
    # Check for required sections
    required_keywords = ['market', 'stock', 'index', 'trading']
    has_required_content = any(keyword in summary.lower() for keyword in required_keywords)
    
    return has_required_content

def format_telegram_message(content: str, language: str = 'en') -> str:
    """Format content for Telegram with proper markdown"""
    # Escape special characters for Telegram markdown
    content = content.replace('*', '\\*').replace('_', '\\_').replace('[', '\\[').replace(']', '\\]')
    
    # Add language indicator
    language_names = {
        'en': '🇺🇸 English',
        'hi': '🇮🇳 Hindi',
        'ar': '🇸🇦 Arabic',
        'he': '🇮🇱 Hebrew'
    }
    
    header = f"📈 **Daily Market Summary** - {language_names.get(language, language.upper())}\n\n"
    return header + content
