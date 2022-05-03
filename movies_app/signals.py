from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver

from movies_app.services.emailServices import send_confirmation_url

from .models import Profile


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        profile = Profile.objects.create(user=instance)
        send_confirmation_url(instance, profile.confirmation_code)