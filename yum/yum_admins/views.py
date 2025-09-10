from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from core.models import Recipe, IngredientType, Review, Instruction, User, Multimedia
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from yum_users.forms import RecipeFilterForm
from django.db.models import Count, Avg
from django.views.generic import TemplateView
from django.contrib import messages
from django.urls import reverse_lazy
from yum_users.forms import RecipeForm, MultimediaForm, IngredientTypeForm, InstructionForm, ReviewForm
from django.contrib.contenttypes.models import ContentType
from core.models import Multimedia
from core.mixins import AdminRequiredMixin


User = get_user_model()


# Dashboard Principal del Admin
class AdminDashboardView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = "yum_admins/dashboard.html"

    # Solo admins pueden entrar
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_admin()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["total_users"] = User.objects.count()
        context["total_recipes"] = Recipe.objects.count()
        context["total_reviews"] = Review.objects.count()

        context["top_recipes"] = (
            Recipe.objects.annotate(avg_score=Avg("reviews__score"))
            .order_by("-avg_score")[:5]
        )

        context["top_users"] = (
            User.objects.annotate(recipe_count=Count("recipes"))
            .order_by("-recipe_count")[:5]
        )


        context["top_reviewers"] = (
            User.objects.annotate(review_count=Count("reviews"))
            .order_by("-review_count")[:5]
        )

        context["global_avg_score"] = Review.objects.aggregate(
            global_avg=Avg("score")
        )["global_avg"] or 0

        return context

# Gestión de Usuarios
class AdminUserListView(AdminRequiredMixin, ListView):
    model = User
    template_name = "yum_admins/users/list.html"
    context_object_name = "users"
    paginate_by = 20

    def get_queryset(self):
        queryset = User.objects.annotate(
            recipe_count=Count("recipes"),
            review_count=Count("reviews")
        ).order_by("-date_joined")

        search = self.request.GET.get("search")
        if search:
            queryset = queryset.filter(username__icontains=search)

        role_filter = self.request.GET.get("role")
        if role_filter:
            queryset = queryset.filter(role=role_filter)

        return queryset


class AdminUserDetailView(AdminRequiredMixin, DetailView):
    model = User
    template_name = "yum_admins/users/detail.html"
    context_object_name = "user_detail"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.get_object()
        context.update({
            "user_recipes": Recipe.objects.filter(user=user).order_by("-creation_date"),
            "user_reviews": Review.objects.filter(user=user).select_related("recipe").order_by("-creation_date"),
            "recipe_count": Recipe.objects.filter(user=user).count(),
            "review_count": Review.objects.filter(user=user).count(),
        })
        return context

class AdminUserDeleteView(AdminRequiredMixin, DeleteView):
    model = User
    template_name = "yum_admins/users/confirm_delete.html"
    success_url = reverse_lazy("admin_user_list")

    def dispatch(self, request, *args, **kwargs):
        user_to_delete = self.get_object()
        if user_to_delete == request.user:
            messages.error(request, "No puedes eliminar tu propia cuenta.")
            return redirect("admin_user_list")
        return super().dispatch(request, *args, **kwargs)


# Gestión de Recetas
class AdminRecipeListView(AdminRequiredMixin, ListView):
    model = Recipe
    template_name = "yum_admins/recipe/list.html"
    context_object_name = "recipes"
    paginate_by = 20

    def get_queryset(self):
        queryset = Recipe.objects.all().select_related("user").prefetch_related("ingredients").annotate(
            review_count=Count("reviews"),
            avg_rating=Avg("reviews__score")
        )

        form = RecipeFilterForm(self.request.GET)
        if form.is_valid():
            name = form.cleaned_data.get("name")
            ingredient_type = form.cleaned_data.get("ingredient_type")
            min_value = form.cleaned_data.get("min_value")
            max_value = form.cleaned_data.get("max_value")

            if name:
                queryset = queryset.filter(title__icontains=name)

            if ingredient_type:
                queryset = queryset.filter(ingredients__ingredient_type=ingredient_type)

            if min_value is not None:
                queryset = queryset.filter(nutritional_value__gte=min_value)

            if max_value is not None:
                queryset = queryset.filter(nutritional_value__lte=max_value)

        user_filter = self.request.GET.get("user")
        if user_filter:
            queryset = queryset.filter(user__username__icontains=user_filter)

        return queryset.distinct().order_by("-creation_date")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filter_form"] = RecipeFilterForm(self.request.GET)
        return context


class AdminRecipeDetailView(AdminRequiredMixin, DetailView):
    model = Recipe
    template_name = "yum_admins/recipe/detail.html"
    context_object_name = "recipe"

    def get_queryset(self):
        return (
            Recipe.objects.all()
            .select_related("user")
            .prefetch_related(
                "ingredients__ingredient_type",
                "instructions",
                "reviews__user",
            )
            .annotate(
                review_count=Count("reviews", distinct=True),
                avg_rating=Avg("reviews__score"),
            )
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        recipe = self.object

        # solo calculamos los adicionales
        context["review_count"] = recipe.review_count or 0
        context["avg_rating"] = round(recipe.avg_rating, 1) if recipe.avg_rating else None

        return context



class AdminRecipeUpdateView(AdminRequiredMixin, UpdateView):
    model = Recipe
    form_class = RecipeForm
    template_name = "yum_admins/recipe/edit.html"
    
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        recipe = self.get_object()
        existing_media = Multimedia.objects.filter(
            content_type=ContentType.objects.get_for_model(Recipe),
            object_id=recipe.id
        ).first()

        if self.request.POST:
            ctx["media_form"] = MultimediaForm(
                self.request.POST,
                self.request.FILES,
                instance=existing_media
            )
        else:
            ctx["media_form"] = MultimediaForm(instance=existing_media)

        return ctx

    def form_valid(self, form):
        recipe = form.save()

        existing_media = Multimedia.objects.filter(
            content_type=ContentType.objects.get_for_model(Recipe),
            object_id=recipe.id
        ).first()

        media_form = MultimediaForm(
            self.request.POST,
            self.request.FILES,
            instance=existing_media
        )

        if media_form.is_valid():
            media = media_form.save(commit=False)
            media.content_object = recipe
            media.save()

        messages.success(self.request, f"Receta '{recipe.title}' actualizada correctamente.")
        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy("admin_recipe_detail", kwargs={"pk": self.object.pk})

class AdminRecipeDeleteView(AdminRequiredMixin, DeleteView):
    model = Recipe
    template_name = "yum_admins/recipe/confirm_delete.html"
    success_url = reverse_lazy("admin_recipe_list")
    
    def delete(self, request, *args, **kwargs):
        recipe = self.get_object()
        messages.success(request, f"Receta '{recipe.title}' eliminada correctamente.")
        return super().delete(request, *args, **kwargs)

class AdminIngredientTypeListView(AdminRequiredMixin, ListView):
    model = IngredientType
    template_name = "yum_admins/ingredient_type/list.html"
    context_object_name = "ingredient_types"
    paginate_by = 20

    def get_queryset(self):
        queryset = IngredientType.objects.all().select_related("user")

        # Filtros opcionales
        name = self.request.GET.get("name")
        category = self.request.GET.get("category")
        user_filter = self.request.GET.get("user")

        if name:
            queryset = queryset.filter(nombre__icontains=name)

        if category:
            queryset = queryset.filter(category=category)

        if user_filter:
            queryset = queryset.filter(user__username__icontains=user_filter)

        return queryset.order_by("nombre")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        # Puedes crear un formulario de filtro (opcional) como en RecipeFilterForm
        ctx["categories"] = dict(IngredientType.CATEGORY_CHOICES)  
        return ctx


class AdminIngredientTypeDetailView(AdminRequiredMixin, DetailView):
    model = IngredientType
    template_name = "yum_admins/ingredient_type/detail.html"
    context_object_name = "ingredient_type"

    def get_queryset(self):
        return IngredientType.objects.all().select_related("user")


class AdminIngredientTypeUpdateView(AdminRequiredMixin, UpdateView):
    model = IngredientType
    form_class = IngredientTypeForm
    template_name = "yum_admins/ingredient_type/edit.html"

    def form_valid(self, form):
        ingredient_type = form.save()
        messages.success(
            self.request,
            f"Tipo de ingrediente '{ingredient_type.nombre}' actualizado correctamente."
        )
        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy(
            "admin_ingredienttype_detail",
            kwargs={"pk": self.object.pk}
        )


class AdminIngredientTypeDeleteView(AdminRequiredMixin, DeleteView):
    model = IngredientType
    template_name = "yum_admins/ingredient_type/confirm_delete.html"
    success_url = reverse_lazy("admin_ingredienttype_list")

    def delete(self, request, *args, **kwargs):
        ingredient_type = self.get_object()
        messages.success(
            request,
            f"Tipo de ingrediente '{ingredient_type.nombre}' eliminado correctamente."
        )
        return super().delete(request, *args, **kwargs)
    

class AdminInstructionCreateView(AdminRequiredMixin, CreateView):
    model = Instruction
    form_class = InstructionForm
    template_name = "yum_admins/instruction/add.html"

    def dispatch(self, request, *args, **kwargs):
        self.recipe = get_object_or_404(Recipe, pk=kwargs["recipe_id"])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.recipe = self.recipe
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("admin_recipe_detail", kwargs={"pk": self.recipe.id})

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["recipe"] = self.recipe
        return ctx


class AdminInstructionUpdateView(AdminRequiredMixin, UpdateView):
    model = Instruction
    form_class = InstructionForm
    template_name = "yum_admins/instruction/add.html"

    def get_success_url(self):
        return reverse_lazy("admin_recipe_detail", kwargs={"pk": self.object.recipe.id})

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["recipe"] = self.object.recipe
        return ctx


class AdminInstructionDeleteView(AdminRequiredMixin, DeleteView):
    model = Instruction
    template_name = "yum_admins/instruction/confirm_delete.html"

    def get_success_url(self):
        return reverse_lazy("admin_recipe_detail", kwargs={"pk": self.object.recipe.id})
    

    
class AdminReviewDeleteView(AdminRequiredMixin, DeleteView):
    model = Review
    template_name = "yum_admins/review/confirm_delete.html"

    def get_success_url(self):
        return reverse_lazy("admin_recipe_detail", kwargs={"pk": self.object.recipe.id})
