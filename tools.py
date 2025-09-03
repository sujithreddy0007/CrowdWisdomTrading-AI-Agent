try:
    from crewai_tools import BaseTool  # type: ignore
    BASETOOL_AVAILABLE = True
except Exception:
    # Compatibility shim for environments where BaseTool isn't exported
    from typing import Any
    BASETOOL_AVAILABLE = False
    class BaseTool:  # minimal interface needed by CrewAI tools
        name: str = ""
        description: str = ""
        args_schema = None

        def __init__(self, *args: Any, **kwargs: Any) -> None:
            pass

        # CrewAI expects tools to expose a run method; delegate to _run
        def run(self, *args: Any, **kwargs: Any):  # noqa: D401
            return self._run(*args, **kwargs)
from typing import Type, Optional
from pydantic import BaseModel, Field
import requests
import json
import logging
from datetime import datetime
import yfinance as yf
import matplotlib.pyplot as plt
import os
from config import Config
from utils import download_image, clean_text

logger = logging.getLogger(__name__)

# ---------------- Tavily Search ---------------- #
class TavilySearchInput(BaseModel):
    query: str = Field(..., description="Search query for financial news")
    max_results: int = Field(default=10, description="Maximum number of results to return")

class TavilySearchTool(BaseTool):
    name: str = "tavily_financial_search"
    description: str = "Search for the latest US financial market news using Tavily API"
    args_schema: Type[BaseModel] = TavilySearchInput

    def _run(self, query: str, max_results: int = 10) -> str:
        """Search for financial news using Tavily API"""

        try:
            url = "https://api.tavily.com/search"
            payload = {
                "api_key": Config.TAVILY_API_KEY,
                "query": query,
                "search_depth": "advanced",
                "include_answer": True,
                "include_images": True,
                "include_raw_content": False,
                "max_results": max_results,
                "include_domains": [
                    "reuters.com", "bloomberg.com", "cnbc.com", "marketwatch.com",
                    "wsj.com", "ft.com", "yahoo.com/finance", "investing.com"
                ]
            }
            
            response = requests.post(url, json=payload, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            
            # Format the results
            results = []
            if 'results' in data:
                for item in data['results']:
                    result = {
                        'title': item.get('title', ''),
                        'url': item.get('url', ''),
                        'content': item.get('content', ''),
                        'published_date': item.get('published_date', ''),
                        'score': item.get('score', 0)
                    }
                    results.append(result)
            
            # Include AI summary if available
            if 'answer' in data and data['answer']:
                results.insert(0, {
                    'title': 'AI Summary',
                    'content': data['answer'],
                    'url': '',
                    'published_date': datetime.now().isoformat(),
                    'score': 1.0
                })
            
            return json.dumps(results, indent=2)
            
        except Exception as e:
            logger.error(f"Tavily search failed: {e}")
            return json.dumps([{"error": f"Search failed: {str(e)}"}])

# ---------------- Market Data ---------------- #
class MarketDataInput(BaseModel):
    symbols: str = Field(..., description="Comma-separated list of stock symbols (e.g., 'AAPL,MSFT,GOOGL')")
    period: str = Field(default="1d", description="Time period for data (1d, 5d, 1mo, etc.)")

class MarketDataTool(BaseTool):
    name: str = "market_data_fetcher"
    description: str = "Fetch real-time market data and create charts for stocks and indices"
    args_schema: Type[BaseModel] = MarketDataInput

    def _run(self, symbols: str, period: str = "1d") -> str:
        """Fetch market data and create charts"""
        try:
            os.makedirs("temp_images", exist_ok=True)  # ensure folder exists
            symbol_list = [s.strip().upper() for s in symbols.split(',')]
            results = {}
            
            for symbol in symbol_list:
                try:
                    ticker = yf.Ticker(symbol)
                    hist = ticker.history(period=period)
                    
                    if not hist.empty:
                        # Get current price
                        current_price = hist['Close'].iloc[-1]
                        prev_close = hist['Close'].iloc[-2] if len(hist) > 1 else current_price
                        change = current_price - prev_close
                        change_pct = (change / prev_close) * 100 if prev_close else 0
                        
                        # Create simple chart
                        plt.figure(figsize=(10, 6))
                        plt.plot(hist.index, hist['Close'], linewidth=2)
                        plt.title(f'{symbol} - {period} Performance')
                        plt.xlabel('Time')
                        plt.ylabel('Price ($)')
                        plt.grid(True, alpha=0.3)
                        plt.xticks(rotation=45)
                        plt.tight_layout()
                        
                        # Save chart
                        chart_filename = f"chart_{symbol}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
                        chart_path = f"temp_images/{chart_filename}"
                        plt.savefig(chart_path, dpi=150, bbox_inches='tight')
                        plt.close()
                        
                        results[symbol] = {
                            'current_price': round(current_price, 2),
                            'change': round(change, 2),
                            'change_percent': round(change_pct, 2),
                            'chart_path': chart_path,
                            'volume': int(hist['Volume'].iloc[-1]) if 'Volume' in hist.columns else 0
                        }
                        
                except Exception as e:
                    logger.error(f"Failed to fetch data for {symbol}: {e}")
                    results[symbol] = {'error': str(e)}
            
            return json.dumps(results, indent=2)
            
        except Exception as e:
            logger.error(f"Market data fetch failed: {e}")
            return json.dumps({"error": f"Market data fetch failed: {str(e)}"})

# ---------------- Image Search ---------------- #
class ImageSearchInput(BaseModel):
    query: str = Field(..., description="Search query for financial images")
    max_results: int = Field(default=3, description="Maximum number of images to return")

class ImageSearchTool(BaseTool):
    name: str = "financial_image_search"
    description: str = "Search for relevant financial images and charts"
    args_schema: Type[BaseModel] = ImageSearchInput

    def _run(self, query: str, max_results: int = 3) -> str:
        """Search for financial images using Tavily"""
        try:
            url = "https://api.tavily.com/search"
            payload = {
                "api_key": Config.TAVILY_API_KEY,
                "query": f"{query} chart graph financial",
                "search_depth": "basic",
                "include_images": True,
                "max_results": max_results,
                "include_domains": [
                    "tradingview.com", "investing.com", "marketwatch.com",
                    "bloomberg.com", "reuters.com", "cnbc.com"
                ]
            }
            
            response = requests.post(url, json=payload, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            
            images = []
            if 'images' in data:
                for img_url in data['images'][:max_results]:
                    try:
                        # Download and save image
                        local_path = download_image(img_url)
                        if local_path:
                            images.append({
                                'url': img_url,
                                'local_path': local_path,
                                'description': f"Financial chart related to {query}"
                            })
                    except Exception as e:
                        logger.error(f"Failed to process image {img_url}: {e}")
            
            return json.dumps(images, indent=2)
            
        except Exception as e:
            logger.error(f"Image search failed: {e}")
            return json.dumps([{"error": f"Image search failed: {str(e)}"}])

# ---------------- Telegram Sender ---------------- #
class TelegramSendInput(BaseModel):
    message: str = Field(..., description="Message content to send")
    chat_id: str = Field(..., description="Telegram chat ID or @channelusername")
    image_path: Optional[str] = Field(None, description="Path to image file to send")

class TelegramSendTool(BaseTool):
    name: str = "telegram_sender"
    description: str = "Send messages and images to Telegram channel"
    args_schema: Type[BaseModel] = TelegramSendInput

    def _run(self, message: str, chat_id: str, image_path: Optional[str] = None) -> str:
        """Send message to Telegram"""
        try:
            bot_token = Config.TELEGRAM_BOT_TOKEN
            base_url = f"https://api.telegram.org/bot{bot_token}"
            
            if image_path:
                # Send photo with caption
                url = f"{base_url}/sendPhoto"
                with open(image_path, 'rb') as photo:
                    files = {'photo': photo}
                    data = {
                        'chat_id': chat_id,
                        'caption': message,
                        'parse_mode': 'Markdown'
                    }
                    response = requests.post(url, files=files, data=data, timeout=30)
            else:
                # Send text message
                url = f"{base_url}/sendMessage"
                data = {
                    'chat_id': chat_id,
                    'text': message,
                    'parse_mode': 'Markdown'
                }
                response = requests.post(url, json=data, timeout=30)
            
            response.raise_for_status()
            result = response.json()
            
            if result.get('ok'):
                return json.dumps({"success": True, "message_id": result['result']['message_id']})
            else:
                return json.dumps({"success": False, "error": result.get('description', 'Unknown error')})
                
        except Exception as e:
            logger.error(f"Telegram send failed: {e}")
            return json.dumps({"success": False, "error": str(e)})

# ---------------- Tool Instances ---------------- #
tavily_search_tool = TavilySearchTool()
market_data_tool = MarketDataTool()
image_search_tool = ImageSearchTool()
telegram_send_tool = TelegramSendTool()
