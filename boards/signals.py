from django.db.models.signals import pre_save, post_save
from django.utils.text import slugify
from django.dispatch import receiver

from .models import Board, Topic
from chat.models import ChatRoom


@receiver(pre_save, sender=Board)
def make_slug_with_board_title(sender, instance, **kwargs):
        if instance.slug == '':
            slug = slugify(instance.board)
            # to make a unique slug, check if there's a same slug.
            if Board.objects.filter(slug=slug).exists():
                raise ValueError('Board title exists')
            else:
                instance.slug = slug


@receiver(pre_save, sender=Topic)
def make_slug_with_topic_title(sender, instance, **kwargs):
        if instance.slug == '':
            slug = slugify(instance.topic)
            # to make a unique slug, check if there's a same slug.
            if Topic.objects.filter(slug=slug).exists():
                raise ValueError('Topic title exists')
            else:
                instance.slug = slug


@receiver(post_save, sender=Topic)
def create_chatroom_model(sender, instance, *args, created, **kwargs):
    """
    Create ChatRoom model when Topic model is created.
    """
    if created:
        new_chatroom = ChatRoom.objects.create(room_name=instance.topic)
        new_chatroom.save()


# @receiver(post_save, sender=Board)
# def make_slug_with_board_title(sender, instance, *args, created, **kwargs):
#     if created:
#         instance.slug = slugify(instance.title)
#         instance.save()