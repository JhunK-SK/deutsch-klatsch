import uuid
from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.conf import settings
from django.contrib.auth import get_user_model
from mptt.models import MPTTModel, TreeForeignKey


class Board(models.Model):
    board = models.CharField(max_length=100)
    slug = models.SlugField(null=False, blank=True)
    date_created = models.DateTimeField(
        verbose_name='date created',
        default=timezone.now
    )
    
    # This makes difference between board and slug, it's used to distinguish in home page collapse cards.
    def __str__(self):
        return self.board.capitalize()
    

class Topic(models.Model):
    board = models.ForeignKey(Board, on_delete=models.PROTECT)
    topic = models.CharField(max_length=100)
    slug = models.SlugField(null=False, blank=True)
    favorites = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='favorite',
        default=None,
        blank=True
    )
    date_created = models.DateTimeField(
        verbose_name='date created',
        default=timezone.now
    )
    
    def __str__(self):
        return self.topic.capitalize()
    
    def get_absolute_url(self):
        return reverse('topic', kwargs={'slug': self.slug})
 
    
# Post Model, View Counter, Thumbs Up need to be updated. 
class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    topic = models.ForeignKey(Topic, on_delete=models.PROTECT)
    writer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        on_delete=models.SET_NULL
    )
    title = models.CharField(max_length=100)
    post = models.TextField()
    likes = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='like',
        blank=True,
        default=None
    )
    like_count = models.BigIntegerField(default=0)
    view_count = models.BigIntegerField(default=0)
    date_created = models.DateTimeField(
        verbose_name='date created',
        default=timezone.now
    )
    date_updated = models.DateTimeField(
        verbose_name='date updated',
        auto_now=True
    )
    
    class Meta:
        ordering = ['-date_created']
    
    def __str__(self):
        return self.title


class Comment(MPTTModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    writer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        on_delete=models.SET_NULL
    )
    comment = models.TextField(max_length=1000)
    parent = TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children'
    )
    date_created = models.DateTimeField(
        verbose_name='date created',
        default=timezone.now
    )
    date_updated = models.DateTimeField(
        verbose_name='date updated',
        auto_now=True
    )
    
    class MPTTMeta:
        order_insertion_by = ['date_created']
    
    def __str__(self):
        return self.comment       
    
    
class IpModel(models.Model):
    ip = models.CharField(max_length=100)
    post = models.ManyToManyField(Post,
        related_name='viewed_ip',
        blank=True,
        default=None,
    )
    
    def __str__(self):
        return self.ip
    

class TopicRequest(models.Model):
    category = models.CharField(max_length=50)
    topic = models.CharField(max_length=100)
    purpose = models.TextField(max_length=1000)
    writer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        on_delete=models.SET_NULL
    )
    recommendations = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='recommendation',
        blank=True,
        default=None
    )
    like_count = models.BigIntegerField(default=0)
    date_created = models.DateTimeField(
        verbose_name='date created',
        default=timezone.now
    )
    date_updated = models.DateTimeField(
        verbose_name='date updated',
        auto_now=True
    )
    
    class Meta:
        ordering = ['-date_created']
    
    def __str__(self):
        return f'{self.category} - {self.topic}'