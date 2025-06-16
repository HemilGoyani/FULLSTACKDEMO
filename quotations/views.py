import io
from datetime import datetime
from io import BytesIO
from pathlib import Path

from backend.settings import DOMAIN
from django.contrib.auth.decorators import login_required
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.db.models import Q
from django.http import FileResponse
from django.http import Http404
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import redirect
from django.template.loader import get_template
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic.edit import CreateView
from django.views.generic.edit import DeleteView
from django.views.generic.edit import UpdateView
from django.views.generic.list import ListView
from pdf2docx import Converter
from settings.models import Settings
from technologyoptions.models import COMPONENT_CHOICES
from technologyoptions.models import TechnologyOption
from technologyoptions.models import TechnologySubComponent
from technologyoptions.models import TechnologyType
from users.models import User
# from weasyprint import HTML

from quotations.models import Client
from quotations.models import Quotation
from quotations.models import QuotationIntroPara
from quotations.models import QuotationTechnologyOption
from quotations.models import QuotationThirdPartyItem
from quotations.models import ThirdPartyItem
from quotations.utils import SCOPE_OF_WORKS
from quotations.utils import TERMS_AND_CONDITION


@method_decorator(login_required, name="dispatch")
class QuotationListView(ListView):
    template_name = "quotations.html"
    model = Quotation
    context_object_name = "quotations"

    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_superuser:
            if self.request.user.is_reviewer:
                queryset = queryset.filter(
                    Q(reviewer=self.request.user) | Q(creator=self.request.user)
                )
            else:
                queryset = queryset.filter(creator=self.request.user)
        return queryset


class BaseQuotation:
    def get_success_url(self, **kwargs):
        return reverse_lazy(self.success_url_name, args=(self.object.id,))


class QuotationBaseView(BaseQuotation, UpdateView):
    model = Quotation
    queryset = Quotation.objects.all()
    fields = "__all__"

    def dispatch(self, request, *args, **kwargs):
        object = self.get_object()
        if not self.request.user.is_superuser:
            # For creator quotation creator should be current user
            if self.request.user.is_reviewer:
                if not (
                    object.creator == self.request.user
                    or object.reviewer == self.request.user
                ):
                    return redirect(reverse_lazy("quotations:quotations"))
            else:
                if object.creator != self.request.user:
                    return redirect(reverse_lazy("quotations:quotations"))
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        quotation = self.get_object()
        quotation.status = Quotation.DRAFT
        quotation.save()
        return super().post(request, args, kwargs)


@method_decorator(login_required, name="dispatch")
class QuotationCreateView(BaseQuotation, CreateView):
    model = Client
    fields = (
        "name",
        "position",
        "company_name",
        "company_address",
    )
    template_name = "distributor_or_client_details.html"
    success_url_name = "quotations:choose-technology-type"

    def get_context_data(self, **kwargs):
        context = {}
        context["clients"] = Client.objects.all()
        return context

    def post(self, form):
        try:
            client = Client.objects.filter(id=self.request.POST["name"]).first()
        except:
            client = Client.objects.create(
                name=self.request.POST.get("name"),
                position=self.request.POST.get("position"),
                company_name=self.request.POST.get("company_name"),
                company_address=self.request.POST.get("company_address"),
            )
            client.save()
        company_name = [x[0] for x in client.company_name.split(" ")]
        company_char = "".join(company_name).upper()
        creator = (
            [x[0] for x in self.request.user.name.split(" ")]
            if self.request.user.name
            else self.request.user.email[0:2]
        )
        creator_char = "".join(creator).upper()
        x = datetime.today()
        quotation_number = (
            x.strftime("%Y")
            + x.strftime("%m")
            + x.strftime("%d")
            + "-"
            + company_char
            + "-"
            + creator_char
        )
        data = Quotation.objects.filter(
            quotation_number__startswith=quotation_number
        ).count()
        if data:
            quotation_number = quotation_number + "-" + str(data + 1)
        quotation_obj = Quotation.objects.create(
            client_id=client.id if client else form.instance.id,
            creator=self.request.user,
            quotation_number=quotation_number,
        )
        quotation_obj.save()
        return redirect(
            reverse_lazy(
                "quotations:choose-technology-type", kwargs={"pk": quotation_obj.id}
            )
        )


