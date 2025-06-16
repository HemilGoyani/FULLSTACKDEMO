from decimal import Decimal

from backend.models import BaseModel
from django.db import models
from django.db.models import F
from django.db.models import Q
from django.db.models import Sum
from django.utils.translation import gettext_lazy as _
from technologyoptions.models import COMPONENT_CHOICES
from technologyoptions.models import UNIT_CHOICES
from technologyoptions.models import TechnologyOption
from technologyoptions.models import TechnologyType
from users.models import User


class ThirdPartyItem(BaseModel):
    item_name = models.CharField(max_length=80, unique=True)
    description = models.TextField()
    unit = models.CharField(max_length=40)
    ps_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    selling_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self) -> str:
        return str(self.item_name)

    class Meta:
        verbose_name = "ThirdPartyItem"
        verbose_name_plural = "ThirdPartyItems"


class Client(BaseModel):
    name = models.CharField(max_length=20, verbose_name="Full Name")
    position = models.CharField(
        max_length=20,
        verbose_name="Customer Position",
    )
    company_name = models.CharField(
        max_length=20,
        verbose_name="Company Name",
    )
    company_address = models.CharField(
        max_length=120,
        verbose_name="Company Address",
    )

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "Client"
        verbose_name_plural = "Clients"


class Quotation(BaseModel):

    DRAFT = "draft"
    WAITING_FOR_APPROVAL = "waiting for approval"
    COMPLETED = "completed"
    STATUSES = (
        (DRAFT, "Draft"),
        (WAITING_FOR_APPROVAL, "Waiting for Approval"),
        (COMPLETED, "Completed"),
    )

    DISTRIBUTOR = "distributor"
    ENDUSER = "end_user"
    END_USERS_CHOICES = ((DISTRIBUTOR, "Distributor"), (ENDUSER, "End User"))

    class QUOTATION_TYPE_CHOICES(models.TextChoices):
        LUMP_SUM = "lump_sum", _("Lump Sum")
        ITEMIZED = "itemized", _("Itemized")
        SUBSCRIPTION_BASED = "subscription_based", _("Subscription Based")

    client = models.ForeignKey(
        Client, on_delete=models.PROTECT, related_name="quotations"
    )

    creator = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name="created_quotations"
    )
    reviewer = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="reviewed_quotations",
        blank=True,
        null=True,
    )
    technology_type = models.ManyToManyField(
        TechnologyType,
        related_name="quotations",
    )
    user_type = models.CharField(
        choices=END_USERS_CHOICES, max_length=12, default=DISTRIBUTOR
    )

    quotation_type = models.CharField(
        choices=QUOTATION_TYPE_CHOICES.choices,
        max_length=20,
        default=QUOTATION_TYPE_CHOICES.LUMP_SUM,
    )

    subscription_months = models.IntegerField(blank=True, default=1)
    kick_off_fee = models.DecimalField(
        max_digits=10, decimal_places=2, default=0, blank=True, null=True
    )
    approved_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    approved_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="approved_quotations",
        null=True,
        blank=True,
    )
    terms_and_conditions = models.TextField(null=True)
    scope_of_work = models.TextField(null=True)
    status = models.CharField(choices=STATUSES, default=DRAFT, max_length=30)
    is_approved = models.BooleanField(default=False)
    quotation_number = models.CharField(
        max_length=20, null=True, blank=True, unique=True
    )
    header = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    is_intropara = models.BooleanField(default=True)
    is_terms_and_condition = models.BooleanField(default=True)
    is_scope_of_work = models.BooleanField(default=True)
    is_background = models.BooleanField(default=True)

    def __str__(self) -> str:
        return f"{self.client.name} - {self.creator}"

    class Meta:
        verbose_name = "Quotation"
        verbose_name_plural = "Quotations"


