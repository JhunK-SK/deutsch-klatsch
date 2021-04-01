from django.urls import path
from . import views

app_name = 'user'
urlpatterns = [
    path('logout/', views.logout_view, name='logout'),
    path('profile/<str:username>/', views.user_profile_view, name='profile'),
    path('profile/<uuid:pk>/avatar/', views.user_edit, name='avatar'),
    path('account/deletion/<uuid:pk>/', views.user_account_delete, name='delete'),
]