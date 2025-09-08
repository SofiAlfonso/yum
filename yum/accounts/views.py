from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import login
from django.contrib import messages
from django.shortcuts import render, redirect
from core.models import User
from .forms import RegisterForm,CustomLoginForm


class RegisterView(CreateView):
    model = User
    form_class = RegisterForm
    template_name = "accounts/register.html"

    def get_success_url(self):
        # Redirigir según el rol del usuario
        if self.object.role == "admin":
            return reverse_lazy("#")  # TODO: ruta para yum_admins
        return reverse_lazy("user_home")      # TODO: ruta para yum_users

    def form_valid(self, form):
        self.object = form.save()  # guardamos el usuario y lo asignamos
        login(self.request, self.object)  # lo logueamos
        messages.success(self.request, "Registro exitoso. Bienvenido!")
        return redirect(self.get_success_url())


class CustomLoginView(LoginView):
    template_name = "accounts/login.html"
    authentication_form = CustomLoginForm 
    redirect_authenticated_user = True

    def get_success_url(self):
        user = self.request.user
        if user.role == "admin":
            return reverse_lazy("#")  # TODO: vista para admins
        return reverse_lazy("user_home")      # TODO: vista para comunes


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy("login")