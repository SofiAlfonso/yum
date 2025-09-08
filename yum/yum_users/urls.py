from django.urls import path
from .views import HomeView, IngredientTypeCreateView, IngredientTypeListView

urlpatterns = [
  path('home/', HomeView.as_view(), name='user_home'),
  path('ingredienttypes/add/', IngredientTypeCreateView.as_view(), name='ingredienttype_add'),
  path('ingredienttypes/', IngredientTypeListView.as_view(), name='ingredienttype_list'),
]