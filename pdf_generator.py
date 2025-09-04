# pdf_generator.py (TYPO FIXED)

import os
import re
import logging
from datetime import datetime
from typing import Dict, List
import requests
from PIL import Image as PILImage
from io import BytesIO

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor

# Setup logging
logger = logging.getLogger(__name__)

# Define colors
PRIMARY_COLOR = HexColor("#1a73e8")
TEXT_COLOR = HexColor("#202124")
GRAY_COLOR = HexColor("#5f6368")

class PDFGenerator:
    def __init__(self, output_dir: str = "output"):
        self.output_dir = output_dir
        self.temp_image_paths = []
        self._register_fonts()
        self.styles = self._create_styles()
        os.makedirs(self.output_dir, exist_ok=True)

    def _register_fonts(self):
        """Register fonts needed for multilingual support."""
        font_map = {
            'NotoSansArabic': 'fonts/NotoSansArabic-Regular.ttf',
            'NotoSansHebrew': 'fonts/NotoSansHebrew-Regular.ttf',
            'NotoSansDevanagari': 'fonts/NotoSansDevanagari-Regular.ttf'
        }
        for name, path in font_map.items():
            try:
                if os.path.exists(path):
                    pdfmetrics.registerFont(TTFont(name, path))
                else:
                    raise FileNotFoundError
            except Exception:
                logger.warning(
                    f"Font not found: {path}. "
                    f"Please download it and place it in the '{os.path.dirname(path)}' directory "
                    f"for proper {name.replace('NotoSans', '')} language support in the PDF."
                )

    def _create_styles(self) -> Dict:
        """Create ParagraphStyle objects for the PDF."""
        styles = getSampleStyleSheet()  # <-- TYPO FIXED HERE
        styles.add(ParagraphStyle(
            name='TitleStyle',
            fontName='Helvetica-Bold',
            fontSize=24,
            leading=28,
            textColor=PRIMARY_COLOR,
            alignment=TA_CENTER,
            spaceAfter=20
        ))
        styles.add(ParagraphStyle(
            name='LangHeaderStyle',
            fontName='Helvetica-Bold',
            fontSize=16,
            leading=20,
            textColor=TEXT_COLOR,
            spaceBefore=20,
            spaceAfter=10
        ))
        # Base body style for English
        styles.add(ParagraphStyle(
            name='BodyStyle',
            fontName='Helvetica',
            fontSize=10,
            leading=14,
            textColor=GRAY_COLOR,
            spaceAfter=12
        ))
        # Styles for other languages, falling back to Helvetica if font is missing
        styles.add(ParagraphStyle(
            name='BodyStyle_ar',
            parent=styles['BodyStyle'],
            fontName='NotoSansArabic' if 'NotoSansArabic' in pdfmetrics.getRegisteredFontNames() else 'Helvetica',
            alignment=TA_RIGHT
        ))
        styles.add(ParagraphStyle(
            name='BodyStyle_he',
            parent=styles['BodyStyle'],
            fontName='NotoSansHebrew' if 'NotoSansHebrew' in pdfmetrics.getRegisteredFontNames() else 'Helvetica',
            alignment=TA_RIGHT
        ))
        styles.add(ParagraphStyle(
            name='BodyStyle_hi',
            parent=styles['BodyStyle'],
            fontName='NotoSansDevanagari' if 'NotoSansDevanagari' in pdfmetrics.getRegisteredFontNames() else 'Helvetica',
            alignment=TA_LEFT
        ))
        return styles

    def _fetch_image(self, url: str) -> Image:
        """Fetch an image from a URL and prepare it for the PDF."""
        try:
            # Add a browser-like header to avoid being blocked
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
            response = requests.get(url, timeout=10, headers=headers) # <-- ADDED headers
            response.raise_for_status()
            img_data = BytesIO(response.content)

            # Create a temporary file to save the image
            ext = PILImage.open(img_data).format.lower()
            temp_path = f"temp_image.{ext}"
            with open(temp_path, "wb") as f:
                f.write(img_data.getvalue())
            self.temp_image_paths.append(temp_path)

            # Create ReportLab Image, preserving aspect ratio
            img = Image(temp_path, width=4*inch, height=3*inch, kind='proportional')
            img.hAlign = 'CENTER'
            return img
        except Exception as e:
            logger.error(f"Could not fetch or process image from {url}: {e}")
            return None

    def _parse_markdown(self, text: str, style: ParagraphStyle) -> List:
        """Parse markdown text into a list of ReportLab Flowables."""
        flowables = []
        lines = text.split('\n')

        for line in lines:
            line = line.strip()
            if not line:
                continue

            # Handle images: ![alt](url)
            img_match = re.match(r'!\[.*?\]\((.*?)\)', line)
            if img_match:
                img_url = img_match.group(1)
                img = self._fetch_image(img_url)
                if img:
                    flowables.append(img)
                continue

            # Handle headings: # Title
            if line.startswith('# '):
                heading_text = line[2:]
                flowables.append(Paragraph(heading_text, self.styles['LangHeaderStyle']))
                continue

            # Handle bullet points: * point
            if line.startswith('* '):
                line = f"• {line[2:]}" # Replace markdown '*' with a bullet character

            flowables.append(Paragraph(line, style))

        return flowables

    def generate_pdf(self, all_translations: Dict) -> str:
        """Generate the PDF from the provided translations."""
        try:
            date_str = datetime.now().strftime("%Y-%m-%d")
            file_path = os.path.join(self.output_dir, f"market_summary_{date_str}.pdf")

            doc = SimpleDocTemplate(file_path, pagesize=(8.5 * inch, 11 * inch))
            story = []

            # Add main title
            story.append(Paragraph("Daily Market Summary", self.styles['TitleStyle']))
            story.append(Spacer(1, 0.25 * inch))

            language_map = {
                'en': 'English', 'hi': 'Hindi', 'ar': 'Arabic', 'he': 'Hebrew'
            }

            for lang_code, text in all_translations.items():
                if not text:
                    continue

                lang_name = language_map.get(lang_code, lang_code.upper())
                story.append(Paragraph(f"Summary in {lang_name}", self.styles['LangHeaderStyle']))

                body_style_name = f"BodyStyle_{lang_code}"
                body_style = self.styles.get(body_style_name, self.styles['BodyStyle'])

                # Parse markdown content
                content_flowables = self._parse_markdown(text, body_style)
                story.extend(content_flowables)
                story.append(Spacer(1, 0.25 * inch))

            doc.build(story)
            logger.info(f"Successfully generated PDF: {file_path}")
            return file_path
        except Exception as e:
            logger.error(f"PDF generation failed: {e}")
            raise
        finally:
            self.cleanup_temp_files()

    def cleanup_temp_files(self):
        """Remove temporary image files."""
        for path in self.temp_image_paths:
            try:
                if os.path.exists(path):
                    os.remove(path)
            except Exception as e:
                logger.warning(f"Failed to remove temporary file {path}: {e}")
        self.temp_image_paths = []