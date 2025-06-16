from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView
from django.views.generic import DeleteView
from django.views.generic import UpdateView
from quotations.models import ThirdPartyItem
from quotations.utils import SCOPE_OF_WORKS
from quotations.utils import TERMS_AND_CONDITION

from settings.forms import ManualItemCreateFormView
from settings.forms import ManualItemUpdateFormView
from settings.forms import TermsAndConditionFormView
from settings.models import Settings


@method_decorator(login_required, name="dispatch")
class TermsAndConditionView(UpdateView):
    model = Settings
    form_class = TermsAndConditionFormView
    template_name = "settings.html"
    success_url = reverse_lazy("settings:settings")

    def get_object(self):
        obj = Settings.objects.first()
        return obj

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return redirect(reverse_lazy("quotations:quotations"))
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        data = Settings.objects.first()
        if not data:
            data = Settings.objects.create(
                terms_and_conditions=TERMS_AND_CONDITION, scope_of_works=SCOPE_OF_WORKS
            )
            data.save()
        context["terms_and_conditions"] = data.terms_and_conditions
        context["scope_of_works"] = data.scope_of_works
        return context

    def post(self, request, *args, **kwargs):
        settings_obj = self.get_object()
        terms_and_conditions = request.POST["terms_and_conditions"]
        scope_of_works = request.POST["scope_of_works"]
        settings_obj.terms_and_conditions = terms_and_conditions
        settings_obj.scope_of_works = scope_of_works
        settings_obj.save()
        return redirect(reverse_lazy("settings:settings"))


@login_required
def update_terms_and_conditions(request):
    data = Settings.objects.first()
    data.terms_and_conditions = request.POST["terms_and_conditions"]
    data.scope_of_works = request.POST["scope_of_works"]
    data.save()
    return redirect(reverse_lazy("settings:settings"))


@method_decorator(login_required, name="dispatch")
class ManageManualItemsView(CreateView):
    model = ThirdPartyItem
    form_class = ManualItemCreateFormView
    template_name = "manage_manual_items.html"
    success_url = reverse_lazy("settings:manage-manual-items")

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return redirect(reverse_lazy("quotations:quotations"))

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(
            **kwargs, manual_items_list=ThirdPartyItem.objects.all()
        )
        return context


@method_decorator(login_required, name="dispatch")
class UpdateManualItemView(UpdateView):
    queryset = ThirdPartyItem.objects.all()
    form_class = ManualItemUpdateFormView
    template_name = "update_manual_item.html"
    success_url = reverse_lazy("settings:manage-manual-items")


@method_decorator(login_required, name="dispatch")
class DeleteManualItemView(DeleteView):
    model = ThirdPartyItem
    template_name = "delete_manual_item.html"
    success_url = reverse_lazy("settings:manage-manual-items")
