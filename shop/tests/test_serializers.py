from decimal import Decimal
from django.core.files import File
from django.contrib.auth import get_user_model
from django.test import TestCase

from .common import create_testing_image
from shop import models, serializers


class ItemSerializerTests(TestCase):
    def test_serialize_item_instance(self):
        testing_seller = get_user_model().objects.create_user(
            username="testing_seller",
            password="dws9uirj"
        )

        item = models.Item.objects.create(
            name="Test Item",
            description="This is a test item.",
            price=Decimal("5.7"),
            seller=testing_seller,
        )

        testing_image = create_testing_image()
        item_photo = models.ItemPhoto.objects.create(
            item=item,
            photo=File(testing_image)
        )

        serializer = serializers.ItemSerializer(item)
        data = serializer.data

        self.assertEqual(item.name, data["name"])
        self.assertEqual(item.description, data["description"])
        self.assertEqual(item.price, Decimal(data["price"]))
        self.assertTrue(data["available"])
        self.assertEqual(testing_seller.username, data["seller"]["username"])
        self.assertNotEqual(data["photos"], [])
        self.assertEqual(item_photo.photo.url, data["photos"][0]["photo"])

        item_photo.photo.delete()

    def test_serializer_create_item(self):
        testing_seller = get_user_model().objects.create_user(
            username="testing_seller",
            password="dws9uirj"
        )

        testing_image = create_testing_image()

        item_data = {
            "name": "Test Item",
            "description": "This is a test item.",
            "price": "5.7",
            "photos": [
                {"photo": File(testing_image)}
            ]
        }

        serializer = serializers.ItemSerializer(data=item_data)

        validation_status = serializer.is_valid()
        if validation_status:
            item = serializer.save(seller=testing_seller)

        self.assertTrue(validation_status)
        self.assertEqual(item.name, item_data["name"])
        self.assertEqual(item.description, item_data["description"])
        self.assertEqual(item.price, Decimal(item_data["price"]))
        self.assertTrue(item.available)
        self.assertEqual(testing_seller, item.seller)
        self.assertEqual(item.photos.count(), 1)
        self.assertIsNotNone(item.photos.get().photo)

        item.photos.get().photo.delete()

    def test_serializer_update_item(self):
        testing_seller = get_user_model().objects.create_user(
            username="testing_seller",
            password="dws9uirj"
        )

        item = models.Item.objects.create(
            name="Test Item",
            description="This is a test item.",
            price=Decimal("5.7"),
            seller=testing_seller,
        )

        testing_image = create_testing_image()

        new_item_data = {
            "name": "Updated Test Item",
            "description": "This test item was updated.",
            "price": "6.7",
            "available": False,
            "photos": [
                {"photo": File(testing_image)}
            ]
        }

        serializer = serializers.ItemSerializer(item, data=new_item_data)

        validation_status = serializer.is_valid()
        if validation_status:
            item = serializer.save()

        self.assertTrue(validation_status)
        self.assertEqual(item.name, new_item_data["name"])
        self.assertEqual(item.description, new_item_data["description"])
        self.assertEqual(item.price, Decimal(new_item_data["price"]))
        self.assertFalse(item.available)
        self.assertEqual(testing_seller, item.seller)
        self.assertEqual(item.photos.count(), 1)
        self.assertIsNotNone(item.photos.get().photo)

        item.photos.get().photo.delete()


class ItemReviewSerializerTests(TestCase):
    def test_serialize_review_instance(self):
        testing_seller = get_user_model().objects.create_user(
            username="testing_seller",
            password="dws9uirj"
        )

        testing_reviewer = get_user_model().objects.create_user(
            username="testing_reviewer",
            password="dws9uirj"
        )

        item = models.Item.objects.create(
            name="Test Item",
            description="This is a test item.",
            price=Decimal("5.7"),
            seller=testing_seller,
        )

        review = models.ItemReview(
            item=item,
            rate=7,
            text="This is a test review.",
            author=testing_reviewer
        )

        serializer = serializers.ItemReviewSerializer(review)
        data = serializer.data

        self.assertEqual(review.rate, data["rate"])
        self.assertEqual(review.text, data["text"])
        self.assertEqual(review.author.username, data["author"]["username"])
        self.assertEqual(review.item.name, data["item"]["name"])

    def test_serializer_create_review(self):
        testing_seller = get_user_model().objects.create_user(
            username="testing_seller",
            password="dws9uirj"
        )

        testing_reviewer = get_user_model().objects.create_user(
            username="testing_reviewer",
            password="dws9uirj"
        )

        item = models.Item.objects.create(
            name="Test Item",
            description="This is a test item.",
            price=Decimal("5.7"),
            seller=testing_seller,
        )

        review_data = {
            "rate": 7,
            "text": "This is a test review.",
        }

        serializer = serializers.ItemReviewSerializer(data=review_data)

        validation_status = serializer.is_valid()
        if validation_status:
            review = serializer.save(item=item, author=testing_reviewer)

        self.assertTrue(validation_status)
        self.assertEqual(review.rate, review_data["rate"])
        self.assertEqual(review.text, review_data["text"])
        self.assertEqual(review.author, testing_reviewer)
        self.assertEqual(review.item, item)

    def test_serializer_update_review(self):
        testing_seller = get_user_model().objects.create_user(
            username="testing_seller",
            password="dws9uirj"
        )

        testing_reviewer = get_user_model().objects.create_user(
            username="testing_reviewer",
            password="dws9uirj"
        )

        item = models.Item.objects.create(
            name="Test Item",
            description="This is a test item.",
            price=Decimal("5.7"),
            seller=testing_seller,
        )
        
        review = models.ItemReview(
            item=item,
            rate=7,
            text="This is a test review.",
            author=testing_reviewer
        )

        new_review_data = {
            "rate": 5,
            "text": "This test review was updated.",
        }

        serializer = serializers.ItemReviewSerializer(review, data=new_review_data)

        validation_status = serializer.is_valid()
        if validation_status:
            review = serializer.save()

        self.assertTrue(validation_status)
        self.assertEqual(review.rate, new_review_data["rate"])
        self.assertEqual(review.text, new_review_data["text"])
        self.assertEqual(review.author, testing_reviewer)
        self.assertEqual(review.item, item)
