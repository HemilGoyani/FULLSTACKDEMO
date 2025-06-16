from django.contrib import messages
from django.contrib.auth import authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView as BaseLoginView
from django.contrib.auth.views import PasswordChangeView, PasswordResetConfirmView
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, RedirectView
from django.views.generic.edit import DeleteView, UpdateView
from django.views.generic.list import ListView

from users.forms import (
    AuthenticationForm,
    ChangePasswordForm,
    ResetPasswordForm,
    UserCreateForm,
    UserProfileForm,
    UserUpdateForm,
    send_invitation,
)
from users.models import User


class UserPermission(object):
    def has_permissions(self):
        return self.get_object().id != self.request.user.id

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permissions():
            return redirect(reverse_lazy("users:users"))

        return super(UserPermission, self).dispatch(request, *args, **kwargs)


class LoginView(BaseLoginView):
    form_class = AuthenticationForm
    success_url = reverse_lazy("users:users")

    def form_valid(self, form):
        """Security check complete. Log the user in."""
        user = form.get_user()
        success_url = super(LoginView, self).form_valid(form)
        self.request.session["pk"] = user.pk
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password"]
        user = User.objects.get(email=username)
        user = authenticate(self.request, email=username, password=password)
        if not user.is_superuser:
            return HttpResponseRedirect(reverse_lazy("quotations:quotations"))

        return success_url


@method_decorator(login_required, name="dispatch")
class OnlyForAdmin:
    def dispatch(self, request, *args, **kwargs):

        if not request.user.is_superuser:
            return redirect(reverse_lazy("quotations:quotations"))

        return super().dispatch(request, *args, **kwargs)


@method_decorator(login_required, name="dispatch")
class UserListView(OnlyForAdmin, ListView):
    model = User
    template_name = "users.html"
    ordering = ["-id"]
    success_url = reverse_lazy("users:users")

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(~Q(email=self.request.user.email))
        return queryset


@method_decorator(login_required, name="dispatch")
class UserCreateView(OnlyForAdmin, CreateView):
    model = User
    form_class = UserCreateForm
    template_name = "user_add.html"
    success_url = reverse_lazy("users:users")


@method_decorator(login_required, name="dispatch")
class UserUpdateView(OnlyForAdmin, UserPermission, UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = "user_update.html"
    success_url = reverse_lazy("users:users")

    def form_valid(self, form):
        success_url = super().form_valid(form)
        return success_url


@method_decorator(login_required, name="dispatch")
class UserDeleteView(OnlyForAdmin, DeleteView):
    model = User
    template_name = "user_delete.html"
    success_url = reverse_lazy("users:users")


@method_decorator(login_required, name="dispatch")
class ChangePasswordView(PasswordChangeView):
    template_name = "registration/change_password.html"
    form_class = ChangePasswordForm
    success_url = reverse_lazy("user-login")

    def form_valid(self, form, *args, **kwargs):
        old_password = self.request.POST.get("old_password")
        new_password1 = self.request.POST.get("new_password1")
        if old_password == new_password1:
            messages.error(self.request, "New password can't be same as old password.")
            return redirect(reverse_lazy("change-password"))
        form.save()

        update_session_auth_hash(self.request, form.user)
        return super().form_valid(form)


@method_decorator(login_required, name="dispatch")
class UserProfileView(UpdateView):
    template_name = "profile.html"
    form_class = UserProfileForm
    success_url = reverse_lazy("users:users")

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        user = self.request.user
        success_url = super().form_valid(form)
        if user.is_superuser:
            return success_url
        return redirect(reverse_lazy("quotations:quotations"))


PasswordResetConfirmView.form_class = ResetPasswordForm
PasswordResetConfirmView.template_name = "registration/password_reset_confirm.html"
PasswordResetConfirmView.success_url = reverse_lazy("password_reset_complete")


@method_decorator(login_required, name="dispatch")
class ResendInvitationView(RedirectView):
    def get_redirect_url(self, pk, *args, **kwargs):
        user = User.objects.get(pk=pk)
        user.is_active = False
        user.save()
        send_invitation(user)
        redirect_url = self.request.build_absolute_uri(reverse("users:users"))
        return redirect_url