@method_decorator(login_required, name="dispatch")
class QuotationUpdateView(QuotationBaseView):
    model = Client
    fields = (
        "name",
        "position",
        "company_name",
        "company_address",
    )
    template_name = "distributor_or_client_details.html"
    success_url_name = "quotations:choose-technology-type"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["clients"] = Client.objects.all()
        data = Quotation.objects.filter(id=self.get_object().id).first()
        context["selected_name"] = data.client.name
        return context

    def post(self, *args, **kwargs):
        try:
            client = Client.objects.filter(id=self.request.POST["name"]).first()
        except:
            client = Client.objects.create(
                name=self.request.POST.get("name"),
                position=self.request.POST.get("position"),
                company_name=self.request.POST.get("company_name"),
                company_address=self.request.POST.get("company_address"),
            )
            client.save()
        data = Quotation.objects.filter(id=self.kwargs["pk"]).first()
        data.client_id = client.id
        data.save()
        return redirect(
            reverse_lazy(
                "quotations:choose-technology-type", kwargs={"pk": self.kwargs["pk"]}
            )
        )


@method_decorator(login_required, name="dispatch")
class DeleteQuotationView(DeleteView):
    model = Quotation
    template_name = "delete_quotation.html"
    success_url = reverse_lazy("quotations:quotations")


@method_decorator(login_required, name="dispatch")
class ChooseTechnologyTypeView(QuotationBaseView):
    template_name = "choose_technology_type.html"
    fields = ("technology_type",)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(
            **kwargs,
            technology_types=TechnologyType.objects.all(),
            selected_technology_types=self.get_object().technology_type.all(),
        )
        return context

    def post(self, request, *args, **kwargs):
        super().post(request, args, kwargs)
        quotation = self.get_object()
        quotation.technology_type.set(
            TechnologyType.objects.filter(
                type__in=request.POST.getlist("technology_type")
            ).all()
        )
        quotation.save()

        technology_types = list(quotation.technology_type.all())

        for technology_type in technology_types:
            if not QuotationIntroPara.objects.filter(
                quotation=quotation, technology_type=technology_type
            ).first():
                QuotationIntroPara.objects.create(
                    quotation=quotation,
                    technology_type=technology_type,
                    intro_para=technology_type.intro_para,
                )
        setting_obj = Settings.objects.first()
        if not setting_obj:
            setting_obj = Settings.objects.create(
                terms_and_conditions=TERMS_AND_CONDITION, scope_of_works=SCOPE_OF_WORKS
            )
        if not quotation.terms_and_conditions:
            quotation.terms_and_conditions = setting_obj.terms_and_conditions

        if not quotation.scope_of_work:
            quotation.scope_of_work = setting_obj.scope_of_works

        quotation.save()

        for technology_type in technology_types:

            technology_components = [key for key, val in COMPONENT_CHOICES.choices]

            for technology_component in technology_components:

                for technology_subcomponent in TechnologySubComponent.objects.filter(
                    technology_type__type=technology_type,
                    technology_component=technology_component,
                ).all():

                    item = TechnologyOption.objects.filter(
                        technology_type__type=technology_type,
                        technology_component=technology_component,
                        technology_sub_component=technology_subcomponent,
                    ).first()

                    if item:

                        cost = item.distribution_cost if item.distribution_cost else 0
                        if quotation.user_type == Quotation.ENDUSER:
                            cost = item.end_user_cost if item.end_user_cost else 0
                        technology_option = QuotationTechnologyOption.objects.filter(
                            quotation=quotation,
                            technology_type=technology_type,
                            technology_component=technology_component,
                            sub_component=technology_subcomponent,
                            part_number=item.part_number,
                        ).first()

                        if technology_option:
                            technology_option.description = item.description
                            technology_option.selling_cost = cost
                            technology_option.ps_cost = (
                                item.ps_cost if item.ps_cost else 0
                            )
                            technology_option.unit = item.unit
                            technology_option.save()
                        else:
                            QuotationTechnologyOption.objects.create(
                                quotation=quotation,
                                technology_type=technology_type,
                                technology_component=technology_component,
                                sub_component=technology_subcomponent,
                                description=item.description,
                                part_number=item.part_number,
                                ps_cost=item.ps_cost if item.ps_cost else 0,
                                selling_cost=cost,
                                unit=item.unit,
                                category=item.category,
                            )

        return redirect(
            reverse_lazy(
                "quotations:choose-user-type-distributor-or-client",
                kwargs={
                    "pk": self.get_object().id,
                },
            )
        )


