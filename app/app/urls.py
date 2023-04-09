"""URL configuration for app project."""
from django.contrib import admin
from django.urls import path, include

from rest_framework.authtoken import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include([
        path('users/', include('users.api.urls'), name='users'),
        path('tasks/', include('tasks.api.urls'), name='tasks'),
    ]), name='api'),
    path('api-token-auth/', views.obtain_auth_token, name='api_token_auth'),
]
