# Autor: Ana Sofía Alfonso
"""
Servicio para consumir la API externa de food_registers
"""
import requests
from typing import Dict, List, Optional


def get_food_registers() -> Dict:
    """
    Consume la API externa y retorna los datos procesados.
    
    Returns:
        Dict con la estructura:
        {
            "count": int,
            "results": [
                {
                    "id": int,
                    "ingredients": [
                        {"name": str, "category": str},
                        ...
                    ],
                    "nutrition_summary": dict,
                    "image_url": str,
                    "total_calories": float,
                    "total_protein": float,
                    "total_carbs": float,
                    "total_fat": float,
                    "total_fiber": float,
                    "total_sugar": float,
                    "total_sodium": float
                },
                ...
            ]
        }
    
    Raises:
        Exception: Si hay error en la petición HTTP o al procesar los datos
    """
    EXTERNAL_API_URL = "https://respectful-miracle-production.up.railway.app/api/External/food_registers/"
    
    try:
        # Hacer petición GET a la API externa
        response = requests.get(EXTERNAL_API_URL, timeout=10)
        response.raise_for_status()  # Lanza excepción si hay error HTTP
        
        # Obtener datos JSON
        data = response.json()
        
        # Procesar y filtrar los datos
        processed_data = {
            "count": data.get("count", 0),
            "results": []
        }
        
        for food_register in data.get("results", []):
            # Extraer ingredientes (solo nombre y categoría)
            ingredients = []
            for food_item in food_register.get("food_items", []):
                ingredients.append({
                    "name": food_item.get("name"),
                    "category": food_item.get("category")
                })
            
            # Construir objeto procesado
            processed_register = {
                "id": food_register.get("id"),
                "ingredients": ingredients,
                "nutrition_summary": food_register.get("nutrition_summary"),
                "image_url": food_register.get("image_url"),
                "total_calories": food_register.get("total_calories"),
                "total_protein": food_register.get("total_protein"),
                "total_carbs": food_register.get("total_carbs"),
                "total_fat": food_register.get("total_fat"),
                "total_fiber": food_register.get("total_fiber"),
                "total_sugar": food_register.get("total_sugar"),
                "total_sodium": food_register.get("total_sodium")
            }
            
            processed_data["results"].append(processed_register)
        
        return processed_data
        
    except requests.exceptions.RequestException as e:
        raise Exception(f"Error al consumir la API externa: {str(e)}")
    except Exception as e:
        raise Exception(f"Error al procesar los datos: {str(e)}")

