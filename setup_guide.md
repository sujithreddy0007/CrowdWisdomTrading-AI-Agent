# Setup Guide for Market Summary Generator

This guide will help you set up the Market Summary Generator system with all required API keys and configurations.

## 🔑 Required API Keys

### 1. OpenAI API Key
- **Purpose**: LLM processing for all AI agents
- **Get it**: https://platform.openai.com/api-keys
- **Cost**: Pay-per-use (GPT-4o-mini is cost-effective)
- **Usage**: All agent processing, translations, summaries

### 2. Tavily API Key
- **Purpose**: Real-time financial news search
- **Get it**: https://tavily.com/
- **Cost**: Free tier available, paid plans for higher usage
- **Usage**: News search, image search, content discovery

### 3. Telegram Bot Token
- **Purpose**: Sending summaries to Telegram channels
- **Get it**: 
  1. Message @BotFather on Telegram
  2. Send `/newbot`
  3. Follow instructions to create your bot
  4. Copy the bot token
- **Usage**: Message delivery, multi-language distribution

### 4. Telegram Chat ID
- **Purpose**: Target channel/chat for message delivery
- **Get it**:
  1. Add your bot to a channel/group
  2. Send a message to the channel
  3. Visit: `https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates`
  4. Find the chat ID in the response
- **Usage**: Message destination

## 🛠️ Installation Steps

### Step 1: Clone and Install
```bash
git clone <your-repo-url>
cd market-summary-generator
pip install -r requirements.txt
```

### Step 2: Environment Setup
```bash
# Copy the example environment file
cp env_example.txt .env

# Edit .env with your API keys
nano .env  # or use your preferred editor
```

### Step 3: Configure .env File
```env
# Required API Keys
OPENAI_API_KEY=sk-your-openai-key-here
TAVILY_API_KEY=tvly-your-tavily-key-here
TELEGRAM_BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
TELEGRAM_CHAT_ID=-1001234567890

# Optional Configuration
GROQ_API_KEY=your-groq-key-here
MARKET_TIMEZONE=America/New_York
SUMMARY_LANGUAGE=en
TRANSLATION_LANGUAGES=hi,ar,he
MAX_SUMMARY_WORDS=500
OUTPUT_DIR=outputs
PDF_FILENAME=daily_market_summary.pdf
```

### Step 4: Test Configuration
```bash
python run_market_summary.py --mode test
```

### Step 5: Run Demo (Optional)
```bash
python demo.py
```

### Step 6: First Real Run
```bash
python run_market_summary.py --mode once --force
```

## 🔧 Telegram Bot Setup

### Creating a Telegram Bot
1. Open Telegram and search for `@BotFather`
2. Start a chat and send `/newbot`
3. Choose a name for your bot (e.g., "Market Summary Bot")
4. Choose a username (e.g., "market_summary_bot")
5. Copy the bot token provided

### Setting Up a Channel
1. Create a new Telegram channel
2. Add your bot as an administrator
3. Give the bot permission to post messages
4. Get the channel ID:
   - Forward a message from your channel to @userinfobot
   - Or use the API method described above

### Testing Telegram Integration
```python
# Test script to verify Telegram setup
import requests

BOT_TOKEN = "your_bot_token_here"
CHAT_ID = "your_chat_id_here"

url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
data = {
    "chat_id": CHAT_ID,
    "text": "Test message from Market Summary Bot!"
}

response = requests.post(url, json=data)
print(response.json())
```

## 📊 API Usage and Costs

### OpenAI API
- **Model**: GPT-4o-mini (recommended for cost efficiency)
- **Estimated Cost**: $0.01-0.05 per daily summary
- **Usage**: ~2000-5000 tokens per summary

### Tavily API
- **Free Tier**: 1000 searches/month
- **Paid Plans**: Starting at $20/month for 10,000 searches
- **Usage**: ~10-20 searches per daily summary

### Telegram API
- **Cost**: Free
- **Limits**: 30 messages/second, 20 messages/minute per bot

## 🚨 Troubleshooting

### Common Issues

#### 1. API Key Errors
```
Error: Missing required environment variables: OPENAI_API_KEY
```
**Solution**: Ensure all API keys are set in `.env` file

#### 2. Import Errors
```
ModuleNotFoundError: No module named 'crewai'
```
**Solution**: Install dependencies: `pip install -r requirements.txt`

#### 3. Telegram Delivery Issues
```
Error: Telegram send failed: Bad Request: chat not found
```
**Solution**: Verify bot token and chat ID are correct

#### 4. PDF Generation Problems
```
Error: PDF generation failed: Font not found
```
**Solution**: Install system fonts or use default fonts

### Debug Mode
Run with verbose logging to see detailed error information:
```bash
python run_market_summary.py --mode once --verbose
```

### Log Files
Check `market_summary.log` for detailed execution logs and error information.

## 🔄 Scheduling Options

### Option 1: Built-in Scheduler
```bash
python run_market_summary.py --mode schedule
```

### Option 2: System Cron (Linux/Mac)
```bash
# Edit crontab
crontab -e

# Add this line to run at 4:30 PM EST daily
30 16 * * 1-5 cd /path/to/market-summary-generator && python run_market_summary.py --mode once
```

### Option 3: Windows Task Scheduler
1. Open Task Scheduler
2. Create Basic Task
3. Set trigger to daily at 4:30 PM
4. Set action to start program: `python run_market_summary.py --mode once`

## 📈 Monitoring and Maintenance

### Log Monitoring
- Check `market_summary.log` regularly
- Monitor for API rate limit warnings
- Watch for delivery failures

### Output Verification
- Verify PDF generation in `outputs/` directory
- Check Telegram message delivery
- Validate translation quality

### API Quota Management
- Monitor OpenAI usage in dashboard
- Track Tavily search usage
- Set up billing alerts

## 🆘 Getting Help

### Support Resources
1. Check the logs in `market_summary.log`
2. Run with `--verbose` flag for detailed output
3. Test configuration with `--mode test`
4. Review the README.md for detailed documentation

### Common Commands
```bash
# Test configuration
python run_market_summary.py --mode test

# Run once with verbose output
python run_market_summary.py --mode once --verbose

# Run demo without API keys
python demo.py

# Check system status
python -c "from config import Config; Config.validate(); print('Configuration OK')"
```

---

**Note**: This system is designed to be robust and handle errors gracefully. If you encounter issues, check the logs first and ensure all API keys are correctly configured.
