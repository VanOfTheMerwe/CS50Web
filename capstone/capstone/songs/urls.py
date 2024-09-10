from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('songs/', views.song_list, name='song_list'),
    path('add/', views.song_add, name='song_add'),
    path('edit/<int:song_id>/', views.song_edit, name='song_edit'),
    path('delete/<int:song_id>/', views.song_delete, name='song_delete'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.register, name='register'),
]