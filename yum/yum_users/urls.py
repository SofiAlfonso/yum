# Autor: Ana Sofía Alfonso
from django.urls import path
from .views import (HomeView, IngredientTypeCreateView, IngredientTypeListView, IngredientDetailView, 
                    IngredientTypeUpdateView, IngredientTypeDeleteView, IngredientCreateView,
                    IngredientUpdateView, IngredientDeleteView, RecipeCreateView, RecipeUpdateView,
                    RecipeDetailView, InstructionCreateView, InstructionUpdateView, InstructionDeleteView,
                    ReviewCreateView, FavoriteListView, ToggleFavoriteView, RecipeDeleteView)


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
  path('ingredients/<int:pk>/', IngredientDetailView.as_view(), name='ingredient_detail'),

  # Recipe URLs
  path('recipes/add/', RecipeCreateView.as_view(), name='recipe_add'),
  path('recipes/<int:pk>/edit/', RecipeUpdateView.as_view(), name='recipe_edit'),
  path('recipes/<int:pk>/', RecipeDetailView.as_view(), name='recipe_detail'),
  path('recipes/<int:pk>/delete/', RecipeDeleteView.as_view(), name='recipe_delete'),

  # Instruction URLs
  path("recipes/<int:recipe_id>/instructions/add/", InstructionCreateView.as_view(), name="instruction_add"),
  path("instructions/<int:pk>/edit/", InstructionUpdateView.as_view(), name="instruction_edit"),
  path("instructions/<int:pk>/delete/", InstructionDeleteView.as_view(), name="instruction_delete"),

  # Review URLs
  path("recipes/<int:pk>/reviews/add/", ReviewCreateView.as_view(), name="review_add"),

  # Favorites
  path("favorites/", FavoriteListView.as_view(), name="favorites"),
  path("favorite/<int:recipe_id>/toggle/", ToggleFavoriteView.as_view(), name="toggle_favorite"),

]