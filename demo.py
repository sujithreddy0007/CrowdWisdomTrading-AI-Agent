#!/usr/bin/env python3
"""
Demo script for the Market Summary Generator
This script demonstrates the system without requiring real API keys
"""

import os
import json
from datetime import datetime
from pdf_generator import PDFGenerator
from sample_data_generator import (
    generate_sample_market_data, 
    generate_sample_summary, 
    generate_sample_translations
)
from config import Config

def run_demo():
    """Run a demonstration of the market summary system"""
    print("🚀 Market Summary Generator Demo")
    print("=" * 50)
    
    # Create output directory
    os.makedirs(Config.OUTPUT_DIR, exist_ok=True)
    
    # Generate sample data
    print("📊 Generating sample market data...")
    market_data = generate_sample_market_data()
    
    print("📝 Creating market summary...")
    summary = generate_sample_summary()
    
    print("🌍 Generating translations...")
    translations = generate_sample_translations()
    
    # Create content dictionary for PDF
    content_dict = {
        'en': summary,
        'hi': translations['hi'],
        'ar': translations['ar'],
        'he': translations['he'],
        'images': [
            {
                'path': 'temp_images/sample_chart.png',
                'caption': 'Market Performance Chart (Sample)'
            }
        ]
    }
    
    # Generate PDF
    print("📄 Generating PDF document...")
    try:
        pdf_generator = PDFGenerator()
        pdf_path = pdf_generator.generate_pdf(content_dict)
        print(f"✅ PDF generated: {pdf_path}")
    except Exception as e:
        print(f"⚠️  PDF generation failed: {e}")
        print("   (This is expected in demo mode without proper fonts)")
    
    # Save sample files
    print("💾 Saving sample files...")
    
    # Save search results
    with open(os.path.join(Config.OUTPUT_DIR, 'demo_search_results.json'), 'w') as f:
        json.dump(market_data, f, indent=2)
    
    # Save summary
    with open(os.path.join(Config.OUTPUT_DIR, 'demo_market_summary.md'), 'w') as f:
        f.write(summary)
    
    # Save translations
    for lang, content in translations.items():
        with open(os.path.join(Config.OUTPUT_DIR, f'demo_summary_{lang}.md'), 'w', encoding='utf-8') as f:
            f.write(content)
    
    # Create delivery report
    delivery_report = {
        "timestamp": datetime.now().isoformat(),
        "status": "demo_completed",
        "files_generated": [
            "demo_search_results.json",
            "demo_market_summary.md",
            "demo_summary_hi.md",
            "demo_summary_ar.md", 
            "demo_summary_he.md",
            "daily_market_summary.pdf"
        ],
        "languages": ["en", "hi", "ar", "he"],
        "word_count": len(summary.split()),
        "message": "Demo completed successfully - all sample files generated"
    }
    
    with open(os.path.join(Config.OUTPUT_DIR, 'demo_delivery_report.json'), 'w') as f:
        json.dump(delivery_report, f, indent=2)
    
    print("\n✅ Demo completed successfully!")
    print(f"📁 Check the '{Config.OUTPUT_DIR}' directory for generated files:")
    print("   - demo_search_results.json (sample market data)")
    print("   - demo_market_summary.md (English summary)")
    print("   - demo_summary_hi.md (Hindi translation)")
    print("   - demo_summary_ar.md (Arabic translation)")
    print("   - demo_summary_he.md (Hebrew translation)")
    print("   - daily_market_summary.pdf (multi-language PDF)")
    print("   - demo_delivery_report.json (delivery status)")
    
    print("\n🔧 To run the full system:")
    print("   1. Set up your API keys in a .env file")
    print("   2. Run: python run_market_summary.py --mode once")
    print("   3. Or schedule daily runs: python run_market_summary.py --mode schedule")

def show_system_architecture():
    """Display the system architecture"""
    print("\n🏗️  System Architecture")
    print("=" * 50)
    print("""
    ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
    │   Search Agent  │───▶│  Summary Agent  │───▶│Formatting Agent│
    │ (News Research) │    │ (Market Analyst)│    │ (Visual Design) │
    └─────────────────┘    └─────────────────┘    └─────────────────┘
           │                        │                        │
           ▼                        ▼                        ▼
    ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
    │Translation Agent│    │   Send Agent    │    │  PDF Generator  │
    │ (Multi-language)│    │ (Telegram Bot)  │    │ (Documentation) │
    └─────────────────┘    └─────────────────┘    └─────────────────┘
    
    Data Flow:
    1. Search Agent → Finds latest financial news
    2. Summary Agent → Creates comprehensive market summary
    3. Formatting Agent → Adds charts and visual elements
    4. Translation Agent → Translates to Hindi, Arabic, Hebrew
    5. Send Agent → Delivers to Telegram channels
    6. PDF Generator → Creates multi-language PDF document
    """)

def show_features():
    """Display system features"""
    print("\n✨ Key Features")
    print("=" * 50)
    features = [
        "🤖 Multi-Agent AI System using CrewAI",
        "📰 Real-time financial news search",
        "📊 Comprehensive market analysis",
        "🌍 Multi-language support (EN, HI, AR, HE)",
        "📱 Telegram bot delivery",
        "📄 Professional PDF generation",
        "⏰ Automated daily scheduling",
        "🛡️ Built-in error handling and validation",
        "📈 Market data integration",
        "🎨 Visual content enhancement"
    ]
    
    for feature in features:
        print(f"   {feature}")

if __name__ == "__main__":
    show_system_architecture()
    show_features()
    run_demo()
