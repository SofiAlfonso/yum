import google.generativeai as genai
from django.conf import settings

# Configurar el cliente de Gemini
genai.configure(api_key=settings.GEMINI_API_KEY)

def calculate_nutritional_value(recipe):
    ingredientes = []
    for ing in recipe.ingredients.all():
        ingredientes.append({
            "nombre": ing.ingredient_type.nombre,
            "cantidad": f"{ing.quantity} {ing.unit}",
            "categoria": ing.ingredient_type.category,
            "vitaminas": ing.ingredient_type.vitamins,
            "excesos": ing.ingredient_type.excesses,
        })

    prompt = f"""
    Eres un experto en nutrición. Evalúa la siguiente receta y dame un puntaje nutricional 
    de 1 a 100, donde 100 es extremadamente saludable y 1 es nada saludable.
    
    Receta: {recipe.title}
    Descripción: {recipe.description}
    Categoría: {recipe.category}
    Porciones: {recipe.portions}
    Ingredientes: {ingredientes}
    
    Responde SOLO con un número entre 1 y 100.
    """

    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)

        text = response.text.strip()
        number = "".join([c for c in text if c.isdigit()])

        if number:
            score = int(number)
            return max(1, min(score, 100)) 
        return 50  
    
    except Exception as e:
        print(f"Error al calcular valor nutricional: {e}")
        return 50