@method_decorator(login_required, name="dispatch")
class ChooseUseTypeView(QuotationBaseView):
    template_name = "choose_user_type_distributor_or_client.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(
            **kwargs,
            user_types=Quotation.END_USERS_CHOICES,
            selected_user_type=self.get_object().user_type,
        )
        return context

    def post(self, request, *args, **kwargs):
        super().post(request, args, kwargs)
        quotation = self.get_object()
        if quotation.user_type != request.POST["user_type"]:
            technology_types = list(quotation.technology_type.all())

            for technology_type in technology_types:

                technology_components = [key for key, val in COMPONENT_CHOICES.choices]

                for technology_component in technology_components:

                    for (
                        technology_subcomponent
                    ) in TechnologySubComponent.objects.filter(
                        technology_type__type=technology_type,
                        technology_component=technology_component,
                    ).all():

                        for (
                            technology_option
                        ) in QuotationTechnologyOption.objects.filter(
                            quotation=quotation,
                            technology_type__type=technology_type,
                            technology_component=technology_component,
                            sub_component=technology_subcomponent,
                        ).all():

                            item = TechnologyOption.objects.filter(
                                technology_type=technology_type,
                                technology_component=technology_component,
                                technology_sub_component=technology_subcomponent,
                                part_number=technology_option.part_number,
                            ).first()

                            cost = (
                                item.distribution_cost if item.distribution_cost else 0
                            )
                            if request.POST["user_type"] == Quotation.ENDUSER:
                                cost = item.end_user_cost if item.end_user_cost else 0

                            technology_option.description = item.description
                            technology_option.selling_cost = cost
                            technology_option.ps_cost = (
                                item.ps_cost if item.ps_cost else 0
                            )
                            technology_option.unit = item.unit
                            technology_option.save()

        quotation.user_type = request.POST["user_type"]
        quotation.save()

        return redirect(
            reverse_lazy(
                "quotations:tech-options-selection",
                kwargs={
                    "pk": self.kwargs["pk"],
                    "component": "1-Hardware",
                },
            )
        )


