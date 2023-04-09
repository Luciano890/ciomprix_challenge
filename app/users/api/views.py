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

from users.models import User
from common.helpers import data_response
from users.serializers import UserSerializer


@api_view(['GET', 'POST', ])
def users_view(request: Request) -> Response:
    """Users default views."""
    if request.method == 'GET':
        params = {param: value for param, value in request.query_params.items() if value}
        users = User.objects.all() if not params else User.objects.filter(**params)
        serializer = UserSerializer(users, many=True)
        return Response(data=serializer.data, status=HTTP_200_OK)
    elif request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=HTTP_201_CREATED)
        return Response(data=data_response(serializer.errors), status=HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PATCH', 'DELETE', ])
def user_by_uuid_view(request: Request, user_uuid: str) -> Response:
    """Users by uuid views."""
    try:
        user = User.objects.get(uuid=user_uuid)
    except User.DoesNotExist:
        return Response(status=HTTP_404_NOT_FOUND)
    except ValidationError as errors:
        return Response(data=data_response(errors.messages), status=HTTP_400_BAD_REQUEST)
    if request.method == 'GET':
        serializer = UserSerializer(user)
        return Response(data=serializer.data, status=HTTP_200_OK)
    elif request.method == 'PATCH':
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=HTTP_200_OK)
        return Response(data=serializer.errors, status=HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        user.delete()
        return Response(status=HTTP_204_NO_CONTENT)
