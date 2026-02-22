from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework import permissions
from django.http import Http404
from django.shortcuts import get_object_or_404

from . import serializers, models
from .permissions import IsSellerOrReadOnly, IsReviewAuthor


class ListCreateItemView(generics.ListCreateAPIView):
    """
    This view is used to get a list
    of items, or create a new item.
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = models.Item.objects.all()
    serializer_class = serializers.ItemSerializer

    def perform_create(self, serializer):
        serializer.save(seller=self.request.user)


class RetrieveUpdateItemView(generics.RetrieveUpdateDestroyAPIView):
    """
    This view is used to retrieve information
    about an item, update, or delete it.
    """
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsSellerOrReadOnly
    ]
    queryset = models.Item.objects.all()
    serializer_class = serializers.ItemSerializer


class CreateReviewView(APIView):
    """
    This view is used to leave review on an item.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        item = get_object_or_404(models.Item, pk=pk)

        serializer = serializers.ItemReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user, item=item)

            return Response(status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateDestroyReviewView(APIView):
    """
    This view is used to update or delete a review.
    """
    permission_classes = [permissions.IsAuthenticated, IsReviewAuthor]

    def put(self, request, pk, r_pk):
        review = get_object_or_404(models.ItemReview, pk=r_pk)

        serializer = serializers.ItemReviewSerializer(review, data=request.data)
        if serializer.is_valid():
            serializer.save()

            return Response(status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, r_pk):
        review = get_object_or_404(models.ItemReview, pk=r_pk)
        review.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class ManageCartView(APIView):
    """
    This view is used to add or delete an item
    from user's cart.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        item = get_object_or_404(models.Item, pk=pk)

        if item not in request.user.cart.items.all():
            request.user.cart.items.add(item)

        return Response(status=status.HTTP_200_OK)

    def delete(self, request, pk):
        item = get_object_or_404(models.Item, pk=pk)

        if item in request.user.cart.items.all():
            request.user.cart.items.remove(item)

        return Response(status=status.HTTP_200_OK)
