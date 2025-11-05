# Autor: Ana Sofía Alfonso

from django.shortcuts import redirect, get_object_or_404, render
from django.views.generic import ListView, DetailView
from django.views import View
from core.models import Recipe, IngredientType, Ingredient, Instruction, Review, Multimedia
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from core.forms import IngredientTypeForm, IngredientForm, RecipeForm, InstructionForm, ReviewForm, RecipeFilterForm, MultimediaForm
from django.core.exceptions import PermissionDenied
from django.contrib.contenttypes.models import ContentType
from core.mixins import CommonUserRequiredMixin
from django.utils.translation import gettext as _


class HomeView(CommonUserRequiredMixin, ListView):
    model = Recipe
    template_name = "yum_users/home.html"
    context_object_name = "recipes"

    def get_queryset(self):
        queryset = Recipe.objects.all().select_related("user").prefetch_related("ingredients")

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

        return queryset.distinct()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filter_form"] = getattr(self, "filter_form", RecipeFilterForm())
        return context

# IngredientType Views

class IngredientTypeCreateView(CommonUserRequiredMixin, CreateView):
    model = IngredientType
    form_class = IngredientTypeForm
    template_name = "yum_users/ingredient_type/add.html"
    success_url = reverse_lazy("ingredienttype_list") 
    
    
    def form_valid(self, form):
        form.instance.user = self.request.user  
        return super().form_valid(form)

class IngredientTypeListView(CommonUserRequiredMixin, ListView):
    model = IngredientType
    template_name = "yum_users/ingredient_type/list.html"
    context_object_name = "ingredient_types"
    

    def form_valid(self, form):
        form.instance.user = self.request.user 
        return super().form_valid(form)

class IngredientTypeUpdateView(CommonUserRequiredMixin, UpdateView):
    model = IngredientType
    form_class = IngredientTypeForm
    template_name = "yum_users/ingredient_type/add.html"
    success_url = reverse_lazy("ingredienttype_list")
    

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.user != self.request.user:
            raise PermissionDenied("No tienes permiso para editar este ingrediente.")
        return obj


class IngredientTypeDeleteView(CommonUserRequiredMixin, DeleteView):
    model = IngredientType
    template_name = "yum_users/ingredient_type/confirm_delete.html"
    success_url = reverse_lazy("ingredienttype_list")

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.user != self.request.user:
            raise PermissionDenied("No tienes permiso para eliminar este ingrediente.")
        return obj

# Ingredient Views

class IngredientCreateView(CommonUserRequiredMixin, CreateView):
    model = Ingredient
    form_class = IngredientForm
    template_name = "yum_users/ingredient/add.html"
    

    def dispatch(self, request, *args, **kwargs):
        self.recipe = get_object_or_404(Recipe, pk=kwargs["recipe_id"])
        if self.recipe.user != request.user:
            raise PermissionDenied(_("No tienes permiso para añadir ingredientes a esta receta."))
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


class IngredientUpdateView(CommonUserRequiredMixin, UpdateView):
    model = Ingredient
    form_class = IngredientForm
    template_name = "yum_users/ingredient/add.html"
    

    def dispatch(self, request, *args, **kwargs):
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


class IngredientDeleteView(CommonUserRequiredMixin, DeleteView):
    model = Ingredient
    template_name = "yum_users/ingredient/confirm_delete.html"
    

    def dispatch(self, request, *args, **kwargs):
        self.ingredient = self.get_object()
        if self.ingredient.recipe.user != request.user:
            raise PermissionDenied("No tienes permiso para eliminar este ingrediente.")
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy("recipe_edit", kwargs={"pk": self.ingredient.recipe.id})
    
class IngredientDetailView(CommonUserRequiredMixin, DetailView):
    model = Ingredient
    template_name = "yum_users/ingredient/detail.html"
    context_object_name = "ingredient"
    

# Recipe Views

class RecipeDetailView(CommonUserRequiredMixin, DetailView):
    model = Recipe
    template_name = "yum_users/recipe/detail.html"
    context_object_name = "recipe"

    def get_queryset(self):
        return Recipe.objects.all()

class RecipeCreateView(CommonUserRequiredMixin, CreateView):
    model = Recipe
    form_class = RecipeForm
    template_name = "yum_users/recipe/add.html"
    

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("recipe_edit", kwargs={"pk": self.object.pk})
    

class RecipeUpdateView(CommonUserRequiredMixin, UpdateView):
    model = Recipe
    form_class = RecipeForm
    template_name = "yum_users/recipe/add.html"
    

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
        recipe = form.save(commit=False)
        recipe.user = self.request.user
        recipe.save()

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

        return redirect(self.get_success_url())

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.user != self.request.user:
            raise PermissionDenied("No puedes editar esta receta.")
        return obj

    def get_success_url(self):
        return reverse_lazy("recipe_edit", kwargs={"pk": self.object.pk})

