from django.test import TestCase
from django.contrib.auth import authenticate, get_user_model

from users import serializers


# Create your tests here.
class CreateUserSerializerTests(TestCase):
    def test_valid_data(self):
        test_username = "test_user"
        test_password = "dws9uirj"

        serializer = serializers.CreateUserSerializer(
            data={"username": test_username,
                  "password": test_password}
        )

        validation_status = serializer.is_valid()

        if validation_status:
            user = serializer.save()

        self.assertTrue(validation_status)
        self.assertEqual(
            user,
            authenticate(username=test_username, password=test_password)
        )


class UserSerializerTests(TestCase):
    def test_get_user_data(self):
        user = get_user_model().objects.create_user(
            username="test_user",
            password="dws9uirj"
        )

        serializer = serializers.UserSerializer(user)

        self.assertEqual(serializer.data["username"], user.username)

    def test_get_multiple_user_data(self):
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

        users = get_user_model().objects.all()

        serializer = serializers.UserSerializer(users, many=True)

        self.assertEqual(len(serializer.data), 3)
        self.assertEqual(serializer.data[0]["username"], "test_user1")
        self.assertEqual(serializer.data[1]["username"], "test_user2")
        self.assertEqual(serializer.data[2]["username"], "test_user3")

    def test_update_user_data(self):
        user = get_user_model().objects.create_user(
            username="test_user",
            password="dws9uirj"
        )

        payload = {
            "username": "test_user_new",
            "email": "test_user@gmail.com",
            "first_name": "Test",
            "last_name": "User",
            "bio": "Test bio.",
            "country": "UA"
        }

        serializer = serializers.UserSerializer(user, data=payload)

        validation_status = serializer.is_valid()
        if validation_status:
            serializer.save()

        self.assertTrue(validation_status)
        self.assertEqual(user.username, payload["username"])
        self.assertEqual(user.email, payload["email"])
        self.assertEqual(user.first_name, payload["first_name"])
        self.assertEqual(user.last_name, payload["last_name"])
        self.assertEqual(user.bio, payload["bio"])
        self.assertEqual(user.country.code, payload["country"])