class TechnologyOptionsSelectionView(QuotationBaseView):
    components_dict = dict(COMPONENT_CHOICES.choices)
    components = list(dict(COMPONENT_CHOICES.choices).keys())
    template_name = "select_technology_options.html"

    def get_context_data(self, **kwargs):

        context = super().get_context_data(
            **kwargs,
            technology_component=self.kwargs["component"],
        )
        current_component_index = self.components.index(self.kwargs["component"])
        if not current_component_index:
            context["back_url"] = reverse_lazy(
                "quotations:choose-user-type-distributor-or-client",
                kwargs={"pk": self.kwargs["pk"]},
            )
        else:
            context["back_url"] = reverse_lazy(
                "quotations:tech-options-selection",
                kwargs={
                    "pk": self.kwargs["pk"],
                    "component": self.components[current_component_index - 1],
                },
            )
        context["component"] = self.components_dict[self.kwargs["component"]]
        context["subcomponents"] = TechnologySubComponent.objects.filter(
            technology_component=self.kwargs["component"]
        )
        return context

    def post(self, request, *args, **kwargs):
        super().post(request, args, kwargs)
        current_component = self.kwargs["component"]
        quotation = self.get_object()

        options = request.POST.getlist("part_number")
        selling_costs = request.POST.getlist("selling_cost")
        quantitys = request.POST.getlist("quantity")
        comments = request.POST.getlist("comment")

        # Delete all Quotation Products / Part Numbers for the current component
        QuotationTechnologyOption.objects.filter(
            quotation=quotation,
            technology_component=current_component,
        ).delete()

        for index, option_id in enumerate(options):
            item = TechnologyOption.objects.get(id=option_id)

            # Create Quotation Technology option for current component
            QuotationTechnologyOption.objects.create(
                quotation=quotation,
                technology_type=item.technology_type,
                technology_component=item.technology_component,
                sub_component=item.technology_sub_component.sublist_item_name,
                description=item.description,
                part_number=item.part_number,
                unit=item.unit,
                quantity=quantitys[index],
                ps_cost=item.ps_cost,
                selling_cost=selling_costs[index],
                comment=str(comments[index]).strip(),
                category=item.category,
            )

        current_component_index = self.components.index(current_component)
        if current_component_index == len(self.components) - 1:
            return redirect(
                reverse_lazy(
                    "quotations:add-manual-items",
                    kwargs={"pk": self.kwargs["pk"]},
                )
            )
        else:
            return redirect(
                reverse_lazy(
                    "quotations:tech-options-selection",
                    kwargs={
                        "pk": self.kwargs["pk"],
                        "component": self.components[current_component_index + 1],
                    },
                )
            )


@login_required
def get_part_numbers_from_sub_component(request, pk):
    data = list(
        TechnologyOption.objects.filter(technology_sub_component_id=pk).values()
    )
    return JsonResponse(data, safe=False)


class AddManualItemsView(QuotationBaseView):
    template_name = "add_manual_items.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(
            **kwargs, third_party_items=ThirdPartyItem.objects.all()
        )

        return context

    def post(self, request, *args, **kwargs):
        super().post(request, args, kwargs)
        quotation = self.get_object()
        manual_items = request.POST.getlist("item_name")
        descriptions = request.POST.getlist("description")
        units = request.POST.getlist("unit")
        ps_costs = request.POST.getlist("ps_cost")
        selling_costs = request.POST.getlist("selling_cost")
        quantitys = request.POST.getlist("quantity")
        comments = request.POST.getlist("comment")

        # Delete all Quotation ThirdPartyItem for the current quotation
        QuotationThirdPartyItem.objects.filter(
            quotation=quotation,
        ).delete()

        for index, item_name in enumerate(manual_items):

            # Create Quotation Third Party Item  for current quotation
            QuotationThirdPartyItem.objects.create(
                quotation=quotation,
                item_name=item_name,
                description=descriptions[index],
                unit=units[index],
                ps_cost=ps_costs[index],
                selling_cost=selling_costs[index],
                quantity=quantitys[index],
                comment=str(comments[index]).strip(),
            )

            if not ThirdPartyItem.objects.filter(item_name__iexact=item_name).first():
                ThirdPartyItem.objects.create(
                    item_name=item_name,
                    description=descriptions[index],
                    unit=units[index],
                    ps_cost=ps_costs[index],
                    selling_cost=selling_costs[index],
                )

        return redirect(
            reverse_lazy(
                "quotations:choose-quotation-type",
                kwargs={"pk": self.get_object().id},
            )
        )


class ChooseQuotationTypeView(QuotationBaseView):
    template_name = "choose_quotation_type.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(
            **kwargs,
            quotation_type_list=Quotation.QUOTATION_TYPE_CHOICES.choices,
            selected_quotation_type=self.get_object().quotation_type,
        )
        return context

    def post(self, request, *args, **kwargs):
        super().post(request, args, kwargs)
        quotation = self.get_object()
        quotation.quotation_type = request.POST["quotation_type"]
        quotation.subscription_months = request.POST["subscription_months"]
        quotation.kick_off_fee = request.POST["kick_off_fee"]
        quotation.save()
        return redirect(
            reverse_lazy(
                "quotations:quotation-intro-para",
                kwargs={"pk": quotation.id},
            )
        )


