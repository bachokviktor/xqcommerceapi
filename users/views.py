from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.contrib.auth import get_user_model

from . import serializers
from .permissions import IsCurrentUserOrReadOnly


class ListCreateUserView(APIView):
    """
    This view returns a list of users on GET
    request, and creates a new user on POST.
    """
    def get(self, request):
        users = get_user_model().objects.all()

        serializer = serializers.UserSerializer(users, many=True)

        return Response(data=serializer.data)

    def post(self, request):
        serializer = serializers.CreateUserSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetailView(RetrieveUpdateDestroyAPIView):
    """
    This view retrieves information about a user.
    It also allows authenticated users to update
    or delete their profile.
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsCurrentUserOrReadOnly]
    queryset = get_user_model().objects.all()
    serializer_class = serializers.UserSerializer
