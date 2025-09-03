# Daily Market Summary Generator

A CrewAI-based system that automatically generates and delivers daily financial market summaries after the US stock market closes. The system uses multiple AI agents working together to search for news, create summaries, add visual elements, translate content, and deliver it via Telegram and PDF.

## 🚀 Features

- **Automated Daily Generation**: Runs automatically after US market close (~4:30 PM EST)
- **Multi-Agent Architecture**: Uses CrewAI to orchestrate specialized AI agents
- **Comprehensive Coverage**: Covers major indices, sectors, economic news, and market analysis
- **Multi-Language Support**: Translates summaries into Hindi, Arabic, and Hebrew
- **Visual Enhancement**: Includes relevant charts and financial images
- **Multiple Delivery Methods**: Telegram bot and PDF generation
- **Professional Formatting**: Clean, corporate-style output suitable for distribution

## 🏗️ Architecture

The system uses a team of specialized AI agents:

### 1. **Search Agent** (Financial News Researcher)
- Searches for latest US financial news using Tavily API
- Focuses on major indices, Fed announcements, economic indicators
- Prioritizes recent news (last 6-8 hours) from authoritative sources

### 2. **Summary Agent** (Financial Market Analyst)
- Creates comprehensive market summaries under 500 words
- Covers market performance, sector movements, key news
- Maintains professional, accessible tone

### 3. **Formatting Agent** (Content Designer)
- Enhances content with relevant charts and images
- Ensures professional presentation and layout
- Optimizes for multiple delivery platforms

### 4. **Translation Agent** (Multilingual Translator)
- Translates content into Hindi, Arabic, and Hebrew
- Preserves financial terminology and formatting
- Maintains cultural appropriateness

### 5. **Send Agent** (Content Delivery Specialist)
- Delivers content to Telegram channels
- Handles multi-language distribution
- Manages delivery confirmation and error handling

## 📋 Prerequisites

- Python 3.8 or higher
- API keys for:
  - OpenAI (for LLM processing)
  - Tavily (for news search)
  - Telegram Bot (for delivery)

## 🛠️ Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd market-summary-generator
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**:
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

4. **Configure API keys** in `.env`:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   TAVILY_API_KEY=your_tavily_api_key_here
   TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
   TELEGRAM_CHAT_ID=your_telegram_chat_id_here
   ```

## 🚀 Usage

### Single Run
```bash
python run_market_summary.py --mode once
```

### Scheduled Daily Run
```bash
python run_market_summary.py --mode schedule
```

### Test Configuration
```bash
python run_market_summary.py --mode test
```

### Force Run (even if market is open)
```bash
python run_market_summary.py --mode once --force
```

### Verbose Logging
```bash
python run_market_summary.py --mode once --verbose
```

## 📁 Project Structure

```
market-summary-generator/
├── agents.py                 # CrewAI agent definitions
├── tasks.py                  # Task definitions with guardrails
├── tools.py                  # Custom tools for agents
├── market_summary_crew.py    # Main CrewAI orchestration
├── pdf_generator.py          # PDF generation utilities
├── config.py                 # Configuration management
├── utils.py                  # Utility functions
├── run_market_summary.py     # Main runner script
├── requirements.txt          # Python dependencies
├── README.md                 # This file
└── outputs/                  # Generated outputs
    ├── daily_market_summary.pdf
    ├── search_results.json
    ├── market_summary.md
    └── delivery_report.json
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `OPENAI_API_KEY` | OpenAI API key for LLM processing | Yes |
| `TAVILY_API_KEY` | Tavily API key for news search | Yes |
| `TELEGRAM_BOT_TOKEN` | Telegram bot token | Yes |
| `TELEGRAM_CHAT_ID` | Telegram chat/channel ID | Yes |
| `GROQ_API_KEY` | Groq API key (optional) | No |

### Customization

Edit `config.py` to customize:
- Summary word limit (default: 500 words)
- Translation languages
- News search queries
- Output directory
- Market timezone

## 📊 Output Formats

### 1. Telegram Messages
- Formatted with Markdown
- Includes language indicators
- Supports images and charts
- Multi-language delivery

### 2. PDF Document
- Professional layout
- Multi-language sections
- Embedded charts and images
- Print-ready quality

### 3. JSON Data
- Raw search results
- Structured market data
- Delivery confirmations
- Error logs

## 🔍 Guardrails and Validation

The system includes multiple validation layers:

1. **Content Validation**:
   - Word count limits (max 500 words)
   - Required financial keywords
   - Source credibility checks

2. **Data Validation**:
   - Market data accuracy
   - Image quality checks
   - Translation completeness

3. **Delivery Validation**:
   - Telegram message formatting
   - PDF generation success
   - Error handling and retries

## 🚨 Error Handling

The system includes comprehensive error handling:

- **API Failures**: Automatic retries with exponential backoff
- **Content Issues**: Fallback content generation
- **Delivery Problems**: Multiple delivery attempts
- **Logging**: Detailed logs for debugging

## 📈 Monitoring and Logging

- **Log Files**: `market_summary.log`
- **Output Tracking**: JSON reports for each run
- **Error Alerts**: Detailed error logging
- **Performance Metrics**: Execution time tracking

## 🔄 Scheduling

The system can be scheduled to run automatically:

- **Default**: 4:30 PM EST (30 minutes after market close)
- **Customizable**: Modify schedule in `run_market_summary.py`
- **Market Hours**: Automatic market status checking

## 🧪 Testing

### Configuration Test
```bash
python run_market_summary.py --mode test
```

### Manual Run
```bash
python run_market_summary.py --mode once --force
```

### Verbose Debugging
```bash
python run_market_summary.py --mode once --verbose
```

## 🛡️ Security Considerations

- **API Keys**: Store securely in environment variables
- **Rate Limiting**: Built-in API rate limit handling
- **Data Privacy**: No sensitive data storage
- **Error Logging**: Sanitized error messages

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Troubleshooting

### Common Issues

1. **API Key Errors**:
   - Verify all API keys are correctly set
   - Check API key permissions and quotas

2. **Import Errors**:
   - Ensure all dependencies are installed
   - Check Python version compatibility

3. **Telegram Delivery Issues**:
   - Verify bot token and chat ID
   - Check bot permissions in the channel

4. **PDF Generation Problems**:
   - Ensure write permissions in output directory
   - Check font availability for different languages

### Getting Help

- Check the logs in `market_summary.log`
- Run with `--verbose` flag for detailed output
- Verify configuration with `--mode test`

## 🔮 Future Enhancements

- [ ] YouTube video integration for news
- [ ] Additional language support
- [ ] Custom chart generation
- [ ] Email delivery option
- [ ] Web dashboard for monitoring
- [ ] Advanced market analysis features

---

**Note**: This system is designed for educational and informational purposes. Always verify financial information from multiple sources before making investment decisions.
