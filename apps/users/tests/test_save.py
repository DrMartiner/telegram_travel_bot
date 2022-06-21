from django.contrib.auth import get_user_model
from django.db import IntegrityError

from apps.common.base_test import BaseTest
from apps.users.models import User as UserModel

User: UserModel = get_user_model()


class UserUniqueFieldsTest(BaseTest):
    def test_create_null_telegram_user_id(self):
        User.objects.create(telegram_user_id=None)

    def test_create_double_null_telegram_user_id(self):
        User.objects.create(username="1", telegram_user_id=None)
        User.objects.create(username="2", telegram_user_id=None)

    def test_create_null_telegram_chat_id(self):
        User.objects.create(telegram_chat_id=None)

    def test_create_double_null_telegram_chat_id(self):
        User.objects.create(username="1", telegram_chat_id=None)
        User.objects.create(username="2", telegram_chat_id=None)

    def test_create_unique_telegram_user_id(self):
        User.objects.create(telegram_user_id=123)

    def test_create_double_unique_telegram_user_id(self):
        user_id = 123
        User.objects.create(telegram_user_id=user_id)
        with self.assertRaises(IntegrityError, msg=f"User with telegram_user_id={user_id} is already exists"):
            User.objects.create(telegram_user_id=user_id)

    def test_create_unique_telegram_chat_id(self):
        User.objects.create(telegram_user_id=123)

    def test_create_double_unique_telegram_chat_id(self):
        chat_id = 123
        User.objects.create(telegram_chat_id=chat_id)
        with self.assertRaises(IntegrityError, msg=f"User with telegram_chat_id={chat_id} is already exists"):
            User.objects.create(telegram_chat_id=chat_id)

    def test_update_null_telegram_user_id(self):
        user = User.objects.create(username="1", telegram_user_id=None)
        user.username = "new"
        user.save()

    def test_update_telegram_user_id(self):
        user = User.objects.create(username="1", telegram_user_id=123)
        user.username = "new"
        user.save()

    def test_update_telegram_user_id_value(self):
        user = User.objects.create(username="1", telegram_user_id=123)
        user.telegram_user_id = 456
        user.save()

    def test_update_null_telegram_chat_id(self):
        user = User.objects.create(username="1", telegram_user_id=None)
        user.username = "new"
        user.save()

    def test_update_telegram_chat_id(self):
        user = User.objects.create(username="1", telegram_chat_id=123)
        user.username = "new"
        user.save()

    def test_update_telegram_chat_id_value(self):
        user = User.objects.create(username="1", telegram_chat_id=123)
        user.telegram_chat_id = 456
        user.save()
