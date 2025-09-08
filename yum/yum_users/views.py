from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from core.models import Recipe, IngredientType, Ingredient
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .forms import IngredientTypeForm, IngredientForm
from django.core.exceptions import PermissionDenied

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

    def form_valid(self, form):
        recipe = get_object_or_404(Recipe, pk=self.kwargs["recipe_id"])
        form.instance.recipe = recipe

        if recipe.user != self.request.user:
            raise PermissionDenied("No tienes permiso para añadir ingredientes a esta receta.")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("recipe_edit", kwargs={"pk": self.kwargs["recipe_id"]})
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(self.login_url)
         
        if request.user.role != "common":
            return redirect(self.login_url) 
        return super().dispatch(request, *args, **kwargs)


class IngredientUpdateView(LoginRequiredMixin, UpdateView):
    model = Ingredient
    form_class = IngredientForm
    template_name = "yum_users/ingredient/add.html"
    login_url = "login"

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.recipe.user != self.request.user:
            raise PermissionDenied("No tienes permiso para editar este ingrediente.")
        return obj

    def get_success_url(self):
        return reverse_lazy("recipe_edit", kwargs={"pk": self.object.recipe.id})
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(self.login_url)
         
        if request.user.role != "common":
            return redirect(self.login_url) 
        return super().dispatch(request, *args, **kwargs)


class IngredientDeleteView(LoginRequiredMixin, DeleteView):
    model = Ingredient
    template_name = "yum_users/ingredient/confirm_delete.html"

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.recipe.user != self.request.user:
            raise PermissionDenied("No tienes permiso para eliminar este ingrediente.")
        return obj

    def get_success_url(self):
        return reverse_lazy("recipe_edit", kwargs={"pk": self.object.recipe.id})
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(self.login_url)
         
        if request.user.role != "common":
            return redirect(self.login_url) 
        return super().dispatch(request, *args, **kwargs)
    
