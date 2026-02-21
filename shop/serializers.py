from rest_framework import serializers
from django.contrib.auth import get_user_model

from . import models


class CompactUserSerializer(serializers.ModelSerializer):
    """
    This is a compact user serializer intended for
    use as a nested serializer.
    """
    class Meta:
        model = get_user_model()
        fields = ["id", "username"]


class CompactItemSerializer(serializers.ModelSerializer):
    """
    This is a compact item serializer intended for
    use as a nested serializer.
    """
    class Meta:
        model = models.Item
        fields = ["id", "name"]


class ItemReviewSerializer(serializers.ModelSerializer):
    """
    This serializer represents item reviews.
    """
    item = CompactItemSerializer(read_only=True)
    author = CompactUserSerializer(read_only=True)

    class Meta:
        model = models.ItemReview
        fields = ["id", "rate", "text", "created_at", "item", "author"]
        read_only_fields = ["created_at"]


class ItemPhotoSerializer(serializers.ModelSerializer):
    """
    This serializer represents item photos.
    It is intended to be used as a nested serializer
    in ItemSerializer.
    """
    
    class Meta:
        model = models.ItemPhoto
        fields = ["id", "item", "photo"]
        read_only_fields = ["item"]


class ItemSerializer(serializers.ModelSerializer):
    """
    This serializer represents items (products).
    """
    photos = ItemPhotoSerializer(many=True, required=False)
    seller = CompactUserSerializer(read_only=True)
    reviews = ItemReviewSerializer(read_only=True, many=True)

    class Meta:
        model = models.Item
        fields = ["id", "name", "description", "price",
                  "available", "created_at", "photos", "seller", "reviews"]
        read_only_fields = ["created_at"]

    def create(self, validated_data):
        if "photos" in validated_data:
            photos = validated_data.pop("photos")
        else:
            photos = []

        item = models.Item.objects.create(**validated_data)

        
        for photo in photos:
            models.ItemPhoto.objects.create(item=item, photo=photo["photo"])

        return item

    def update(self, instance, validated_data):
        if "photos" in validated_data:
            photos = validated_data.pop("photos")
        else:
            photos = []

        instance.name = validated_data.get("name", instance.name)
        instance.description = validated_data.get("description", instance.description)
        instance.price = validated_data.get("price", instance.price)
        instance.available = validated_data.get("available", instance.available)

        instance.save()

        for photo in photos:
            models.ItemPhoto.objects.create(item=instance, photo=photo["photo"])

        return instance


class CartSerializer(serializers.ModelSerializer):
    """
    This serializer represents user's cart.
    """
    owner = CompactUserSerializer(read_only=True)
    items = CompactItemSerializer(read_only=True, many=True)

    class Meta:
        model = models.Cart
        fields = ["id", "owner", "items"]
