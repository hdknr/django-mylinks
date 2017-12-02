from django.db.models.signals import post_save
from django.dispatch import receiver
from . import models


@receiver(post_save, sender=models.Page)
def on_save_saved(sender, instance=None, **kwargs):
    instance.update_content()    # TODO: not everytime when saved
