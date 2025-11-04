# Autor: Ana Sofía Alfonso
# yum_admins/services/reports/report_factory.py

from typing import Optional
from .report_interface import IReportGenerator
from .pdf_report import PDFReportGenerator
from .excel_report import ExcelReportGenerator


class ReportFactory:
    """
    Factory para crear instancias de generadores de reportes.
    Implementa el patrón Factory Method junto con el principio DIP.
    
    Esta clase centraliza la creación de objetos y permite agregar
    nuevos tipos de reportes sin modificar el código existente
    (Open/Closed Principle).
    """
    
    # Registro de generadores disponibles
    _generators = {
        'pdf': PDFReportGenerator,
        'excel': ExcelReportGenerator,
    }
    
    @classmethod
    def create_generator(cls, report_type: str) -> Optional[IReportGenerator]:
        """
        Crea una instancia del generador de reportes solicitado.
        
        Args:
            report_type: Tipo de reporte ('pdf' o 'excel')
            
        Returns:
            Instancia de IReportGenerator o None si el tipo no existe
            
        Example:
            >>> generator = ReportFactory.create_generator('pdf')
            >>> response = generator.generate(recipes, 'mi_reporte')
        """
        generator_class = cls._generators.get(report_type.lower())
        
        if generator_class:
            return generator_class()
        
        return None
    
    @classmethod
    def get_available_formats(cls) -> list:
        """
        Retorna la lista de formatos de reporte disponibles.
        
        Returns:
            Lista con los nombres de los formatos disponibles
        """
        return list(cls._generators.keys())
    
    @classmethod
    def register_generator(cls, report_type: str, generator_class: type):
        """
        Permite registrar un nuevo tipo de generador dinámicamente.
        Útil para extensiones futuras.
        
        Args:
            report_type: Nombre del tipo de reporte
            generator_class: Clase que implementa IReportGenerator
        """
        if not issubclass(generator_class, IReportGenerator):
            raise ValueError(
                f"{generator_class.__name__} debe implementar IReportGenerator"
            )
        
        cls._generators[report_type.lower()] = generator_class