from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView
from core.models import Recipe, IngredientType, Ingredient
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .forms import IngredientTypeForm, IngredientForm, RecipeForm
from django.core.exceptions import PermissionDenied
from django.shortcuts import render

class HomeView(LoginRequiredMixin, ListView):
    model = Recipe
    template_name = "yum_users/home.html"
    context_object_name = "recipes"
    login_url = "login"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(self.login_url)
         
        if request.user.role != "common":
            return redirect(self.login_url) 
        return super().dispatch(request, *args, **kwargs)

# IngredientType Views

class IngredientTypeCreateView(LoginRequiredMixin, CreateView):
    model = IngredientType
    form_class = IngredientTypeForm
    template_name = "yum_users/ingredient_type/add.html"
    success_url = reverse_lazy("ingredienttype_list") 
    login_url = "login"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(self.login_url)
         
        if request.user.role != "common":
            return redirect(self.login_url) 
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        form.instance.user = self.request.user  
        return super().form_valid(form)

class IngredientTypeListView(LoginRequiredMixin, ListView):
    model = IngredientType
    template_name = "yum_users/ingredient_type/list.html"
    context_object_name = "ingredient_types"
    login_url = "login"

    def form_valid(self, form):
        form.instance.user = self.request.user 
        return super().form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(self.login_url)
         
        if request.user.role != "common":
            return redirect(self.login_url) 
        return super().dispatch(request, *args, **kwargs)

class IngredientTypeUpdateView(LoginRequiredMixin, UpdateView):
    model = IngredientType
    form_class = IngredientTypeForm
    template_name = "yum_users/ingredient_type/add.html"
    success_url = reverse_lazy("ingredienttype_list")
    login_url = "login"

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.user != self.request.user:
            raise PermissionDenied("No tienes permiso para editar este ingrediente.")
        return obj
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(self.login_url)
         
        if request.user.role != "common":
            return redirect(self.login_url) 
        return super().dispatch(request, *args, **kwargs)


class IngredientTypeDeleteView(LoginRequiredMixin, DeleteView):
    model = IngredientType
    template_name = "yum_users/ingredient_type/confirm_delete.html"
    success_url = reverse_lazy("ingredienttype_list")

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.user != self.request.user:
            raise PermissionDenied("No tienes permiso para eliminar este ingrediente.")
        return obj
     
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(self.login_url)
         
        if request.user.role != "common":
            return redirect(self.login_url) 
        return super().dispatch(request, *args, **kwargs)

# Ingredient Views

class IngredientCreateView(LoginRequiredMixin, CreateView):
    model = Ingredient
    form_class = IngredientForm
    template_name = "yum_users/ingredient/add.html"
    login_url = "login"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(self.login_url)
        if request.user.role != "common":
            return redirect(self.login_url)

        self.recipe = get_object_or_404(Recipe, pk=kwargs["recipe_id"])
        if self.recipe.user != request.user:
            raise PermissionDenied("No tienes permiso para añadir ingredientes a esta receta.")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.recipe = self.recipe
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("recipe_edit", kwargs={"pk": self.recipe.id})

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["recipe"] = self.recipe
        return ctx


class IngredientUpdateView(LoginRequiredMixin, UpdateView):
    model = Ingredient
    form_class = IngredientForm
    template_name = "yum_users/ingredient/add.html"
    login_url = "login"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(self.login_url)
        if request.user.role != "common":
            return redirect(self.login_url)

        self.ingredient = self.get_object()
        if self.ingredient.recipe.user != request.user:
            raise PermissionDenied("No tienes permiso para editar este ingrediente.")
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy("recipe_edit", kwargs={"pk": self.ingredient.recipe.id})

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["recipe"] = self.ingredient.recipe
        return ctx


class IngredientDeleteView(LoginRequiredMixin, DeleteView):
    model = Ingredient
    template_name = "yum_users/ingredient/confirm_delete.html"
    login_url = "login"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(self.login_url)
        if request.user.role != "common":
            return redirect(self.login_url)

        self.ingredient = self.get_object()
        if self.ingredient.recipe.user != request.user:
            raise PermissionDenied("No tienes permiso para eliminar este ingrediente.")
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy("recipe_edit", kwargs={"pk": self.ingredient.recipe.id})
    

# Recipe Views

class RecipeDetailView(LoginRequiredMixin, DetailView):
    model = Recipe
    template_name = "yum_users/recipe/detail.html"
    context_object_name = "recipe"

    def get_queryset(self):
        return Recipe.objects.filter(user=self.request.user)
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(self.login_url)
         
        if request.user.role != "common":
            return redirect(self.login_url) 
        return super().dispatch(request, *args, **kwargs)

# Crear receta
class RecipeCreateView(LoginRequiredMixin, CreateView):
    model = Recipe
    form_class = RecipeForm
    template_name = "yum_users/recipe/add.html"
    login_url = "login"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("recipe_edit", kwargs={"pk": self.object.pk})
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(self.login_url)
         
        if request.user.role != "common":
            return redirect(self.login_url) 
        return super().dispatch(request, *args, **kwargs)

# Editar receta
class RecipeUpdateView(LoginRequiredMixin, UpdateView):
    model = Recipe
    form_class = RecipeForm
    template_name = "yum_users/recipe/add.html"
    login_url = "login"

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.user != self.request.user:
            raise PermissionDenied("No puedes editar esta receta.")
        return obj

    def get_success_url(self):
        return reverse_lazy("recipe_edit", kwargs={"pk": self.object.pk})
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(self.login_url)
         
        if request.user.role != "common":
            return redirect(self.login_url) 
        return super().dispatch(request, *args, **kwargs)

# Eliminar receta
class RecipeDeleteView(LoginRequiredMixin, DeleteView):
    model = Recipe
    template_name = "yum_users/recipe/confirm_delete.html"
    success_url = reverse_lazy("recipe_list")

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.user != self.request.user:
            raise PermissionDenied("No puedes eliminar esta receta.")
        return obj
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(self.login_url)
         
        if request.user.role != "common":
            return redirect(self.login_url) 
        return super().dispatch(request, *args, **kwargs)