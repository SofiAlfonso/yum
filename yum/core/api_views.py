# Autor: Ana Sofía Alfonso
"""
Vistas API para exponer servicios web en formato JSON
"""
from django.http import JsonResponse
from core.models import Recipe


def format_duration(duration):
    """
    Convierte un timedelta a formato string HH:MM:SS
    """
    total_seconds = int(duration.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"


def recipes_api(request):
    """
    API endpoint público que retorna todas las recetas disponibles en formato JSON.
    
    Formato de respuesta:
    {
        "recipes": [
            {
                "id": 1,
                "nombre": "Nombre de la receta",
                "tiempo_preparacion": "01:30:00",
                "porciones": 4,
                "valor_nutricional": 85,
                "calificacion": 4.5
            },
            ...
        ],
        "total": 10
    }
    """
    # Obtener todas las recetas ordenadas por fecha de creación (más recientes primero)
    recipes = Recipe.objects.all().order_by('-creation_date')
    
    recipes_data = []
    for recipe in recipes:
        # Convertir DurationField a string en formato HH:MM:SS
        prep_time = format_duration(recipe.preparation_time)
        
        recipes_data.append({
            'id': recipe.id,
            'nombre': recipe.title,
            'tiempo_preparacion': prep_time,
            'porciones': recipe.portions,
            'valor_nutricional': recipe.nutritional_value,
            'calificacion': float(recipe.media_score) if recipe.media_score else 0.0
        })
    
    return JsonResponse({
        'recipes': recipes_data,
        'total': len(recipes_data)
    }, safe=False)