class RecipeDeleteView(CommonUserRequiredMixin, DeleteView):
    model = Recipe
    template_name = "yum_users/recipe/confirm_delete.html"
    success_url = reverse_lazy("user_home")

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.user != self.request.user:
            raise PermissionDenied("No puedes eliminar esta receta.")
        return obj
    

# Instruction views

class InstructionCreateView(CommonUserRequiredMixin, CreateView):
    model = Instruction
    form_class = InstructionForm
    template_name = "yum_users/instruction/add.html"
    

    def dispatch(self, request, *args, **kwargs):
        self.recipe = get_object_or_404(Recipe, pk=kwargs["recipe_id"])
        if self.recipe.user != request.user:
            raise PermissionDenied(_("No tienes permiso para añadir ingredientes a esta receta."))
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

class InstructionUpdateView(CommonUserRequiredMixin, UpdateView):
    model = Instruction
    form_class = InstructionForm
    template_name = "yum_users/instruction/add.html"
    

    def dispatch(self, request, *args, **kwargs):
        self.instruction = self.get_object()
        if self.instruction.recipe.user != request.user:
            raise PermissionDenied("No tienes permiso para editar este ingrediente.")
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy("recipe_edit", kwargs={"pk": self.instruction.recipe.id})

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["recipe"] = self.instruction.recipe
        return ctx


class InstructionDeleteView(CommonUserRequiredMixin, DeleteView):
    model = Instruction
    template_name = "yum_users/instruction/confirm_delete.html"
    

    def dispatch(self, request, *args, **kwargs):
        self.ingredient = self.get_object()
        if self.ingredient.recipe.user != request.user:
            raise PermissionDenied("No tienes permiso para eliminar este ingrediente.")
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy("recipe_edit", kwargs={"pk": self.ingredient.recipe.id})

# Review View 

class ReviewCreateView(CommonUserRequiredMixin, CreateView):
    model = Review
    form_class = ReviewForm
    template_name = "yum_users/review/add.html"
    

    def form_valid(self, form):
        recipe = get_object_or_404(Recipe, pk=self.kwargs["pk"])
        form.instance.user = self.request.user
        form.instance.recipe = recipe
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("recipe_detail", kwargs={"pk": self.kwargs["pk"]})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        recipe = get_object_or_404(Recipe, pk=self.kwargs["pk"])
        context["recipe"] = recipe
        return context

# Favorites

class ToggleFavoriteView(CommonUserRequiredMixin, View):
    def post(self, request, recipe_id, *args, **kwargs):
        recipe = get_object_or_404(Recipe, id=recipe_id)

        if recipe in request.user.favorite_recipes.all():
            request.user.favorite_recipes.remove(recipe)  
        else:
            request.user.favorite_recipes.add(recipe)  

        return redirect("user_home")  

class FavoriteListView(CommonUserRequiredMixin, ListView):
    model = Recipe
    template_name = "yum_users/favorites.html"
    context_object_name = "recipes"
    

    def get_queryset(self):
        return self.request.user.favorite_recipes.all()


class ExternalRecommendationsView(CommonUserRequiredMixin, View):
    """
    Vista para mostrar recomendaciones de la API externa.
    Solo accesible para usuarios comunes (no admins).
    """
    template_name = "yum_users/external_recommendations.html"
    
    def dispatch(self, request, *args, **kwargs):
        # Verificar que el usuario sea común (no admin)
        if request.user.is_admin():
            raise PermissionDenied(_("Esta página solo está disponible para usuarios comunes."))
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request):
        from core.services.external_api import get_food_registers
        from django.contrib import messages
        
        try:
            # Consumir la API externa
            data = get_food_registers()
            
            context = {
                'recommendations': data.get('results', []),
                'total_count': data.get('count', 0),
                'error': None
            }
            
        except Exception as e:
            # En caso de error, mostrar mensaje y contexto vacío
            messages.error(request, _("Error al cargar las recomendaciones"))
            context = {
                'recommendations': [],
                'total_count': 0,
                'error': str(e)
            }
        
        return render(request, self.template_name, context)


class NewsView(CommonUserRequiredMixin, View):
    """
    Vista para mostrar noticias de nutrición y alimentación desde NewsAPI.org.
    Solo accesible para usuarios comunes (no admins).
    """
    template_name = "yum_users/news.html"
    
    def dispatch(self, request, *args, **kwargs):
        # Verificar que el usuario sea común (no admin)
        if request.user.is_admin():
            raise PermissionDenied(_("Esta página solo está disponible para usuarios comunes."))
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request):
        from core.services.news_api import get_nutrition_news
        from django.contrib import messages
        
        try:
            # Consumir la API de noticias
            data = get_nutrition_news()
            
            context = {
                'articles': data.get('articles', []),
                'total': data.get('total', 0),
                'error': None
            }
            
        except Exception as e:
            # En caso de error, mostrar mensaje y contexto vacío
            messages.error(request, _("Error al cargar las noticias"))
            context = {
                'articles': [],
                'total': 0,
                'error': str(e)
            }
        
        return render(request, self.template_name, context)
