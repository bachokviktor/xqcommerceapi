from decimal import Decimal
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status

from shop import views, models, serializers


class ListCreateItemTests(APITestCase):
    def test_list_items(self):
        testing_seller = get_user_model().objects.create_user(
            username="testing_seller",
            password="dws9uirj"
        )

        models.Item.objects.create(
            name="Test Item 1",
            description="This is a test item.",
            price=Decimal("5.7"),
            seller=testing_seller,
        )

        models.Item.objects.create(
            name="Test Item 2",
            description="This is a test item.",
            price=Decimal("7.5"),
            seller=testing_seller,
        )

        models.Item.objects.create(
            name="Test Item 3",
            description="This is a test item.",
            price=Decimal("9.8"),
            seller=testing_seller,
        )

        response = self.client.get(reverse("shop:list_items"), format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_create_item(self):
        testing_seller = get_user_model().objects.create_user(
            username="testing_seller",
            password="dws9uirj"
        )

        item_data = {
            "name": "Test Item",
            "description": "This is a test item.",
            "price": "11.6"
        }

        self.client.force_authenticate(user=testing_seller)

        response = self.client.post(
            reverse("shop:list_items"),
            data=item_data,
            format="json"
        )
        
        self.client.force_authenticate(user=None)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], item_data["name"])
        self.assertEqual(response.data["description"], item_data["description"])
        self.assertEqual(Decimal(response.data["price"]), Decimal(item_data["price"]))
        self.assertEqual(response.data["seller"]["username"], testing_seller.username)


class RetrieveUpdateItemTests(APITestCase):
    def test_retrieve_item(self):
        testing_seller = get_user_model().objects.create_user(
            username="testing_seller",
            password="dws9uirj"
        )

        item = models.Item.objects.create(
            name="Test Item 1",
            description="This is a test item.",
            price=Decimal("5.7"),
            seller=testing_seller,
        )

        response = self.client.get(
            reverse("shop:retrieve_item", kwargs={"pk": item.id}),
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], item.name)
        self.assertEqual(response.data["description"], item.description)
        self.assertEqual(Decimal(response.data["price"]), item.price)
        self.assertEqual(response.data["seller"]["username"], testing_seller.username)

    def test_update_item(self):
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

        item_data = {
            "name": "Updated Test Item",
            "description": "This is an updated test item.",
            "price": "11.6"
        }

        self.client.force_authenticate(user=testing_seller)

        response = self.client.put(
            reverse("shop:retrieve_item", kwargs={"pk": item.id}),
            data=item_data,
            format="json"
        )
        
        self.client.force_authenticate(user=None)

        item = models.Item.objects.get()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(item.name, item_data["name"])
        self.assertEqual(item.description, item_data["description"])
        self.assertEqual(item.price, Decimal(item_data["price"]))
        self.assertEqual(item.seller, testing_seller)

    def test_delete_item(self):
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

        self.client.force_authenticate(user=testing_seller)

        response = self.client.delete(
            reverse("shop:retrieve_item", kwargs={"pk": item.id}),
            format="json"
        )
        
        self.client.force_authenticate(user=None)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(models.Item.objects.count(), 0)


class CreateReviewTests(APITestCase):
    def test_create_review(self):
        testing_reviewer = get_user_model().objects.create_user(
            username="testing_reviewer",
            password="dws9uirj"
        )

        item = models.Item.objects.create(
            name="Test Item",
            description="This is a test item.",
            price=Decimal("5.7"),
            seller=testing_reviewer,
        )

        review_data = {
            "rate": 7,
            "text": "This is a test review."
        }

        self.client.force_authenticate(user=testing_reviewer)

        response = self.client.post(
            reverse("shop:create_review", kwargs={"pk": item.id}),
            data=review_data,
            format="json"
        )
        
        self.client.force_authenticate(user=None)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["rate"], review_data["rate"])
        self.assertEqual(response.data["text"], review_data["text"])
        self.assertEqual(response.data["author"]["username"], testing_reviewer.username)


class UpdateDestroyReviewTests(APITestCase):
    def test_update_review(self):
        testing_reviewer = get_user_model().objects.create_user(
            username="testing_reviewer",
            password="dws9uirj"
        )

        item = models.Item.objects.create(
            name="Test Item",
            description="This is a test item.",
            price=Decimal("5.7"),
            seller=testing_reviewer,
        )

        review = models.ItemReview.objects.create(
            rate=7,
            text="This is a test review.",
            item=item,
            author=testing_reviewer
        )

        review_data = {
            "rate": 5,
            "text": "This is an updated review."
        }

        self.client.force_authenticate(user=testing_reviewer)

        response = self.client.put(
            reverse("shop:update_review", kwargs={"pk": item.id, "r_pk": review.id}),
            data=review_data,
            format="json"
        )
        
        self.client.force_authenticate(user=None)
        
        review = models.ItemReview.objects.get()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(review.rate, review_data["rate"])
        self.assertEqual(review.text, review_data["text"])
        self.assertEqual(review.author, testing_reviewer)
        self.assertEqual(review.item, item)

    def test_delete_review(self):
        testing_reviewer = get_user_model().objects.create_user(
            username="testing_reviewer",
            password="dws9uirj"
        )

        item = models.Item.objects.create(
            name="Test Item",
            description="This is a test item.",
            price=Decimal("5.7"),
            seller=testing_reviewer,
        )

        review = models.ItemReview.objects.create(
            rate=7,
            text="This is a test review.",
            item=item,
            author=testing_reviewer
        )

        self.client.force_authenticate(user=testing_reviewer)

        response = self.client.delete(
            reverse("shop:update_review", kwargs={"pk": item.id, "r_pk": review.id}),
            format="json"
        )
        
        self.client.force_authenticate(user=None)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(models.ItemReview.objects.count(), 0)


class ManageCartTests(APITestCase):
    def test_cart_add_item(self):
        testing_seller = get_user_model().objects.create_user(
            username="testing_seller",
            password="dws9uirj"
        )

        testing_buyer = get_user_model().objects.create_user(
            username="testing_buyer",
            password="dws9uirj"
        )

        models.Cart.objects.create(owner=testing_buyer)

        item = models.Item.objects.create(
            name="Test Item",
            description="This is a test item.",
            price=Decimal("5.7"),
            seller=testing_seller,
        )

        self.client.force_authenticate(user=testing_buyer)

        response = self.client.post(
            reverse("shop:manage_cart", kwargs={"pk": item.id}),
            format="json"
        )
        
        self.client.force_authenticate(user=None)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(item, testing_buyer.cart.items.all())

    def test_cart_remove_item(self):
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

        testing_buyer = get_user_model().objects.create_user(
            username="testing_buyer",
            password="dws9uirj"
        )

        models.Cart.objects.create(owner=testing_buyer)
        testing_buyer.cart.items.add(item)

        self.client.force_authenticate(user=testing_buyer)

        response = self.client.delete(
            reverse("shop:manage_cart", kwargs={"pk": item.id}),
            format="json"
        )
        
        self.client.force_authenticate(user=None)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(testing_buyer.cart.items.count(), 0)
        self.assertNotIn(item, testing_buyer.cart.items.all())
