"""
PDF Generator Module
Generates PDF reports for coffee bean analysis
"""

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image as RLImage, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from datetime import datetime
from PIL import Image
import os


class PDFGenerator:
    
    def __init__(self):
        """Initialize PDF generator"""
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
    
    def _setup_custom_styles(self):
        """Setup custom paragraph styles"""
        # Title style
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=28,
            textColor=colors.HexColor('#4A2511'),
            spaceAfter=20,
            spaceBefore=10,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))
        
        # Subtitle style
        self.styles.add(ParagraphStyle(
            name='CustomSubtitle',
            parent=self.styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#6F4E37'),
            spaceAfter=15,
            spaceBefore=10,
            fontName='Helvetica-Bold'
        ))
        
        # Section title style
        self.styles.add(ParagraphStyle(
            name='SectionTitle',
            parent=self.styles['Heading3'],
            fontSize=14,
            textColor=colors.HexColor('#6F4E37'),
            spaceAfter=10,
            spaceBefore=15,
            fontName='Helvetica-Bold'
        ))
        
        # Grade style
        self.styles.add(ParagraphStyle(
            name='GradeStyle',
            parent=self.styles['Normal'],
            fontSize=56,
            textColor=colors.HexColor('#228B22'),
            alignment=TA_CENTER,
            spaceAfter=15,
            spaceBefore=10,
            fontName='Helvetica-Bold'
        ))
    
    def _get_image_dimensions(self, image_path: str, max_width: float, max_height: float):
        """
        Calculate image dimensions while maintaining aspect ratio
        
        Args:
            image_path: Path to image file
            max_width: Maximum width in inches
            max_height: Maximum height in inches
            
        Returns:
            Tuple of (width, height) in inches
        """
        try:
            with Image.open(image_path) as img:
                img_width, img_height = img.size
                aspect_ratio = img_width / img_height
                
                # Calculate dimensions to fit within max bounds
                if aspect_ratio > 1:  # Landscape
                    width = min(max_width, max_height * aspect_ratio)
                    height = width / aspect_ratio
                else:  # Portrait or square
                    height = min(max_height, max_width / aspect_ratio)
                    width = height * aspect_ratio
                
                # Ensure we don't exceed max bounds
                if width > max_width:
                    width = max_width
                    height = width / aspect_ratio
                if height > max_height:
                    height = max_height
                    width = height * aspect_ratio
                
                return (width * inch, height * inch)
        except Exception as e:
            print(f"⚠️ Error getting image dimensions: {e}")
            # Fallback to default size
            return (5 * inch, 3.5 * inch)
    
    def generate_report(self, analysis_result: dict, original_image_path: str,
                       annotated_image_path: str, output_path: str, analyzer):
        """
        Generate PDF report
        
        Args:
            analysis_result: Analysis results dictionary
            original_image_path: Path to original image
            annotated_image_path: Path to annotated image
            output_path: Path to save PDF
            analyzer: CoffeeAnalyzer instance
        """
        # Use absolute paths
        abs_output_path = os.path.abspath(output_path)
        abs_annotated_path = os.path.abspath(annotated_image_path) if annotated_image_path else None
        
        # Create PDF with margins
        doc = SimpleDocTemplate(
            abs_output_path, 
            pagesize=A4,
            topMargin=0.75*inch,
            bottomMargin=0.75*inch,
            leftMargin=0.75*inch,
            rightMargin=0.75*inch
        )
        story = []
        
        # Title
        title = Paragraph("QOFFEA", self.styles['CustomTitle'])
        story.append(title)
        story.append(Spacer(1, 0.1*inch))
        
        subtitle = Paragraph("Coffee Bean Quality Analysis Report", self.styles['CustomSubtitle'])
        story.append(subtitle)
        story.append(Spacer(1, 0.25*inch))
        
        # Date and Time
        date_text = f"<b>Generated:</b> {datetime.now().strftime('%d %B %Y, %H:%M:%S')}"
        date_para = Paragraph(date_text, self.styles['Normal'])
        story.append(date_para)
        story.append(Spacer(1, 0.4*inch))
        
        # Overall Grade Section
        grade = analysis_result['grade']
        grade_color = self._get_grade_color(grade)
        
        # Create custom grade style with color
        grade_style = ParagraphStyle(
            name='DynamicGrade',
            parent=self.styles['GradeStyle'],
            textColor=grade_color
        )
        
        grade_text = f"<b>Grade: {grade}</b>"
        grade_para = Paragraph(grade_text, grade_style)
        story.append(grade_para)
        story.append(Spacer(1, 0.2*inch))
        
        # Grade Description
        grade_desc = analyzer.get_grade_description(grade)
        desc_para = Paragraph(f"<i>{grade_desc}</i>", self.styles['Normal'])
        story.append(desc_para)
        story.append(Spacer(1, 0.35*inch))
        
        # Summary Section Title
        summary_title = Paragraph("Analysis Summary", self.styles['SectionTitle'])
        story.append(summary_title)
        story.append(Spacer(1, 0.15*inch))
        
        # Summary Table
        summary_data = [
            ['Metric', 'Value'],
            ['Total Beans Detected', str(analysis_result['total_beans'])],
            ['Good Beans', f"{analysis_result['good_beans']} ({analysis_result['good_percentage']}%)"],
            ['Defect Beans', f"{analysis_result['defect_beans']} ({analysis_result['defect_percentage']}%)"],
        ]
        
        summary_table = Table(summary_data, colWidths=[3.25*inch, 3.25*inch])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#6F4E37')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('FONTSIZE', (0, 1), (-1, -1), 11),
            ('TOPPADDING', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.beige, colors.Color(0.95, 0.95, 0.9)])
        ]))
        
        story.append(summary_table)
        story.append(Spacer(1, 0.45*inch))
        
        # Images Section
        if abs_annotated_path and os.path.exists(abs_annotated_path):
            img_title = Paragraph("Analyzed Image with Detection Boxes", self.styles['SectionTitle'])
            story.append(img_title)
            story.append(Spacer(1, 0.2*inch))
            
            # Calculate image dimensions maintaining aspect ratio
            img_width, img_height = self._get_image_dimensions(abs_annotated_path, 6.5, 4.5)
            
            # Add annotated image with original aspect ratio
            img = RLImage(abs_annotated_path, width=img_width, height=img_height)
            story.append(img)
            story.append(Spacer(1, 0.35*inch))
        
        # Detection Details
        if 'detections' in analysis_result and len(analysis_result['detections']) > 0:
            # Add page break if needed
            if len(analysis_result['detections']) > 15:
                story.append(PageBreak())
            
            details_title = Paragraph("Detection Details", self.styles['SectionTitle'])
            story.append(details_title)
            story.append(Spacer(1, 0.15*inch))
            
            # Create detection table
            det_data = [['#', 'Class', 'Confidence']]
            for idx, det in enumerate(analysis_result['detections'][:30], 1):  # Limit to 30
                det_data.append([
                    str(idx),
                    det['class_name'],
                    f"{det['confidence']:.2%}"
                ])
            
            det_table = Table(det_data, colWidths=[0.6*inch, 3.7*inch, 2.2*inch])
            det_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#6F4E37')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 11),
                ('FONTSIZE', (0, 1), (-1, -1), 9),
                ('TOPPADDING', (0, 0), (-1, -1), 6),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.beige, colors.Color(0.95, 0.95, 0.9)])
            ]))
            
            story.append(det_table)
        
        # Footer
        story.append(Spacer(1, 0.5*inch))
        footer_text = "<i>This report is generated by QOFFEA AI-powered coffee grading system.</i>"
        footer = Paragraph(footer_text, self.styles['Normal'])
        story.append(footer)
        
        # Build PDF
        doc.build(story)
        print(f"✅ PDF report generated: {abs_output_path}")
    
    def _get_grade_color(self, grade: str):
        """
        Get color for grade
        
        Args:
            grade: Grade letter
            
        Returns:
            ReportLab color
        """
        grade_colors = {
            'A': colors.HexColor('#28a745'),  # Green
            'B': colors.HexColor('#ffc107'),  # Yellow/Orange
            'C': colors.HexColor('#dc3545'),  # Red
            'D': colors.HexColor('#6c757d'),  # Gray
        }
        return grade_colors.get(grade, colors.black)
