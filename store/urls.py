from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.beat_list, name='beat_list'),
    path('explore/', views.genres, name='genres'),
    path('beat/<int:pk>/', views.beat_detail, name='beat_detail'),
    path('upload/', views.beat_upload, name='beat_upload'),
    path('register/', views.register, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('beat/<int:pk>/delete/', views.delete_beat, name='delete_beat'),
    path('login/', auth_views.LoginView.as_view(template_name='store/login.html'), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('beat/<int:pk>/edit/', views.beat_edit, name='beat_edit'),
    path('beat/<int:pk>/delete/', views.beat_delete, name='beat_delete'),
]

