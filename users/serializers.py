from django.contrib.auth import get_user_model
from rest_framework import serializers
from django_countries.serializers import CountryFieldMixin
from shop.serializers import CompactItemSerializer, ItemReviewSerializer, CartSerializer


class CreateUserSerializer(serializers.ModelSerializer):
    """
    This serializer is used only for user creation.
    """
    class Meta:
        model = get_user_model()
        fields = ["username", "password"]
        extra_kwargs = {
            "password": {"write_only": True}
        }

    def create(self, validated_data):
        user = get_user_model().objects.create_user(**validated_data)

        return user

class UserSerializer(CountryFieldMixin, serializers.ModelSerializer):
    """
    User serializer.
    Can be used to retrieve or update user data.
    """
    items = CompactItemSerializer(read_only=True, many=True)
    reviewed = ItemReviewSerializer(read_only=True, many=True)
    cart = CartSerializer(read_only=True)

    class Meta:
        model = get_user_model()
        fields = ["id", "username", "email", "first_name", "last_name",
                  "bio", "profile_pic", "country", "items", "reviewed", "cart"]
