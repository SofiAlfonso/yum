from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect

class CommonUserRequiredMixin(LoginRequiredMixin):
    login_url = "login"
    def dispatch(self, request, *args, **kwargs):
        if not hasattr(request.user, "role") or request.user.role != "common":
            return redirect(self.login_url)
        return super().dispatch(request, *args, **kwargs)