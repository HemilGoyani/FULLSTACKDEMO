from crispy_forms.helper import FormHelper
from crispy_forms.layout import Button, Submit
from django import forms
from django.core.exceptions import ValidationError

from quotations.models import ThirdPartyItem
from settings.models import Settings


class TermsAndConditionFormView(forms.ModelForm):
    terms_and_conditions = forms.CharField()
    scope_of_works = forms.CharField()

    helper = FormHelper()
    helper.add_input(Submit("submit", "Save", css_class="btn-primary"))
    helper.add_input(
        Button(
            "cancel",
            "Cancel",
            css_class="btn",
            onclick=f"javascript:location.href = '/quotations/';",
        )
    )
    helper.form_method = "POST"

    class Meta:
        model = Settings
        fields = ("terms_and_conditions", "scope_of_works")


class ManualItemCreateFormView(forms.ModelForm):
    helper = FormHelper()
    helper.add_input(Submit("submit", "Save", css_class="btn-primary"))
    helper.add_input(
        Button(
            "cancel",
            "Cancel",
            css_class="btn",
            onclick=f"javascript:location.href = '/settings/';",
        )
    )
    helper.form_method = "POST"

    def clean(self):
        cleaned_data = super(ManualItemCreateFormView, self).clean()
        ps_cost = cleaned_data.get("ps_cost")
        selling_cost = cleaned_data.get("selling_cost")
        if ps_cost >= selling_cost:
            self.add_error(
                "ps_cost", f"  It should be less than selling cost {selling_cost}"
            )
            raise ValidationError("PS cost should be less than selling cost")
        return cleaned_data

    class Meta:
        model = ThirdPartyItem
        fields = (
            "item_name",
            "description",
            "unit",
            "ps_cost",
            "selling_cost",
        )


class ManualItemUpdateFormView(ManualItemCreateFormView):
    helper = FormHelper()
    helper.add_input(Submit("submit", "Save", css_class="btn-primary"))
    helper.add_input(
        Button(
            "cancel",
            "Cancel",
            css_class="btn",
            onclick=f"javascript:location.href = '/settings/manage-other-items/';",
        )
    )
    helper.form_method = "POST"
