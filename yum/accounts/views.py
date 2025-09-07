from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import login
from django.contrib import messages
from core.models import User
from .forms import RegisterForm, LoginForm


class RegisterView(CreateView):
    model = User
    form_class = RegisterForm
    template_name = "register.html"

    def get_success_url(self):
        # Redirigir según el rol del usuario
        if self.object.role == "admin":
            return reverse_lazy("admin_dashboard")  # TODO: ruta para yum_admins
        return reverse_lazy("user_dashboard")      # TODO: ruta para yum_users

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        messages.success(self.request, "Registro exitoso. Bienvenido!")
        return super().form_valid(form)


class CustomLoginView(LoginView):
    template_name = "login.html"
    authentication_form = LoginForm
    redirect_authenticated_user = True

    def get_success_url(self):
        user = self.request.user
        if user.role == "admin":
            return reverse_lazy("admin_dashboard")  # TODO: vista para admins
        return reverse_lazy("user_dashboard")      # TODO: vista para comunes


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy("login")