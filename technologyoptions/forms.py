from crispy_forms.helper import FormHelper
from crispy_forms.layout import Button
from crispy_forms.layout import Submit
from django import forms

from technologyoptions.models import TechnologyOption
from technologyoptions.models import TechnologySubComponent
from technologyoptions.models import TechnologyType


class TechnologyTypeCreateForm(forms.ModelForm):
    helper = FormHelper()
    helper.add_input(Submit("submit", "Save", css_class="btn-primary"))
    helper.add_input(
        Button(
            "cancel",
            "Cancel",
            css_class="btn",
            onclick=f"javascript:location.href = '/product-or-part-numbers/';",
        )
    )
    helper.form_method = "POST"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["image"].required = True

    class Meta:
        model = TechnologyType
        fields = (
            "type",
            "image",
            "intro_para",
        )


class TechnologyTypeUpdateForm(TechnologyTypeCreateForm):
    helper = FormHelper()
    helper.add_input(Submit("submit", "Save", css_class="btn-primary"))
    helper.add_input(
        Button(
            "cancel",
            "Cancel",
            css_class="btn",
            onclick=f"javascript:location.href = '/product-or-part-numbers/add-technology-or-service/';",
        )
    )
    helper.form_method = "POST"


class TechnologyOptionCreateForm(forms.ModelForm):
    helper = FormHelper()
    helper.add_input(Submit("submit", "Save", css_class="btn-primary"))
    helper.add_input(
        Button(
            "cancel",
            "Cancel",
            css_class="btn",
            onclick=f"javascript:location.href = '/product-or-part-numbers/';",
        )
    )
    helper.form_method = "POST"

    class Meta:
        model = TechnologyOption
        fields = (
            "technology_type",
            "technology_component",
            "technology_sub_component",
            "part_number",
            "description",
            "unit",
            "category",
            "ps_cost",
            "distribution_cost",
            "end_user_cost",
        )


class TechnologySubComponentCreateForm(forms.ModelForm):
    helper = FormHelper()
    helper.add_input(Submit("submit", "Save", css_class="btn-primary"))
    helper.add_input(
        Button(
            "cancel",
            "Cancel",
            css_class="btn",
            onclick=f"javascript:location.href = '/product-or-part-numbers/';",
        )
    )
    helper.form_method = "POST"

    class Meta:
        model = TechnologySubComponent
        fields = (
            "technology_type",
            "technology_component",
            "sublist_item_name",
        )


class TechnologySubComponentUpdateForm(TechnologySubComponentCreateForm):
    helper = FormHelper()
    helper.add_input(Submit("submit", "Save", css_class="btn-primary"))
    helper.add_input(
        Button(
            "cancel",
            "Cancel",
            css_class="btn",
            onclick=f"javascript:location.href = '/product-or-part-numbers/technology-or-service-sub-component/add/';",
        )
    )
    helper.form_method = "POST"
