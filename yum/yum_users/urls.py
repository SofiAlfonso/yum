from django.urls import path
from .views import (HomeView, IngredientTypeCreateView, IngredientTypeListView, 
                    IngredientTypeUpdateView, IngredientTypeDeleteView)

urlpatterns = [
  path('home/', HomeView.as_view(), name='user_home'),
  path('ingredienttypes/add/', IngredientTypeCreateView.as_view(), name='ingredienttype_add'),
  path('ingredienttypes/', IngredientTypeListView.as_view(), name='ingredienttype_list'),
  path("ingredient-types/<int:pk>/edit/", IngredientTypeUpdateView.as_view(), name="ingredienttype_edit"),
  path("ingredient-types/<int:pk>/delete/", IngredientTypeDeleteView.as_view(), name="ingredienttype_delete"),

]