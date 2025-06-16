from django.conf import settings
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.models import Site
from django.core.mail import BadHeaderError, send_mail
from django.http import HttpResponse
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.views import View
from django.views.generic.edit import FormView

from users.models import User


def logout_user(request):
    logout(request)
    return redirect("user-login")


class LandingView(View):
    def get(self, request):
        if request.user.is_authenticated:
            if not request.user.is_superuser:
                return redirect(reverse_lazy("quotations:quotations"))
            else:
                return redirect(reverse_lazy("users:users"))
        else:
            return redirect(reverse_lazy("user-login"))


class PasswordResetView(FormView):
    template_name = "registration/password_reset.html"
    form_class = PasswordResetForm
    success_url = reverse_lazy("password-reset")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["password_reset_form"] = PasswordResetForm()
        return context

    def form_valid(self, form):
        success_url = super().form_valid(form)
        if form.is_valid():
            email = form.cleaned_data["email"]
            associated_users = User.objects.filter(email__iexact=email)
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "registration/password_reset_email.txt"
                    c = {
                        "email": user.email,
                        "domain": Site.objects.get_current().domain,
                        "site_name": "Website",
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        "token": default_token_generator.make_token(user),
                        "protocol": "http",
                    }
                    text = render_to_string(email_template_name, c)
                    try:
                        send_mail(
                            subject=subject,
                            message=text,
                            from_email=settings.DEFAULT_FROM_EMAIL,
                            recipient_list=[user.email],
                            fail_silently=False,
                        )
                    except BadHeaderError:
                        return HttpResponse("Invalid header found or Send Email Failed")
                    messages.success(self.request, "Reset Password Successfully")
                    return redirect(reverse_lazy("password_reset_done"))
            messages.success(self.request, "Reset Password Successfully")
            return redirect(reverse_lazy("password_reset_done"))
        return success_url