class QuotationTechnologyOption(BaseModel):
    quotation = models.ForeignKey(
        Quotation, on_delete=models.CASCADE, related_name="quotation_technology_options"
    )
    technology_type = models.ForeignKey(
        TechnologyType,
        on_delete=models.PROTECT,
    )
    technology_component = models.CharField(
        choices=COMPONENT_CHOICES.choices,
        max_length=255,
    )
    sub_component = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    part_number = models.CharField(max_length=80)
    unit = models.CharField(
        max_length=50,
        default=UNIT_CHOICES.PERITEM,
        choices=UNIT_CHOICES.choices,
    )
    quantity = models.IntegerField(default=1)
    ps_cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
    )
    selling_cost = models.DecimalField(
        max_digits=10, decimal_places=2, default=0, null=True
    )
    comment = models.TextField(max_length=255, blank=True, null=True)
    category = models.CharField(
        choices=TechnologyOption.STATUSES, max_length=30, null=True, blank=False
    )

    @property
    def spl(self):
        spl = Decimal(0.00)
        if (self.selling_cost) and (self.ps_cost):
            spl = (self.selling_cost / self.ps_cost) * 100
        return spl.quantize(Decimal("1.00"))

    @staticmethod
    def total_spl(quote_id, component=None, technology_type=None, category=None):
        query = Q(quotation_id=quote_id)
        if technology_type:
            query = query & Q(technology_type=technology_type)

        if component:
            query = query & Q(technology_component=component)

        if category:
            query = query & Q(category=category)

        total_spl = 0
        for option in QuotationTechnologyOption.objects.filter(query):
            total_spl += (option.selling_cost / option.ps_cost) * 100
        return total_spl

    @staticmethod
    def total_cost(quote_id, component=None, technology_type=None, category=None):
        component_total_cost = 0.00
        query = Q(quotation_id=quote_id)
        if component:
            query = query & Q(technology_component=component)
        if technology_type:
            query = query & Q(technology_type=technology_type)
        if category:
            query = query & Q(category=category)

        component_total_cost = (
            QuotationTechnologyOption.objects.filter(query)
            .annotate(total_cost=F("selling_cost") * F("quantity"))
            .aggregate(total_sum=Sum("total_cost"))
        )

        if component_total_cost["total_sum"]:
            return component_total_cost["total_sum"].quantize(Decimal("1.00"))
        return 0

    def __str__(self) -> str:
        return str(self.part_number)

    class Meta:
        verbose_name = "QuotationTechnologyOption"
        verbose_name_plural = "QuotationTechnologyOptions"


class QuotationThirdPartyItem(BaseModel):
    quotation = models.ForeignKey(
        Quotation, on_delete=models.CASCADE, related_name="quotation_third_party_items"
    )
    item_name = models.CharField(max_length=80)
    description = models.TextField()
    unit = models.CharField(max_length=40)
    ps_cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
    )
    selling_cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        null=True,
    )
    quantity = models.IntegerField(default=1)
    comment = models.TextField(max_length=255, blank=True, null=True)

    @property
    def spl(self):
        spl = Decimal(0.00)
        if (self.selling_cost) and (self.ps_cost):
            spl = (self.selling_cost / self.ps_cost) * 100
        return spl.quantize(Decimal("1.00"))

    @staticmethod
    def total_spl(quote_id):
        query = Q(quotation_id=quote_id)
        total_spl = 0
        if QuotationThirdPartyItem.objects.filter(query).exists():
            total_spl = 0
            for item in QuotationThirdPartyItem.objects.filter(query):
                total_spl += (item.selling_cost / item.ps_cost) * 100
            return total_spl
        return total_spl

    @staticmethod
    def total_cost(quote_id):
        queryset = (
            QuotationThirdPartyItem.objects.filter(quotation_id=quote_id)
            .annotate(total_cost=F("selling_cost") * F("quantity"))
            .aggregate(total_sum=Sum("total_cost"))
        )
        if queryset["total_sum"]:
            cost = queryset["total_sum"].quantize(Decimal("1.00"))
            return cost
        return 0

    @property
    def spl(self):
        spl = 0.00
        if self.selling_cost and self.ps_cost:
            spl = (self.selling_cost / self.ps_cost) * 100
        return spl

    def __str__(self) -> str:
        return str(self.item_name)

    class Meta:
        verbose_name = "QuotationThirdPatyItem"
        verbose_name_plural = "QuotationThirdPatyItems"


class QuotationIntroPara(models.Model):
    quotation = models.ForeignKey(
        Quotation, on_delete=models.CASCADE, related_name="quotation_introduction_para"
    )

    technology_type = models.ForeignKey(TechnologyType, on_delete=models.PROTECT)
    intro_para = models.TextField(null=True)

    def __str__(self) -> str:
        return self.intro_para
