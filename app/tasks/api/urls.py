"""Task URLs."""
from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.task_view, name='task_view'),
    path(
        'document/<str:document>/',
        views.get_tasks_by_user_document,
        name='get_tasks_by_user_document_view'
    ),
    path('<str:task_uuid>/', include([
        path('', views.task_by_uuid_view, name='task_by_uuid_view'),
        path('add-users/', views.add_users_to_task_view, name='add_users_to_task_view'),
    ]), name='task_by_uuid_general_view'),
]
