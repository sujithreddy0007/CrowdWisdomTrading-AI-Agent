from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from datetime import datetime
import os
import logging
from typing import Dict, List
from config import Config

logger = logging.getLogger(__name__)

class PDFGenerator:
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self.setup_fonts()
        self.setup_custom_styles()
    
    def setup_fonts(self):
        """Setup fonts for different languages"""
        try:
            # Try to register system fonts for better language support
            # These paths might need adjustment based on the system
            font_paths = {
                'DejaVuSans': '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
                'DejaVuSans-Bold': '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',
                'NotoSansArabic': '/usr/share/fonts/truetype/noto/NotoSansArabic-Regular.ttf',
                'NotoSansHebrew': '/usr/share/fonts/truetype/noto/NotoSansHebrew-Regular.ttf',
                'NotoSansDevanagari': '/usr/share/fonts/truetype/noto/NotoSansDevanagari-Regular.ttf'
            }
            
            for font_name, font_path in font_paths.items():
                if os.path.exists(font_path):
                    pdfmetrics.registerFont(TTFont(font_name, font_path))
                    logger.info(f"Registered font: {font_name}")
                else:
                    logger.warning(f"Font not found: {font_path}")
                    
        except Exception as e:
            logger.warning(f"Font setup failed, using default fonts: {e}")
    
    def setup_custom_styles(self):
        """Setup custom paragraph styles"""
        # Title style
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Title'],
            fontSize=24,
            spaceAfter=30,
            alignment=TA_CENTER,
            textColor=colors.darkblue
        ))
        
        # Subtitle style
        self.styles.add(ParagraphStyle(
            name='CustomSubtitle',
            parent=self.styles['Heading1'],
            fontSize=18,
            spaceAfter=20,
            alignment=TA_CENTER,
            textColor=colors.darkblue
        ))
        
        # Language header style
        self.styles.add(ParagraphStyle(
            name='LanguageHeader',
            parent=self.styles['Heading2'],
            fontSize=16,
            spaceAfter=15,
            spaceBefore=20,
            textColor=colors.darkred,
            borderWidth=1,
            borderColor=colors.grey,
            borderPadding=10
        ))
        
        # Content style
        self.styles.add(ParagraphStyle(
            name='CustomContent',
            parent=self.styles['Normal'],
            fontSize=11,
            spaceAfter=12,
            alignment=TA_JUSTIFY,
            leftIndent=0,
            rightIndent=0
        ))
        
        # Arabic/Hebrew content style (right-to-left)
        self.styles.add(ParagraphStyle(
            name='RTLContent',
            parent=self.styles['Normal'],
            fontSize=11,
            spaceAfter=12,
            alignment=TA_RIGHT,
            leftIndent=0,
            rightIndent=0
        ))
        
        # Footer style
        self.styles.add(ParagraphStyle(
            name='Footer',
            parent=self.styles['Normal'],
            fontSize=8,
            alignment=TA_CENTER,
            textColor=colors.grey
        ))
    
    def create_cover_page(self, story):
        """Create cover page"""
        # Title
        title = Paragraph("Daily Market Summary", self.styles['CustomTitle'])
        story.append(title)
        story.append(Spacer(1, 0.5*inch))
        
        # Date
        date_str = datetime.now().strftime("%B %d, %Y")
        date_para = Paragraph(date_str, self.styles['CustomSubtitle'])
        story.append(date_para)
        story.append(Spacer(1, 0.3*inch))
        
        # Subtitle
        subtitle = Paragraph("Comprehensive Financial Market Analysis", self.styles['CustomSubtitle'])
        story.append(subtitle)
        story.append(Spacer(1, 0.5*inch))
        
        # Description
        description = """
        This report provides a comprehensive analysis of the US financial markets, 
        including major indices performance, sector analysis, economic indicators, 
        and market outlook. The summary is presented in multiple languages for 
        global accessibility.
        """
        desc_para = Paragraph(description, self.styles['CustomContent'])
        story.append(desc_para)
        story.append(Spacer(1, 0.5*inch))
        
        # Generated info
        generated_info = f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}"
        gen_para = Paragraph(generated_info, self.styles['Footer'])
        story.append(gen_para)
        
        story.append(PageBreak())
    
    def create_table_of_contents(self, story):
        """Create table of contents"""
        toc_title = Paragraph("Table of Contents", self.styles['CustomSubtitle'])
        story.append(toc_title)
        story.append(Spacer(1, 0.3*inch))
        
        # TOC entries
        toc_entries = [
            ("English Summary", "english"),
            ("Hindi Summary (हिंदी)", "hindi"),
            ("Arabic Summary (العربية)", "arabic"),
            ("Hebrew Summary (עברית)", "hebrew"),
            ("Charts and Data", "charts")
        ]
        
        for title, anchor in toc_entries:
            toc_item = Paragraph(f"<a href='#{anchor}'>{title}</a>", self.styles['CustomContent'])
            story.append(toc_item)
            story.append(Spacer(1, 0.1*inch))
        
        story.append(PageBreak())
    
    def add_language_section(self, story, content, language, language_name):
        """Add a language section to the PDF"""
        # Language header
        header = Paragraph(f"{language_name} Summary", self.styles['LanguageHeader'])
        story.append(header)
        
        # Determine text direction
        if language in ['ar', 'he']:
            content_style = self.styles['RTLContent']
        else:
            content_style = self.styles['CustomContent']
        
        # Add content
        if isinstance(content, str):
            # Simple text content
            content_para = Paragraph(content, content_style)
            story.append(content_para)
        elif isinstance(content, dict):
            # Structured content with sections
            for section, text in content.items():
                if section != 'images':
                    section_para = Paragraph(f"<b>{section}</b>", self.styles['Heading3'])
                    story.append(section_para)
                    story.append(Spacer(1, 0.1*inch))
                    
                    text_para = Paragraph(text, content_style)
                    story.append(text_para)
                    story.append(Spacer(1, 0.2*inch))
        
        story.append(Spacer(1, 0.3*inch))
        story.append(PageBreak())
    
    def add_images_section(self, story, images_data):
        """Add images and charts section"""
        header = Paragraph("Charts and Visual Data", self.styles['LanguageHeader'])
        story.append(header)
        
        if images_data:
            for img_info in images_data:
                if isinstance(img_info, dict) and 'path' in img_info:
                    try:
                        # Add image
                        img = Image(img_info['path'], width=6*inch, height=4*inch)
                        story.append(img)
                        story.append(Spacer(1, 0.1*inch))
                        
                        # Add caption
                        if 'caption' in img_info:
                            caption = Paragraph(f"<i>{img_info['caption']}</i>", self.styles['Footer'])
                            story.append(caption)
                        
                        story.append(Spacer(1, 0.2*inch))
                        
                    except Exception as e:
                        logger.error(f"Failed to add image {img_info.get('path', 'unknown')}: {e}")
                        error_para = Paragraph(f"Image unavailable: {img_info.get('caption', 'Chart')}", 
                                             self.styles['Footer'])
                        story.append(error_para)
                        story.append(Spacer(1, 0.2*inch))
    
    def generate_pdf(self, content_dict: Dict, output_path: str = None):
        """Generate the complete PDF document"""
        if output_path is None:
            output_path = os.path.join(Config.OUTPUT_DIR, Config.PDF_FILENAME)
        
        # Ensure output directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        try:
            # Create PDF document
            doc = SimpleDocTemplate(
                output_path,
                pagesize=A4,
                rightMargin=72,
                leftMargin=72,
                topMargin=72,
                bottomMargin=18
            )
            
            story = []
            
            # Create cover page
            self.create_cover_page(story)
            
            # Create table of contents
            self.create_table_of_contents(story)
            
            # Add language sections
            language_mapping = {
                'en': 'English',
                'hi': 'Hindi (हिंदी)',
                'ar': 'Arabic (العربية)',
                'he': 'Hebrew (עברית)'
            }
            
            for lang_code, lang_name in language_mapping.items():
                if lang_code in content_dict:
                    self.add_language_section(story, content_dict[lang_code], lang_code, lang_name)
            
            # Add images section
            if 'images' in content_dict:
                self.add_images_section(story, content_dict['images'])
            
            # Build PDF
            doc.build(story)
            
            logger.info(f"PDF generated successfully: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"PDF generation failed: {e}")
            raise
    
    def cleanup_temp_files(self):
        """Clean up temporary image files"""
        try:
            temp_dir = "temp_images"
            if os.path.exists(temp_dir):
                for file in os.listdir(temp_dir):
                    file_path = os.path.join(temp_dir, file)
                    if os.path.isfile(file_path):
                        os.remove(file_path)
                logger.info("Temporary files cleaned up")
        except Exception as e:
            logger.warning(f"Failed to cleanup temp files: {e}")