class QuotationIntroParaView(QuotationBaseView):
    template_name = "intro_para.html"

    def get_context_data(self, **kwargs):
        quotation = self.get_object()
        context = super().get_context_data(
            **kwargs,
            selected_technology_types=list(quotation.technology_type.all()),
            quotation_intro_paras=QuotationIntroPara.objects.filter(
                quotation=quotation
            ).all(),
        )
        return context

    def post(self, request, *args, **kwargs):
        super().post(request, args, kwargs)
        quotation = self.get_object()
        for technology_type in list(quotation.technology_type.all()):
            QuotationIntroPara.objects.filter(
                quotation=quotation, technology_type=technology_type
            ).update(intro_para=request.POST[f"{technology_type.type}_intro_para"])
        return redirect(
            reverse_lazy(
                "quotations:quotation-terms-and-conditions",
                kwargs={"pk": quotation.id},
            )
        )


class QuotationTermsAndConditionView(QuotationBaseView):
    template_name = "terms_&_condition.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(
            **kwargs, terms_and_conditions=self.get_object().terms_and_conditions
        )
        return context

    def post(self, request, *args, **kwargs):
        super().post(request, args, kwargs)
        quotation = self.get_object()
        quotation.terms_and_conditions = request.POST["terms_and_conditions"]
        quotation.save()
        return redirect(
            reverse_lazy(
                "quotations:quotation-scope-of-works",
                kwargs={"pk": quotation.id},
            )
        )


class QuotationScopeOfWorksView(QuotationBaseView):
    template_name = "scope_of_works.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(
            **kwargs, scope_of_work=self.get_object().scope_of_work
        )
        return context

    def post(self, request, *args, **kwargs):
        super().post(request, args, kwargs)
        quotation = self.get_object()
        quotation.scope_of_work = request.POST["scope_of_works"]
        quotation.save()
        return redirect(
            reverse_lazy(
                "quotations:quotation-summary",
                kwargs={"pk": quotation.id},
            )
        )


