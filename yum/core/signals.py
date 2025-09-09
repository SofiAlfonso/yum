
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.db import transaction
from .models import Review

@receiver(post_save, sender=Review)
def review_saved(sender, instance, created, **kwargs):
    def _update():
        instance.recipe.update_media_score()
    transaction.on_commit(_update)