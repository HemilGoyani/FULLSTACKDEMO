from backend.models import BaseModel
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _


class UNIT_CHOICES(models.TextChoices):
    PERITEM = "Per Item", _("Per Item")
    PERIMXUNIT = "Per IMX Unit", _("Per IMX Unit")
    PERHOUR = "Per Hour", _("Per Hour")
    PERLICENCEYEAR = "Per Licence / Year", _("Per Licence / Year")
    PERPROJECT = "Per Project", _("Per Project")
    PERSOFTWARE = "Per Software", _("Per Software")
    PERPOINTMONTH = "Per Point/ Month", _("Per Point/Month")
    PERGATEWAY = "Per Gateway", _("Per Gateway")


class COMPONENT_CHOICES(models.TextChoices):
    HARDWARE = "1-Hardware", _("Hardware")
    SETUP = "2-Setup", _("Setup")
    TRAINING = "3-Training", _("Training")
    SOFTWARE = "4-Software", _("Software")
    ONGOING = "5-Ongoing", _("Analytics and Reporting")


class TechnologyType(BaseModel):
    type = models.CharField(
        max_length=255,
        null=True,
        blank=False,
        unique=True,
        verbose_name="Technology / Service",
    )
    image = models.ImageField(upload_to="TechnologyTypeImages/", null=True, blank=True)
    intro_para = models.TextField(null=True, verbose_name="Introduction Paragraph")

    def __str__(self):
        return str(self.type)


class TechnologySubComponent(BaseModel):
    technology_type = models.ForeignKey(
        TechnologyType,
        related_name="technology_sub_components",
        on_delete=models.PROTECT,
        verbose_name="Technology / Service",
    )
    technology_component = models.CharField(
        choices=COMPONENT_CHOICES.choices,
        verbose_name="Technology / Service Component",
        max_length=255,
    )
    sublist_item_name = models.CharField(
        max_length=255,
        verbose_name="Technology / Service Sub Component",
    )

    def __str__(self) -> str:
        return str(self.sublist_item_name)

    class Meta:
        verbose_name = "TechnologySubComponent"
        verbose_name_plural = "TechnologySubComponents"


class TechnologyOption(BaseModel):
    ONEOFF = "one off"
    ONGOING = "on going"

    STATUSES = (
        (ONEOFF, "One Off"),
        (ONGOING, "On Going"),
    )
    technology_type = models.ForeignKey(
        TechnologyType,
        on_delete=models.PROTECT,
        related_name="technology_options",
        null=True,
        blank=False,
        verbose_name="Technology / Service",
    )
    technology_component = models.CharField(
        choices=COMPONENT_CHOICES.choices,
        max_length=255,
        null=True,
        blank=False,
        verbose_name="Technology / Service Component",
    )
    technology_sub_component = models.ForeignKey(
        TechnologySubComponent,
        on_delete=models.PROTECT,
        related_name="technology_options",
        verbose_name="Technology / Service Sub Component",
    )
    part_number = models.CharField(max_length=255, null=True, blank=False)
    description = models.TextField(max_length=1000, null=True, blank=False)
    unit = models.CharField(
        max_length=255, null=True, blank=False, choices=UNIT_CHOICES.choices
    )
    category = models.CharField(choices=STATUSES, max_length=30, null=True, blank=False)
    ps_cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
    )
    distribution_cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
    )
    end_user_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return str(self.technology_component)

    def clean(self):
        if self.distribution_cost is None or self.ps_cost >= self.distribution_cost:
            raise ValidationError(_("Distribution cost must be greater than PS cost."))

        if self.end_user_cost is None or self.ps_cost >= self.end_user_cost:
            raise ValidationError(_("End user cost must be greater than PS cost."))
