from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator


# Create your models here.
class Item(models.Model):
    """
    This model represents shop items (products).
    """
    name = models.CharField(max_length=150)
    description = models.TextField()
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.1)]
    )
    available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    seller = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="items"
    )

    def __str__(self):
        return f"{self.name} (${self.price})"


class ItemPhoto(models.Model):
    """
    This model represents photos of an item.
    """
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="photos")
    photo = models.ImageField(upload_to="item_photos/")


class ItemReview(models.Model):
    """
    This model represents a review of an item.
    """
    rate = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(10)]
    )
    text = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="reviews")
    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="reviewed"
    )

    def __str__(self):
        return f"{self.rate}/10 by {self.author.username}"


class Cart(models.Model):
    """
    This model represents user's cart.
    """
    owner = models.OneToOneField(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="cart"
    )
    items = models.ManyToManyField(Item, blank=True)
