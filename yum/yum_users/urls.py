from django.urls import path
from .views import (HomeView, IngredientTypeCreateView, IngredientTypeListView, 
                    IngredientTypeUpdateView, IngredientTypeDeleteView, IngredientCreateView,
                    IngredientUpdateView, IngredientDeleteView)

urlpatterns = [
  path('home/', HomeView.as_view(), name='user_home'),

  # IngredientType URLs
  path('ingredienttypes/add/', IngredientTypeCreateView.as_view(), name='ingredienttype_add'),
  path('ingredienttypes/', IngredientTypeListView.as_view(), name='ingredienttype_list'),
  path("ingredient-types/<int:pk>/edit/", IngredientTypeUpdateView.as_view(), name="ingredienttype_edit"),
  path("ingredient-types/<int:pk>/delete/", IngredientTypeDeleteView.as_view(), name="ingredienttype_delete"),

  # Ingredient URLs
  path("recipes/<int:recipe_id>/ingredients/add/", IngredientCreateView.as_view(), name="ingredient_add"),
  path("ingredients/<int:pk>/edit/", IngredientUpdateView.as_view(), name="ingredient_edit"),
  path("ingredients/<int:pk>/delete/", IngredientDeleteView.as_view(), name="ingredient_delete"),

]