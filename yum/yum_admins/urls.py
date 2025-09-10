from django.contrib import admin
from django.urls import path, include

from .views import AdminDashboardView, AdminUserListView, AdminUserDetailView, AdminUserDeleteView, AdminRecipeListView, AdminRecipeDetailView, AdminRecipeUpdateView, AdminRecipeDeleteView, AdminIngredientTypeListView, AdminIngredientTypeDetailView, AdminIngredientTypeUpdateView, AdminIngredientTypeDeleteView, AdminInstructionCreateView, AdminInstructionUpdateView, AdminInstructionDeleteView, AdminReviewDeleteView

urlpatterns = [
    path('dashboard/', AdminDashboardView.as_view(), name='admin_dashboard'),
    path("users/", AdminUserListView.as_view(), name="admin_user_list"),
    path("users/<int:pk>/", AdminUserDetailView.as_view(), name="admin_user_detail"),
    path("users/<int:pk>/delete/", AdminUserDeleteView.as_view(), name="admin_user_delete"),
    path("recipes/", AdminRecipeListView.as_view(), name="admin_recipe_list"),
    path("recipes/<int:pk>/", AdminRecipeDetailView.as_view(), name="admin_recipe_detail"),
    path("recipes/<int:pk>/edit/", AdminRecipeUpdateView.as_view(), name="admin_recipe_edit"),
    path("recipes/<int:pk>/delete/", AdminRecipeDeleteView.as_view(), name="admin_recipe_delete"),
    path("ingredient-types/", AdminIngredientTypeListView.as_view(), name="admin_ingredienttype_list"),
    path("ingredient-types/<int:pk>/", AdminIngredientTypeDetailView.as_view(), name="admin_ingredienttype_detail"),
    path("ingredient-types/<int:pk>/edit/", AdminIngredientTypeUpdateView.as_view(), name="admin_ingredienttype_edit"),
    path("ingredient-types/<int:pk>/delete/", AdminIngredientTypeDeleteView.as_view(), name="admin_ingredienttype_delete"),
    path("recipes/<int:recipe_id>/instructions/add/", AdminInstructionCreateView.as_view(), name="admin_instruction_add"),
    path("instructions/<int:pk>/edit/", AdminInstructionUpdateView.as_view(), name="admin_instruction_edit"),
    path("instructions/<int:pk>/delete/", AdminInstructionDeleteView.as_view(), name="admin_instruction_delete"),
    path("reviews/<int:pk>/delete/", AdminReviewDeleteView.as_view(), name="admin_review_delete"),

]