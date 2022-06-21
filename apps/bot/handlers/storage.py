from typing import Any

import redis

from django.conf import settings

__all__ = ["storage"]

pool = redis.ConnectionPool(host=settings.REDIS_HOST, port=6379, db=0)
client = redis.Redis(connection_pool=pool)


class Storage:
    @staticmethod
    def set(user_id: int, name: str, value: Any) -> None:
        client.set(f"{user_id}::{name}", value)

    @staticmethod
    def get(user_id: int, name: str) -> Any:
        value = client.get(f"{user_id}::{name}")
        if value:
            return value.decode("utf-8")

    @staticmethod
    def delete(user_id: int, name: str) -> None:
        client.delete(f"{user_id}::{name}")

    @staticmethod
    def flush(user_id: int, prefix: str = None) -> None:
        client.delete(f"{user_id}::{prefix or ''}*")

    @staticmethod
    def clean(user_id):
        client.delete(f"{user_id}::*")


storage = Storage()