class QuotationSummaryView(QuotationBaseView):
    template_name = "quotation_summary.html"

    def get_context_data(self, **kwargs):
        quotation = self.get_object()
        reviewers_list = User.objects.filter(Q(is_superuser=True) | Q(is_reviewer=True))
        components_dict = dict(COMPONENT_CHOICES.choices)
        cost_list = {
            component: QuotationTechnologyOption.total_cost(
                quotation.id,
                component,
            )
            for component, val in components_dict.items()
        }
        cost_summary_onoff = [
            {
                "component": val,
                "total_cost": QuotationTechnologyOption.total_cost(
                    quote_id=quotation.id, component=component, category="one off"
                ),
                "total_spl": QuotationTechnologyOption.total_spl(
                    quote_id=quotation.id, component=component, category="one off"
                ),
            }
            for component, val in components_dict.items()
        ]
        cost_summary_ongoing = [
            {
                "component": val,
                "total_cost": QuotationTechnologyOption.total_cost(
                    quote_id=quotation.id, component=component, category="on going"
                ),
                "total_spl": QuotationTechnologyOption.total_spl(
                    quote_id=quotation.id, component=component, category="on going"
                ),
            }
            for component, val in components_dict.items()
        ]

        third_party_total_spl = QuotationThirdPartyItem.total_spl(quotation.id)
        component_spl_list = {
            component: QuotationTechnologyOption.total_spl(
                quote_id=quotation.id,
                component=component,
            )
            for component in list(dict(COMPONENT_CHOICES.choices).keys())
        }

        third_party_total_cost = QuotationThirdPartyItem.total_cost(quotation.id)

        quotation_total_spl_onoff = QuotationTechnologyOption.total_spl(
            quotation.id, category="one off"
        )
        quotation_total_cost_onoff = QuotationTechnologyOption.total_cost(
            quotation.id, category="one off"
        )

        quotation_total_spl_ongoing = (
            QuotationTechnologyOption.total_spl(quotation.id, category="on going")
            + third_party_total_spl
        )

        quotation_total_cost_ongoing = (
            QuotationTechnologyOption.total_cost(quotation.id, category="on going")
            + third_party_total_cost
        )

        queryset_list = {
            component: QuotationTechnologyOption.objects.filter(
                quotation=quotation, technology_component=component
            ).exists()
            for component, val in components_dict.items()
        }
        queryset_list["Manual_items"] = QuotationThirdPartyItem.objects.filter(
            quotation=quotation
        ).exists()

        monthly_installment = 0

        if (
            quotation_total_cost_onoff
            and quotation.kick_off_fee
            and quotation.subscription_months
        ):
            monthly_installment = (
                quotation_total_cost_onoff - quotation.kick_off_fee
            ) / quotation.subscription_months
        context = super().get_context_data(
            **kwargs,
            selected_technology_types=list(quotation.technology_type.all()),
            reviewers_list=reviewers_list,
            cost_list=cost_list,
            cost_summary_onoff=cost_summary_onoff,
            cost_summary_ongoing=cost_summary_ongoing,
            components_dict=components_dict,
            third_party_total_cost=third_party_total_cost,
            quotation_total_cost_onoff=quotation_total_cost_onoff,
            quotation_total_spl_onoff=quotation_total_spl_onoff,
            quotation_total_cost_ongoing=quotation_total_cost_ongoing,
            quotation_total_spl_ongoing=quotation_total_spl_ongoing,
            third_party_total_spl=third_party_total_spl,
            component_spl_list=component_spl_list,
            queryset_list=queryset_list,
            subscription_months=quotation.subscription_months,
            kick_off_fee=quotation.kick_off_fee,
            selected_reviewer=quotation.reviewer,
            monthly_installment=monthly_installment,
        )
        return context

    def post(self, request, *args, **kwargs):
        quotation = self.get_object()
        quotation.reviewer = User.objects.get(pk=request.POST["quotation_reviewer"])
        quotation.status = Quotation.WAITING_FOR_APPROVAL
        quotation.is_approved = False
        quotation.header = request.POST["header"]
        quotation.description = request.POST["description"]
        quotation.is_intropara = (
            True if request.POST.get("is_intropara") == "on" else False
        )
        quotation.is_terms_and_condition = (
            True if request.POST.get("is_terms_and_condition") == "on" else False
        )
        quotation.is_scope_of_work = (
            True if request.POST.get("is_scope_of_work") == "on" else False
        )
        quotation.is_background = (
            True if request.POST.get("background_selection") == "on" else False
        )
        quotation.save()
        return redirect(
            reverse_lazy(
                "quotations:quotations",
            )
        )


def quotation_update_status(request, id):
    data = Quotation.objects.filter(id=id).first()
    data.is_approved = True
    data.status = Quotation.COMPLETED
    data.save()
    return redirect(reverse_lazy("quotations:quotations"))


def quotation_details(request, pk):
    quotation = Client.objects.filter(id=pk).first()
    data = {}
    if quotation:
        data["position"] = quotation.position
        data["company"] = quotation.company_name
        data["company_address"] = quotation.company_address
        response = JsonResponse(data)
    else:
        quotation = None
        response = Http404
    return response


# def render_to_pdf(template_src, data):
#     template = get_template(template_src)
#     html = template.render(data)
#     html = HTML(string=BytesIO(html.encode("cp1252")), encoding="utf8")
#     pdf = html.write_pdf()
#     return pdf


