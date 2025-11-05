# Autor:Ana Sofía Alfonso
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from django.db import transaction
from .models import Review, Ingredient
from .services.nutritional_value import calculate_nutritional_value

@receiver(post_save, sender=Review)
def review_saved(sender, instance, created, **kwargs):
    def _update():
        instance.recipe.update_media_score()
    transaction.on_commit(_update)

@receiver(post_save, sender=Ingredient)
def update_recipe_nutritional_value_on_save(sender, instance, **kwargs):
    recipe = instance.recipe
    recipe.nutritional_value = calculate_nutritional_value(recipe)
    recipe.save(update_fields=["nutritional_value"])

@receiver(post_delete, sender=Ingredient)
def update_recipe_nutritional_value_on_delete(sender, instance, **kwargs):
    recipe = instance.recipe
    recipe.nutritional_value = calculate_nutritional_value(recipe)
    recipe.save(update_fields=["nutritional_value"])
