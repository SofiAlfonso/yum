from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from core.models import User, Recipe
from accounts.views import no_autorized

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
