from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from core.models import Recipe, IngredientType
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from .forms import IngredientTypeForm

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

