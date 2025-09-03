# Quick Start Guide

Get the Market Summary Generator running in 5 minutes!

## 🚀 Quick Setup

### 1. Install Dependencies
```bash
python install.py
```

### 2. Get API Keys
- **OpenAI**: https://platform.openai.com/api-keys
- **Tavily**: https://tavily.com/
- **Telegram**: Message @BotFather on Telegram

### 3. Configure Environment
```bash
# Edit .env file with your API keys
nano .env
```

### 4. Test Configuration
```bash
python run_market_summary.py --mode test
```

### 5. Run Demo
```bash
python demo.py
```

### 6. First Real Run
```bash
python run_market_summary.py --mode once --force
```

## 📋 Required API Keys

| Service | Purpose | Get It |
|---------|---------|--------|
| OpenAI | AI processing | [platform.openai.com](https://platform.openai.com/api-keys) |
| Tavily | News search | [tavily.com](https://tavily.com/) |
| Telegram | Message delivery | Message @BotFather |

## 🎯 What You Get

- **Daily Market Summaries**: Comprehensive analysis after market close
- **Multi-Language**: English, Hindi, Arabic, Hebrew
- **Visual Content**: Charts and financial images
- **Telegram Delivery**: Automated bot messages
- **PDF Reports**: Professional multi-language documents

## 🔧 Troubleshooting

### Common Issues
- **Import errors**: Run `pip install -r requirements.txt`
- **API errors**: Check your .env file
- **Telegram issues**: Verify bot token and chat ID

### Get Help
```bash
# Test everything
python run_market_summary.py --mode test

# Run with verbose output
python run_market_summary.py --mode once --verbose

# Check logs
cat market_summary.log
```

## 📚 Full Documentation

- [README.md](README.md) - Complete documentation
- [setup_guide.md](setup_guide.md) - Detailed setup instructions
- [demo.py](demo.py) - See it in action

---

**Ready to go?** Run `python install.py` to get started!
