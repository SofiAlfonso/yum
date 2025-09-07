from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from .services.nutritional_value import calculate_nutritional_value


# User model with roles and favorite recipes
class User(AbstractUser):
    ROLE_CHOICES = [
        ("admin", "Administrador"),
        ("common", "Usuario Común"),
    ]
    
    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default="common"
    )

    favorite_recipes = models.ManyToManyField(
        "Recipe",
        related_name="favorited_by",
        blank=True
    )

    def is_admin(self):
        return self.role == "admin"

    def is_common(self):
        return self.role == "common"
    
    
# IngeredientType model with nutritional information
class IngredientType(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    category = models.CharField(max_length=100)
    vitamins = models.JSONField(blank=True, null=True)  # lista de strings en formato json
    excesses = models.JSONField(blank=True, null=True)  # lista de strings en formato json

    def __str__(self):
        return self.nombre
    
# Ingredient model linked to IngredientType
class Ingredient(models.Model):
    recipe = models.ForeignKey("Recipe", on_delete=models.CASCADE, related_name="ingredients")
    ingredient_type = models.ForeignKey(IngredientType, on_delete=models.CASCADE, related_name="types")
    quantity = models.FloatField()
    unit = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.quantity} {self.unit} de {self.ingredient_type.nombre}"
    

# Recipe model 
class Recipe(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="recipes")
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=100)
    creation_date = models.DateTimeField(auto_now_add=True)
    preparation_time = models.DurationField()
    portions = models.PositiveIntegerField()

    # Campos calculados
    nutritional_value = models.IntegerField(default=0, editable=False)  # IA
    media_score = models.FloatField(default=0, editable=False)  # promedio reseñas

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.nutritional_value = calculate_nutritional_value(self)
        super().save(*args, **kwargs)

    def update_media_score(self):
        scores = self.reviews.all().values_list("score", flat=True)
        if scores:
            self.media_score = sum(scores) / len(scores)
            self.save(update_fields=["media_score"])


# Review model for user reviews on recipes
class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews")
    recipe = models.ForeignKey( "Recipe", on_delete=models.CASCADE, related_name="reviews")
    score = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])
    comment = models.TextField(blank=True, null=True)
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reseña de {self.user.username} para {self.recipe.title}"
    

# Instructions model for recipe steps
class Instruction(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="instructions")
    title = models.CharField(max_length=200)
    details = models.TextField()
    complexity = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)]) 
    n_step = models.PositiveIntegerField()  # número de paso

    def __str__(self):
        return f"{self.recipe.title} - Paso {self.n_step}: {self.title}"
    

# Multimedia model for recipe and review images
class Multimedia(models.Model):
    file = models.FileField(upload_to="uploads/")
    creation_date = models.DateTimeField(auto_now_add=True)

    # Campos para relación genérica
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    def __str__(self):
        return f"Media for {self.content_object}"