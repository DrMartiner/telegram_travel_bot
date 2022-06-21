from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.utils.translation import gettext_lazy as _

from .models import User

__all__ = ["UserAdminForm"]


class UserAdminForm(UserChangeForm):
    email = forms.EmailField(label=_("Email"), required=False)

    def clean_email(self) -> str:
        email = self.cleaned_data.get("email", "").lower()
        if not email:
            return email

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(_("User email '{}' is already exists.").format(email), code="validate")

        return email

    class Meta(UserChangeForm.Meta):
        ...
