"""
Sample data generator for testing and demonstration purposes
"""

import json
import os
from datetime import datetime
from config import Config

def generate_sample_market_data():
    """Generate sample market data for testing"""
    sample_data = {
        "search_results": [
            {
                "title": "S&P 500 Rises 0.5% as Tech Stocks Lead Market Rally",
                "content": "The S&P 500 closed higher today, gaining 0.5% as technology stocks led a broad market rally. The index closed at 4,567.89, up 22.34 points from yesterday's close.",
                "url": "https://example.com/sp500-rally",
                "published_date": datetime.now().isoformat(),
                "score": 0.95
            },
            {
                "title": "Federal Reserve Holds Interest Rates Steady",
                "content": "The Federal Reserve announced today that it will maintain the current federal funds rate at 5.25-5.50%, citing ongoing inflation concerns and strong economic growth.",
                "url": "https://example.com/fed-rates",
                "published_date": datetime.now().isoformat(),
                "score": 0.92
            },
            {
                "title": "NASDAQ Dips 0.3% Despite Strong Apple Earnings",
                "content": "The NASDAQ Composite fell 0.3% today, closing at 14,234.56, despite Apple Inc. reporting better-than-expected quarterly earnings after the bell.",
                "url": "https://example.com/nasdaq-apple",
                "published_date": datetime.now().isoformat(),
                "score": 0.88
            }
        ],
        "market_data": {
            "indices": {
                "SPY": {"price": 456.78, "change": 2.34, "change_pct": 0.51},
                "QQQ": {"price": 378.45, "change": -1.12, "change_pct": -0.30},
                "DIA": {"price": 345.67, "change": 0.89, "change_pct": 0.26}
            },
            "sectors": {
                "Technology": {"performance": 0.8, "top_stocks": ["AAPL", "MSFT", "GOOGL"]},
                "Healthcare": {"performance": 0.3, "top_stocks": ["JNJ", "PFE", "UNH"]},
                "Financial": {"performance": -0.2, "top_stocks": ["JPM", "BAC", "WFC"]}
            }
        }
    }
    return sample_data

def generate_sample_summary():
    """Generate sample market summary"""
    summary = """# Daily Market Summary - December 15, 2024

## Market Overview
The US stock market showed mixed performance today, with the S&P 500 gaining 0.5% while the NASDAQ declined 0.3%. Overall market sentiment remained cautious as investors digested the Federal Reserve's latest policy decision.

## Major Indices Performance
- **S&P 500**: +0.5% (4,567.89)
- **NASDAQ Composite**: -0.3% (14,234.56)  
- **Dow Jones Industrial Average**: +0.2% (34,567.89)

## Sector Highlights
**Technology** led the market with a 0.8% gain, driven by strong earnings from major tech companies. **Healthcare** also performed well, up 0.3%, while **Financial** stocks declined 0.2% amid interest rate concerns.

## Key News
The Federal Reserve maintained interest rates at 5.25-5.50%, citing ongoing inflation concerns. Apple Inc. reported better-than-expected quarterly earnings, with revenue up 8% year-over-year.

## Currency & Commodities
The US Dollar Index rose 0.2% against major currencies. Oil prices increased 1.5% to $78.45 per barrel, while gold declined 0.8% to $2,045 per ounce.

## Market Outlook
Tomorrow's focus will be on retail sales data and continued earnings reports. Market participants will watch for any Fed commentary on future rate decisions.

---
*This summary is generated automatically and for informational purposes only.*"""
    
    return summary

