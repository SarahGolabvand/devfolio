from .models import User, ProfileModel
from django.dispatch import receiver
from django.db.models.signals import post_save


@receiver(post_save, sender=User)
def auto_create_profile(sender, instance, created, **kwargs):
    if created:
        ProfileModel.objects.create(user=instance)
        print(f"the profile of user {instance} created")