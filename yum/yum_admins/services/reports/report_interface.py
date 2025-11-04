from abc import ABC, abstractmethod
from typing import List
from django.http import HttpResponse


class IReportGenerator(ABC):
    """
    Interfaz abstracta para generadores de reportes.
    Implementa el principio de Inversión de Dependencias (DIP).
    
    Las clases de alto nivel (vistas) dependerán de esta abstracción,
    no de implementaciones concretas (PDF, Excel).
    """
    
    @abstractmethod
    def generate(self, recipes: List, filename: str) -> HttpResponse:
        """
        Genera un reporte con la lista de recetas proporcionada.
        
        Args:
            recipes: Lista de objetos Recipe
            filename: Nombre del archivo a generar
            
        Returns:
            HttpResponse con el archivo generado
        """
        pass
    
    @abstractmethod
    def get_content_type(self) -> str:
        """
        Retorna el content-type del archivo generado.
        
        Returns:
            String con el MIME type del archivo
        """
        pass
    
    @abstractmethod
    def get_file_extension(self) -> str:
        """
        Retorna la extensión del archivo.
        
        Returns:
            String con la extensión (ej: 'pdf', 'xlsx')
        """
        pass