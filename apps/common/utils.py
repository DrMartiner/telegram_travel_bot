import logging
from typing import Any

__all__ = ["get_object_or_none", "slugify"]

logger = logging.getLogger("django.request")


def get_object_or_none(model: Any, *args, **kwargs) -> Any:
    try:
        return model.objects.get(*args, **kwargs)
    except model.DoesNotExist:
        return None
    except Exception as e:
        logger.exception(f"Getting {model} with {args}, {kwargs} was failure")
        raise e


def slugify(text: str) -> str:
    return (
        text.replace("-", "_")
        .replace(" ", "_")
        .replace(",", "_")
        .replace(".", "_")
        .replace("/", "_")
        .replace("\\", "_")
    )
