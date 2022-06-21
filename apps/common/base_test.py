import io

from PIL import Image

from django.contrib.auth import get_user_model
from django.contrib.sessions.models import Session
from django.test import TestCase

from apps.common.utils import get_object_or_none

User = get_user_model()


class BaseTest(TestCase):
    maxDiff = 5000

    def get_image(self) -> io.BytesIO:
        file = io.BytesIO()
        image = Image.new("RGBA", size=(1, 1))
        image.save(file, "png")
        file.name = "test.png"
        file.seek(0)

        return file

    def assertUserPassword(self, user: User, password: str, will_right=True):
        is_right = user.check_password(password)
        if is_right != will_right:
            if will_right:
                self.fail(f'Password "{password}" is not right for User ID={user.pk}')
            else:
                self.fail(f'Password "{password}" is right User ID={user.pk}')

    def assertSessionId(self, sessionid: str, user_to_compare: User = None) -> None:
        session = get_object_or_none(Session, session_key=sessionid)
        if session is None:
            self.fail(f"Session was not found by sessionid={sessionid}")

        uid = session.get_decoded().get("_auth_user_id")
        user: User = get_object_or_none(User, id=uid)
        if user is None:
            self.fail(f"User was not found by sessionid={sessionid}")

        if user_to_compare is not None:
            if user_to_compare.pk != user.pk:
                self.fail(f"Users ID's are not equal: {user.pk} != {user_to_compare.pk}")
