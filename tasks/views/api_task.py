from rest_framework import generics, permissions
from tasks.models import Task
from tasks.serializers import TaskSerializer
from django.contrib.auth.views import LoginView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from rest_framework import permissions

class IsTaskOwner(permissions.BasePermission):
    """
    Custom permission to only allow the owner to view and edit their tasks.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user


class TaskListCreateViewAPI(generics.ListCreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [
        permissions.IsAuthenticated,
        IsTaskOwner
    ]

    def get_queryset(self):
        # Restrict the queryset to tasks owned by the logged-in user.
        return Task.objects.filter(
            owner=self.request.user
        ).order_by(
            'priority'
        )

    def perform_create(self, serializer):
        # Set the owner of the new task to the logged-in user.
        serializer.save(owner=self.request.user)

class TaskRetrieveUpdateDestroyViewAPI(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all().order_by(
        'priority'
    )
    serializer_class = TaskSerializer
    permission_classes = [
        permissions.IsAuthenticated,
        IsTaskOwner
    ]



class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(
            user=user
        )
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })
