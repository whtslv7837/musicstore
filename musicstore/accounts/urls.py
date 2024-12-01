from django.urls import path
from . import views

urlpatterns = [
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
]
