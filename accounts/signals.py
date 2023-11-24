from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Profile


@receiver(post_save, sender=User)
def create_profile(sender, instance, **kwargs):
    if kwargs['created'] == True:
        Profile.objects.create(user=instance)
