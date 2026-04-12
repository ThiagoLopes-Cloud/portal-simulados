from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import Perfil

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def gerenciar_perfil_usuario(sender, instance, created, **kwargs):
    if created:
        Perfil.objects.create(user=instance)
    else:
        if hasattr(instance, 'perfil'):
            instance.perfil.save()