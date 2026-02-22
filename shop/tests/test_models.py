from decimal import Decimal
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.files import File

from shop import models
from .common import create_testing_image


# Create your tests here.
class ItemModelTests(TestCase):
    def test_create_item(self):
        testing_seller = get_user_model().objects.create_user(
            username="testing_seller",
            password="dws9uirj"
        )

        item_data = {
            "name": "Test Item",
            "description": "This is a test item.",
            "price": Decimal("5.7"),
            "seller": testing_seller,
        }

        item = models.Item.objects.create(**item_data)

        self.assertIn(item, testing_seller.items.all())
        self.assertEqual(item.name, item_data["name"])
        self.assertEqual(item.description, item_data["description"])
        self.assertEqual(item.price, item_data["price"])
        self.assertTrue(item.available)
        self.assertEqual(testing_seller, item_data["seller"])

    def test_create_item_with_photo(self):
        testing_seller = get_user_model().objects.create_user(
            username="testing_seller",
            password="dws9uirj"
        )

        testing_item = models.Item.objects.create(
            name="Test Item",
            description="This is a test item.",
            price=Decimal("5.7"),
            seller=testing_seller,
        )

        testing_image = create_testing_image()
        
        item_photo = models.ItemPhoto.objects.create(
            item=testing_item,
            photo=File(testing_image)
        )

        self.assertIn(item_photo, testing_item.photos.all())
        self.assertIsNotNone(item_photo.photo)

        item_photo.photo.delete()


class ItemReviewModelTests(TestCase):
    def test_add_review(self):
        testing_seller = get_user_model().objects.create_user(
            username="testing_seller",
            password="dws9uirj"
        )

        testing_reviewer = get_user_model().objects.create_user(
            username="testing_reviewer",
            password="dws9uirj"
        )

        testing_item = models.Item.objects.create(
            name="Test Item",
            description="This is a test item.",
            price=Decimal("5.7"),
            seller=testing_seller,
        )

        review_data = {
            "rate": 7,
            "text": "This is a test review.",
            "item": testing_item,
            "author": testing_reviewer,
        }

        review = models.ItemReview.objects.create(**review_data)

        self.assertIn(review, testing_reviewer.reviewed.all())
        self.assertIn(review, testing_item.reviews.all())
        self.assertEqual(review.rate, review_data["rate"])
        self.assertEqual(review.text, review_data["text"])
        self.assertEqual(review.item, testing_item)
        self.assertEqual(review.author, testing_reviewer)


class CartModelTests(TestCase):
    def test_cart_add_items(self):
        testing_seller = get_user_model().objects.create_user(
            username="testing_seller",
            password="dws9uirj"
        )

        testing_user = get_user_model().objects.create_user(
            username="testing_user",
            password="dws9uirj"
        )

        testing_item1 = models.Item.objects.create(
            name="Test Item",
            description="This is a test item.",
            price=Decimal("5.7"),
            seller=testing_seller,
        )

        testing_item2 = models.Item.objects.create(
            name="Another Test Item",
            description="This is a test item.",
            price=Decimal("6.7"),
            seller=testing_seller,
        )

        cart = models.Cart.objects.create(owner=testing_user)
        cart.items.add(testing_item1)
        cart.items.add(testing_item2)

        self.assertIn(testing_item1, cart.items.all())
        self.assertIn(testing_item2, cart.items.all())