def get_quotation_data(pk):
    quotation = Quotation.objects.filter(id=pk).first()
    reviewers_list = User.objects.filter(Q(is_superuser=True) | Q(is_reviewer=True))
    components_dict = dict(COMPONENT_CHOICES.choices)

    cost_list = {
        component: QuotationTechnologyOption.total_cost(quotation.id, component)
        for component, val in components_dict.items()
    }
    typevise_cost_list = {
        component: {
            technology_type: QuotationTechnologyOption.total_cost(
                quotation.id, component=component, technology_type=technology_type
            )
            for technology_type in list(quotation.technology_type.all())
        }
        for component, val in components_dict.items()
    }
    third_party_total_cost = QuotationThirdPartyItem.total_cost(quotation.id)
    cost_summary_oneoff = [
        {
            "component": val,
            "total_cost": QuotationTechnologyOption.total_cost(
                quote_id=quotation.id, component=component, category="one off"
            ),
            "total_spl": QuotationTechnologyOption.total_spl(
                quote_id=quotation.id, component=component, category="one off"
            ),
        }
        for component, val in components_dict.items()
    ]
    cost_summary_ongoing = [
        {
            "component": val,
            "total_cost": QuotationTechnologyOption.total_cost(
                quote_id=quotation.id, component=component, category="on going"
            ),
            "total_spl": QuotationTechnologyOption.total_spl(
                quote_id=quotation.id, component=component, category="on going"
            ),
        }
        for component, val in components_dict.items()
    ]

    third_party_total_cost = QuotationThirdPartyItem.total_cost(quotation.id)

    quotation_total_cost_oneoff = QuotationTechnologyOption.total_cost(
        quotation.id, category="one off"
    )

    quotation_total_cost_ongoing = (
        QuotationTechnologyOption.total_cost(quotation.id, category="on going")
        + third_party_total_cost
    )

    monthly_installment = 0

    if (
        quotation_total_cost_oneoff
        and quotation.kick_off_fee
        and quotation.subscription_months
    ):
        monthly_installment = (
            quotation_total_cost_oneoff - quotation.kick_off_fee
        ) / quotation.subscription_months

    data = {
        "quotation": quotation,
        "selected_technology_types": list(quotation.technology_type.all()),
        "reviewers_list": reviewers_list,
        "cost_list": cost_list,
        "typevise_cost_list": typevise_cost_list,
        "quotation_total_cost_oneoff": quotation_total_cost_oneoff,
        "quotation_total_cost_ongoing": quotation_total_cost_ongoing,
        "subscription_months": quotation.subscription_months,
        "kick_off_fee": quotation.kick_off_fee,
        "cost_summary_oneoff": cost_summary_oneoff,
        "cost_summary_ongoing": cost_summary_ongoing,
        "domain": DOMAIN,
        "monthly_installment": monthly_installment,
        "quotation_number": quotation.quotation_number,
        "third_party_total_cost": third_party_total_cost,
    }
    return data


# def download_quotation_pdf(request, pk):
#     data = get_quotation_data(pk)
#     template_src = "quotation_pdf.html"
#     pdf = render_to_pdf(template_src, data)
#     response = FileResponse(ContentFile(pdf), content_type="application/pdf")
#     response["Content-Disposition"] = "attachment; filename={}.pdf".format(
#         data["quotation_number"]
#     )
#     return response


import tempfile


# def download_quotation_docx(request, pk):
#     data = get_quotation_data(pk)
#     template_src = "quotation_docx.html"
#     pdf = render_to_pdf(template_src, data)
#     with tempfile.TemporaryDirectory() as tmpdirname:
#         print("created temporary directory", tmpdirname, "\n\n\n")
#         with open(f"{tmpdirname}/{data['quotation_number']}.pdf", "wb") as file:
#             file.write(pdf)
#         pdf_to_doc = Converter(f"{tmpdirname}/{data['quotation_number']}.pdf")
#         with open(f"{tmpdirname}/{data['quotation_number']}.docx", "w") as file:
#             # Converting PDF to Docx
#             pdf_to_doc.convert(f"{tmpdirname}/{data['quotation_number']}.docx")
#             pdf_to_doc.close()

#         with open(f"{tmpdirname}/{data['quotation_number']}.docx", "rb") as file:
#             bio = file.read()
#         response = FileResponse(
#             ContentFile(bio, "{}.docx".format(data["quotation_number"])),
#             content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
#         )
#     return response
