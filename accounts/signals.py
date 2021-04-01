from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group
# from allauth.account.signals import user_signed_up

from .models import CustomUser

# @receiver(post_save, sender=CustomUser)
# def add_new_user_to_group_post_save(sender, instance, created, **kwargs):
#     if created:
#         general_group = Group.objects.get(name='general_user')
#         instance.groups.add(general_group)
        

## Using signal from allauth doesn't work when creating a new user in admin page.
## so I used the signal from CustomUser directly like above code.
# @receiver(user_signed_up)
# def add_new_user_to_group(sender, request, user, **kwargs):
#     general_group = Group.objects.get(name='general_user')
#     user.groups.add(general_group)