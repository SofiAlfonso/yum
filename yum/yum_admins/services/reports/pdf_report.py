from typing import List
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from datetime import datetime
from django.utils.translation import gettext as _

from .report_interface import IReportGenerator


class PDFReportGenerator(IReportGenerator):
    """
    Implementación concreta del generador de reportes en formato PDF.
    Utiliza ReportLab para crear documentos PDF profesionales.
    """
    
    def generate(self, recipes: List, filename: str) -> HttpResponse:
        """Genera un reporte PDF con las recetas proporcionadas."""
        response = HttpResponse(content_type=self.get_content_type())
        response['Content-Disposition'] = f'attachment; filename="{filename}.{self.get_file_extension()}"'
        
        # Crear el documento PDF
        doc = SimpleDocTemplate(response, pagesize=A4)
        elements = []
        
        # Estilos
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#23b387'),
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )
        
        subtitle_style = ParagraphStyle(
            'CustomSubtitle',
            parent=styles['Normal'],
            fontSize=12,
            textColor=colors.grey,
            spaceAfter=20,
            alignment=TA_CENTER
        )
        
        # Título del reporte
        elements.append(Paragraph("🍽️ Reporte de Recetas - YUM", title_style))
        elements.append(Paragraph(
            f"Generado el: {datetime.now().strftime('%d/%m/%Y %H:%M')}",
            subtitle_style
        ))
        elements.append(Spacer(1, 0.3 * inch))
        
        # Resumen
        summary_data = [
            [_("📊 Resumen del Reporte"), ''],
            [_("Total de Recetas:"), str(len(recipes))],
            [_("Recetas con Reseñas:"), str(sum(1 for r in recipes if r.review_count > 0))],
            [_("Promedio de Rating:"), f"{sum(r.avg_rating or 0 for r in recipes) / len(recipes):.1f} ⭐" if recipes else "N/A"]
        ]
        
        summary_table = Table(summary_data, colWidths=[3*inch, 2*inch])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#23b387')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 14),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('PADDING', (0, 0), (-1, -1), 8),
        ]))
        
        elements.append(summary_table)
        elements.append(Spacer(1, 0.5 * inch))
        
        # Tabla de recetas
        data = [[_("#"), _("Título"), _("Usuario"), _("Valor Nutr."), _("Reseñas"), "Rating"]]
        
        for idx, recipe in enumerate(recipes, 1):
            data.append([
                str(idx),
                recipe.title[:30] + '...' if len(recipe.title) > 30 else recipe.title,
                recipe.user.username,
                str(recipe.nutritional_value),
                str(recipe.review_count),
                f"{recipe.avg_rating:.1f} ⭐" if recipe.avg_rating else "N/A"
            ])
        
        table = Table(data, colWidths=[0.5*inch, 2.5*inch, 1.2*inch, 1*inch, 0.8*inch, 1*inch])
        table.setStyle(TableStyle([
            # Encabezado
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#23b387')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            
            # Contenido
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
            ('ALIGN', (0, 1), (0, -1), 'CENTER'),  # Columna #
            ('ALIGN', (3, 1), (-1, -1), 'CENTER'),  # Columnas numéricas
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f5f5f5')]),
            ('PADDING', (0, 0), (-1, -1), 6),
        ]))
        
        elements.append(table)
        
        # Footer
        elements.append(Spacer(1, 0.5 * inch))
        footer_style = ParagraphStyle(
            'Footer',
            parent=styles['Normal'],
            fontSize=8,
            textColor=colors.grey,
            alignment=TA_CENTER
        )
        elements.append(Paragraph(
            _("Generado por YUM - Sistema de Gestión de Recetas"),
            footer_style
        ))
        
        # Construir el PDF
        doc.build(elements)
        return response
    
    def get_content_type(self) -> str:
        return 'application/pdf'
    
    def get_file_extension(self) -> str:
        return 'pdf'