from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from accounts.others_models.model_profile import UserProfile
from accounts.models import User


@receiver(post_save, sender=User)
def post_save_create_profile_receiver(sender, instance, created, **kwargs):
    print(created)
    if created:
        UserProfile.objects.create(user=instance)
    else:
        try:
            profile = UserProfile.objects.get(user=instance)
            profile.save()
        except:
            # Create the userprofile if not exist
            UserProfile.objects.create(user=instance)

@receiver(pre_save, sender=User)
def pre_save_profile_receiver(sender, instance, **kwargs):
    pass
