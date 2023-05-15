from django.urls import path
from .views import user_create_view, user_list_view

urlpatterns = [
    path('create/', user_create_view, name='user_create'),
    path('list/', user_list_view, name='user_list'),
]
