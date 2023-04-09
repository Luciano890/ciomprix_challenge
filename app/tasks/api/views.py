"""Users views."""
from django.core.exceptions import ValidationError

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
)

from common.helpers import data_response
from tasks.models import Task
from tasks.serializers import TaskSerializer
from users.serializers import UserSerializer
from users.models import User


@api_view(['GET', 'POST', ])
def task_view(request: Request) -> Response:
    """Users default views."""
    if request.method == 'GET':
        params = {param: value for param, value in request.query_params.items() if value}
        tasks = Task.objects.all() if not params else Task.objects.filter(**params)
        serializer = TaskSerializer(tasks, many=True)
        return Response(data=serializer.data, status=HTTP_200_OK)
    elif request.method == 'POST':
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=HTTP_201_CREATED)
        return Response(data=data_response(serializer.errors), status=HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PATCH', 'DELETE', ])
def task_by_uuid_view(request: Request, task_uuid: str) -> Response:
    """Users by uuid views."""
    try:
        tasks = Task.objects.get(uuid=task_uuid)
    except Task.DoesNotExist:
        return Response(status=HTTP_404_NOT_FOUND)
    except ValidationError as errors:
        return Response(data=data_response(errors.messages), status=HTTP_400_BAD_REQUEST)
    if request.method == 'GET':
        serializer = TaskSerializer(tasks)
        return Response(data=serializer.data, status=HTTP_200_OK)
    elif request.method == 'PATCH':
        serializer = TaskSerializer(tasks, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=HTTP_200_OK)
        return Response(data=serializer.errors, status=HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        tasks.delete()
        return Response(status=HTTP_204_NO_CONTENT)

@api_view(['POST', ])
def add_users_to_task_view(request: Request, task_uuid: str) -> Response:
    """Add users to task views."""
    try:
        task = Task.objects.get(uuid=task_uuid)
    except Task.DoesNotExist:
        return Response(status=HTTP_404_NOT_FOUND)
    except ValidationError as errors:
        return Response(data=data_response(errors.messages), status=HTTP_400_BAD_REQUEST)
    if request.method == 'POST':
        users = User.objects.filter(
            uuid__in=request.data.get('users')
        ).exclude(tasks__in=[task.id])
        users_serializer = UserSerializer(users, many=True)
        task.users.add(*users)
        task.save()
        return Response(data=data_response(users_serializer.data), status=HTTP_200_OK)

@api_view(['GET', ])
def get_tasks_by_user_document(request: Request, document: str) -> Response:
    """Get tasks by user document views."""
    try:
        user = User.objects.get(document=document)
    except User.DoesNotExist:
        return Response(status=HTTP_404_NOT_FOUND)
    except ValidationError as errors:
        return Response(data=data_response(errors.messages), status=HTTP_400_BAD_REQUEST)
    if request.method == 'GET':
        tasks = Task.objects.filter(users__in=[user.id])
        serializer = TaskSerializer(tasks, many=True)
        return Response(data=serializer.data, status=HTTP_200_OK)
