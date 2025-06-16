from crispy_forms.helper import FormHelper
from crispy_forms.layout import Button, Submit
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm as BaseAuthenticationForm
from django.contrib.auth.forms import (
    PasswordChangeForm,
    PasswordResetForm,
    SetPasswordForm,
)
from django.contrib.sites.models import Site
from dotenv import load_dotenv

from users.models import User

UserModel = get_user_model()

load_dotenv()


def send_invitation(user):
    reset_password_form = PasswordResetForm(data={"email": user.email})
    if reset_password_form.is_valid():

        reset_password_form.save(
            Site.objects.get_current().domain,
            subject_template_name="registration/account_creation_subject.txt",
            html_email_template_name="registration/account_creation_email.html",
        )


class AuthenticationForm(BaseAuthenticationForm):
    helper = FormHelper()
    helper.add_input(
        Submit(
            "submit",
            "Login",
            css_class="btn-pink btn-block text-uppercase",
        )
    )
    helper.form_method = "POST"


class ChangePasswordForm(PasswordChangeForm):
    helper = FormHelper()
    helper.add_input(Submit("submit", "Change Password", css_class="btn-primary"))
    helper.add_input(
        Button(
            "cancel",
            "Cancel",
            css_class="btn",
            onclick=f"javascript:location.href = '/users/';",
        )
    )
    helper.form_method = "POST"


class ResetPasswordForm(SetPasswordForm):
    helper = FormHelper()
    helper.add_input(
        Submit(
            "submit",
            "Set Password",
            css_class="btn-pink btn-block text-uppercase",
        )
    )
    helper.form_method = "POST"

    def save(self, commit=True):
        password = self.cleaned_data["new_password1"]
        self.user.set_password(password)
        if commit:
            self.user.is_active = True
            self.user.save()
        return self.user


class UserCreateForm(forms.ModelForm):

    helper = FormHelper()
    helper.add_input(Submit("submit", "Submit", css_class="btn-primary"))
    helper.add_input(
        Button(
            "cancel",
            "Cancel",
            css_class="btn",
            onclick=f"javascript:location.href = '/users/';",
        )
    )

    class Meta:
        model = User
        fields = [
            "name",
            "position",
            "email",
            "phone",
            "is_reviewer",
        ]

    def save(self, commit=True):
        user = super().save(commit=False)

        user.name = self.cleaned_data["name"]
        user.position = self.cleaned_data["position"]
        user.email = self.cleaned_data["email"]
        user.phone = self.cleaned_data["phone"]
        user.is_reviewer = self.cleaned_data["is_reviewer"]

        if commit:
            user.save()
        send_invitation(user)
        user.is_active = False
        user.save()
        return user


class UserUpdateForm(forms.ModelForm):
    helper = FormHelper()
    helper.add_input(Submit("submit", "Submit", css_class="btn-primary"))
    helper.add_input(
        Button(
            "cancel",
            "Cancel",
            css_class="btn",
            onclick=f"javascript:location.href = '/users/';",
        )
    )
    helper.form_method = "POST"

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        return user

    class Meta:
        model = User
        fields = ["name", "position", "email", "phone", "is_reviewer"]


class UserProfileForm(UserUpdateForm):
    class Meta:
        model = User
        fields = ["name", "position", "email", "phone"]