def generate_sample_translations():
    """Generate sample translations"""
    translations = {
        "hi": """# दैनिक बाजार सारांश - 15 दिसंबर, 2024

## बाजार अवलोकन
अमेरिकी शेयर बाजार ने आज मिश्रित प्रदर्शन दिखाया, S&P 500 में 0.5% की वृद्धि हुई जबकि NASDAQ में 0.3% की गिरावट आई। फेडरल रिजर्व के नवीनतम नीति निर्णय को देखते हुए समग्र बाजार भावना सतर्क बनी रही।

## प्रमुख सूचकांक प्रदर्शन
- **S&P 500**: +0.5% (4,567.89)
- **NASDAQ Composite**: -0.3% (14,234.56)
- **Dow Jones Industrial Average**: +0.2% (34,567.89)

## क्षेत्र हाइलाइट्स
**प्रौद्योगिकी** ने प्रमुख तकनीकी कंपनियों के मजबूत कमाई के साथ 0.8% की वृद्धि के साथ बाजार का नेतृत्व किया। **स्वास्थ्य सेवा** ने भी अच्छा प्रदर्शन किया, 0.3% की वृद्धि, जबकि ब्याज दर की चिंताओं के बीच **वित्तीय** शेयरों में 0.2% की गिरावट आई।

---
*यह सारांश स्वचालित रूप से उत्पन्न किया गया है और केवल सूचनात्मक उद्देश्यों के लिए है।*""",
        
        "ar": """# ملخص السوق اليومي - 15 ديسمبر 2024

## نظرة عامة على السوق
أظهرت أسواق الأسهم الأمريكية أداءً مختلطاً اليوم، حيث ارتفع مؤشر S&P 500 بنسبة 0.5% بينما انخفض مؤشر NASDAQ بنسبة 0.3%. ظل المزاج العام للسوق حذراً بينما يستوعب المستثمرون أحدث قرار للاحتياطي الفيدرالي.

## أداء المؤشرات الرئيسية
- **S&P 500**: +0.5% (4,567.89)
- **NASDAQ Composite**: -0.3% (14,234.56)
- **Dow Jones Industrial Average**: +0.2% (34,567.89)

## أبرز القطاعات
قاد قطاع **التكنولوجيا** السوق بارتفاع 0.8% مدفوعاً بأرباح قوية من شركات التكنولوجيا الكبرى. كما أدى قطاع **الرعاية الصحية** أداءً جيداً بارتفاع 0.3%، بينما انخفضت أسهم **القطاع المالي** بنسبة 0.2% وسط مخاوف أسعار الفائدة.

---
*تم إنشاء هذا الملخص تلقائياً ولأغراض إعلامية فقط.*""",
        
        "he": """# סיכום שוק יומי - 15 בדצמבר 2024

## סקירת שוק
שוקי המניות האמריקניים הראו ביצועים מעורבים היום, כאשר מדד S&P 500 עלה ב-0.5% בעוד שמדד NASDAQ ירד ב-0.3%. מצב הרוח הכללי של השוק נותר זהיר בעוד המשקיעים מעכלים את ההחלטה האחרונה של הפדרל ריזרב.

## ביצועי מדדים עיקריים
- **S&P 500**: +0.5% (4,567.89)
- **NASDAQ Composite**: -0.3% (14,234.56)
- **Dow Jones Industrial Average**: +0.2% (34,567.89)

## הדגשים סקטוריאליים
סקטור **הטכנולוגיה** הוביל את השוק עם עלייה של 0.8% בזכות רווחים חזקים מחברות טכנולוגיה גדולות. גם סקטור **הבריאות** ביצע טוב עם עלייה של 0.3%, בעוד שמניות **הפיננסים** ירדו ב-0.2% על רקע חששות מריביות.

---
*סיכום זה נוצר אוטומטית ולמטרות מידע בלבד.*"""
    }
    return translations

def create_sample_outputs():
    """Create sample output files for demonstration"""
    os.makedirs(Config.OUTPUT_DIR, exist_ok=True)
    
    # Generate sample data
    market_data = generate_sample_market_data()
    summary = generate_sample_summary()
    translations = generate_sample_translations()
    
    # Save search results
    with open(os.path.join(Config.OUTPUT_DIR, 'sample_search_results.json'), 'w') as f:
        json.dump(market_data, f, indent=2)
    
    # Save summary
    with open(os.path.join(Config.OUTPUT_DIR, 'sample_market_summary.md'), 'w') as f:
        f.write(summary)
    
    # Save translations
    for lang, content in translations.items():
        with open(os.path.join(Config.OUTPUT_DIR, f'sample_summary_{lang}.md'), 'w', encoding='utf-8') as f:
            f.write(content)
    
    print("Sample output files created successfully!")
    print(f"Check the '{Config.OUTPUT_DIR}' directory for sample files.")

if __name__ == "__main__":
    create_sample_outputs()
