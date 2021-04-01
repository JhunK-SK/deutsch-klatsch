from django.urls import path

from .views import AboutView
from . import views

app_name = 'boards'
urlpatterns = [
    path('', views.index, name='home'),
    path('about/', AboutView.as_view(), name='about'),
    path('topic_request/', views.topic_request, name='request_list'),
    path('request/create', views.topic_request_create, name='request_create'),
    path('request/recommendation/', views.request_recommendation, name='request_recommendation'),
    
    # Topics
    path('topic/<slug:slug>/', views.topic_view, name='topic'),
    path('topic/favorite/add/', views.topic_favorite_view, name='topic_favorite'),
     
    # Posts
    path('post/<uuid:pk>/', views.post_view, name='post'),
    path('post/likes/', views.post_likes_view, name='post_likes'),
    path('write/<slug:slug>/', views.create_post_view, name='create'),
    path('edit/<uuid:pk>', views.edit_post_view, name='edit'),
    path('delete/<uuid:pk>', views.delete_post_view, name='delete'),
    
    # Comments
    path('post/<uuid:pk>/addcomment/', views.add_comment_view, name='comment'),
    path('post/comment/delete/<uuid:pk>/', views.delete_comment_view, name='comment-delete'),
    # path('post/comment/edit/<uuid:pk>/', views.edit_comment_view, name='comment-edit'),
    
]