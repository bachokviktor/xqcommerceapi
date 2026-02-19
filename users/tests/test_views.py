from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status


class ListCreateUserViewTests(APITestCase):
    def test_get_user_list(self):
        get_user_model().objects.create_user(
            username="test_user1",
            password="dws9uirj"
        )

        get_user_model().objects.create_user(
            username="test_user2",
            password="dws9uirj"
        )

        get_user_model().objects.create_user(
            username="test_user3",
            password="dws9uirj"
        )

        response = self.client.get(reverse("users:list_create"), format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_create_user(self):
        data = {
            "username": "test_user3",
            "password": "dws9uirj"
        }

        response = self.client.post(
            reverse("users:list_create"),
            data=data,
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(get_user_model().objects.count(), 1)
        self.assertEqual(get_user_model().objects.get().username, data["username"])


class UserDetailViewTest(APITestCase):
    def test_retrieve_user(self):
        user = get_user_model().objects.create_user(
            username="test_user",
            password="dws9uirj"
        )

        response = self.client.get(
            reverse("users:detail", kwargs={"pk": user.id}),
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"], user.username)

    def test_forbidden_access(self):
        user1 = get_user_model().objects.create_user(
            username="test_user1",
            password="dws9uirj"
        )

        user2 = get_user_model().objects.create_user(
            username="test_user2",
            password="dws9uirj"
        )

        self.client.force_authenticate(user=user1)

        response = self.client.delete(
            reverse("users:detail", kwargs={"pk": user2.id}),
            format="json"
        )

        self.client.force_authenticate(user=None)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_anonymous_forbidden_access(self):
        user = get_user_model().objects.create_user(
            username="test_user",
            password="dws9uirj"
        )

        response = self.client.delete(
            reverse("users:detail", kwargs={"pk": user.id}),
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_user(self):
        user = get_user_model().objects.create_user(
            username="test_user",
            password="dws9uirj"
        )

        data = {
            "username": "test_user_new",
            "email": "test_user@gmail.com",
            "first_name": "Test",
            "last_name": "User",
            "bio": "Test bio.",
            "country": "UA"
        }

        self.client.force_authenticate(user=user)

        response = self.client.put(
            reverse("users:detail", kwargs={"pk": user.id}),
            data=data,
            format="json"
        )

        self.client.force_authenticate(user=None)

        user = get_user_model().objects.get()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(user.username, data["username"])
        self.assertEqual(user.email, data["email"])
        self.assertEqual(user.first_name, data["first_name"])
        self.assertEqual(user.last_name, data["last_name"])
        self.assertEqual(user.bio, data["bio"])
        self.assertEqual(user.country.code, data["country"])


    def test_delete_user(self):
        user = get_user_model().objects.create_user(
            username="test_user",
            password="dws9uirj"
        )

        self.client.force_authenticate(user=user)

        response = self.client.delete(
            reverse("users:detail", kwargs={"pk": user.id}),
            format="json"
        )

        self.client.force_authenticate(user=None)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
