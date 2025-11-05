# Autor: Ana Sofía Alfonso
"""
Servicio para consumir la API de NewsAPI.org y obtener noticias sobre nutrición
"""
import requests
from typing import Dict, List, Optional
from django.conf import settings


def get_nutrition_news() -> Dict:
    """
    Consume la API de NewsAPI.org y retorna noticias sobre nutrición y alimentación.
    
    Returns:
        Dict con la estructura:
        {
            "total": int,
            "articles": [
                {
                    "title": str,
                    "description": str,
                    "url": str,
                    "urlToImage": str,
                    "publishedAt": str,
                    "source": str
                },
                ...
            ]
        }
    
    Raises:
        Exception: Si hay error en la petición HTTP o al procesar los datos
    """
    NEWS_API_URL = "https://newsapi.org/v2/everything"
    API_KEY = settings.NEWS_API_KEY
    
    params = {
        'q': 'nutrition OR dieta OR alimentación OR nutrición OR diet OR nutrición balanceada',
        'language': 'es',  # Noticias en español
        'sortBy': 'publishedAt',  # Ordenar por fecha de publicación (más recientes primero)
        'pageSize': 10,  # Máximo 10 noticias
        'apiKey': API_KEY
    }
    
    try:
        # Hacer petición GET a la API de NewsAPI
        response = requests.get(NEWS_API_URL, params=params, timeout=10)
        response.raise_for_status()  # Lanza excepción si hay error HTTP
        
        # Obtener datos JSON
        data = response.json()
        
        # Verificar si hay errores en la respuesta
        if data.get('status') == 'error':
            error_message = data.get('message', 'Error desconocido de la API')
            raise Exception(f"Error de la API: {error_message}")
        
        # Procesar artículos
        articles = []
        for article in data.get('articles', [])[:10]:  # Limitar a 10 artículos
            # Filtrar artículos que no tienen título o URL
            if article.get('title') and article.get('url'):
                articles.append({
                    'title': article.get('title', 'Sin título'),
                    'description': article.get('description', 'Sin descripción'),
                    'url': article.get('url', '#'),
                    'urlToImage': article.get('urlToImage'),
                    'publishedAt': article.get('publishedAt', ''),
                    'source': article.get('source', {}).get('name', 'Fuente desconocida')
                })
        
        return {
            'total': len(articles),
            'articles': articles
        }
        
    except requests.exceptions.RequestException as e:
        raise Exception(f"Error al consumir la API de noticias: {str(e)}")
    except Exception as e:
        raise Exception(f"Error al procesar las noticias: {str(e)}")

