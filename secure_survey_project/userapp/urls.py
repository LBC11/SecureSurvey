from django.urls import path
from . import views

app_name = 'userapp'

urlpatterns = [
    path('register/', views.register_user, name='register'),
    path('success/', views.success, name='success_url'),
]
