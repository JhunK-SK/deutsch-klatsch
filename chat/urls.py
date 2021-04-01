from django.urls import path

from . import views

app_name = 'chat'
urlpatterns = [
    path('<str:topic>/', views.chat_room, name='room' ),
]