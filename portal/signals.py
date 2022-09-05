from allauth.account.signals import user_signed_up
from .models import UserProfile, Record
from django.db.models.signals import post_delete, post_save

def user_signed_up_receiver(request, user, **kwargs):
    user.username = user.email[0:user.email.index('@')]
    user.save()
    UserProfile.objects.create(user=user, firstName=user.first_name, lastName=user.last_name, email=user.email)

user_signed_up.connect(user_signed_up_receiver)

def update_hours_delete(sender, instance, **kwargs):
    instance.user.update_hours()

post_delete.connect(update_hours_delete, sender=Record)

def update_hours_save(sender, instance, created, **kwargs):
    instance.user.update_hours()

post_save.connect(update_hours_save, sender=Record)