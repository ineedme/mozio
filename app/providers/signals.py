from django.core.cache import cache
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import ServiceArea

@receiver([post_save, post_delete], sender=ServiceArea)
def clear_cache(sender, instance, **kwargs):
    """
    Clears the cache when a ServiceArea is saved or deleted.
    """
    cache.clear()
