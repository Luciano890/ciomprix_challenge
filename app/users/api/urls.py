"""Users URLs."""
from django.urls import path

from . import views


urlpatterns = [
    path('', views.users_view, name='users_view'),
    path('<str:user_uuid>/', views.user_by_uuid_view, name='user_by_uuid_view'),
]
