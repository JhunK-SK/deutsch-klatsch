from django import template
from django.shortcuts import get_object_or_404
from django.utils.safestring import mark_safe
from ..models import Post, Topic, TopicRequest

register = template.Library()


@register.simple_tag(name='likeOrNot')
def like_or_not(user, post_id, *args, **kwargs):
    """
    if user is anonymous, returns just string 
    grey or nothing to be applied as a default color from css file.
    if post.likes contains authenticated user, it returns color red.
    otherwise returns default color grey.
    """
    
    post = get_object_or_404(Post, id=post_id)
    
    result = 'grey'
    if not user.is_authenticated:
        pass
    
    elif post.likes.filter(id=user.id).exists():
        result = '#eb4034'
    
    else:
        pass
    
    return result


@register.simple_tag(name='favoriteOrNot')
def favortie_or_now(user, slug, *args, **kwargs):
    """
    if user is anonymous, returns just empty star mark 
    if topic.favorites contains authenticated user, it returns color orange star mark.
    otherwise returns default color grey.
    """
    
    topic = get_object_or_404(Topic, slug=slug)
    
    result = '<i class="far fa-star"></i>'
    if not user.is_authenticated:
        pass
    
    elif topic.favorites.filter(id=user.id).exists():
        result = '<i class="fas fa-star" style="color: rgb(255, 94, 0)"></i>'
    
    else:
        pass
    
    return mark_safe(result)


@register.simple_tag(name='recommendedOrNot')
def recommendedOrNot(user, request_id, *args, **kwargs):
    """
    Check if the user recommended this requested topic or not,
    and display differnt colored thumbsUp mark accordingly.
    """
    
    requested_topic = get_object_or_404(TopicRequest, id=request_id)
    
    result = '<i class="far fa-thumbs-up"></i>'
    if not user.is_authenticated:
        pass
    
    elif requested_topic.recommendations.filter(id=user.id).exists():
        result = '<i class="far fa-thumbs-up" style="color: #eb4034;"></i><p>Sie haben schon ausgewält!</p>'
    
    else:
        pass
    
    return mark_safe(result)