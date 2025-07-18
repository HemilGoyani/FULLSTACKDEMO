# Generated by Django 4.1.2 on 2022-11-11 08:32

from decimal import Decimal
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import djmoney.models.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("technologyoptions", "0005_technologyoption_technologysubcomponent_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="Quotation",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True, null=True)),
                ("updated_at", models.DateTimeField(auto_now=True, null=True)),
                ("is_active", models.BooleanField(default=True)),
                (
                    "doc_file",
                    models.FileField(
                        upload_to="quotations/%Y/%m/%d",
                        validators=[
                            django.core.validators.FileExtensionValidator(
                                allowed_extensions=[".doc", ".docx"]
                            )
                        ],
                    ),
                ),
                (
                    "customer_name",
                    models.CharField(max_length=20, verbose_name="Customer Name"),
                ),
                (
                    "customer_position",
                    models.CharField(max_length=20, verbose_name="Customer Position"),
                ),
                (
                    "customer_company_name",
                    models.CharField(max_length=20, verbose_name="Company Name"),
                ),
                (
                    "customer_company_address",
                    models.CharField(max_length=120, verbose_name="Company Address"),
                ),
                (
                    "user_type",
                    models.CharField(
                        choices=[("Distributor", "Distributor"), ("Client", "Client")],
                        max_length=12,
                    ),
                ),
                (
                    "quotation_type",
                    models.CharField(
                        choices=[
                            ("Lump Sum", "Lump Sum"),
                            ("Itemized", "Itemized"),
                            ("Subscription Based", "Subscription Based"),
                        ],
                        max_length=20,
                    ),
                ),
                ("subscription_months", models.CharField(default=1, max_length=10)),
                (
                    "kick_off_fee_currency",
                    djmoney.models.fields.CurrencyField(
                        choices=[("USD", "USD")],
                        default="USD",
                        editable=False,
                        max_length=3,
                    ),
                ),
                (
                    "kick_off_fee",
                    djmoney.models.fields.MoneyField(
                        currency_choices=(("USD", "USD"),),
                        decimal_places=2,
                        default=Decimal("0"),
                        default_currency="USD",
                        max_digits=10,
                    ),
                ),
                (
                    "creator",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="created_quotations",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "reviewer",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="reviewed_quotations",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "technology_type",
                    models.ManyToManyField(
                        related_name="quotations", to="technologyoptions.technologytype"
                    ),
                ),
            ],
            options={
                "verbose_name": "Quotation",
                "verbose_name_plural": "Quotations",
            },
        ),
        migrations.CreateModel(
            name="ThirdPartyItem",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True, null=True)),
                ("updated_at", models.DateTimeField(auto_now=True, null=True)),
                ("is_active", models.BooleanField(default=True)),
                ("item_name", models.CharField(max_length=80, unique=True)),
                (
                    "cost_currency",
                    djmoney.models.fields.CurrencyField(
                        choices=[("USD", "USD")],
                        default="USD",
                        editable=False,
                        max_length=3,
                    ),
                ),
                (
                    "cost",
                    djmoney.models.fields.MoneyField(
                        currency_choices=(("USD", "USD"),),
                        decimal_places=2,
                        default=Decimal("0"),
                        default_currency="USD",
                        max_digits=10,
                    ),
                ),
            ],
            options={
                "verbose_name": "ThirdPartyItem",
                "verbose_name_plural": "ThirdPartyItems",
            },
        ),
        migrations.CreateModel(
            name="QuotationThirdPartyItem",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True, null=True)),
                ("updated_at", models.DateTimeField(auto_now=True, null=True)),
                ("is_active", models.BooleanField(default=True)),
                ("item_name", models.CharField(max_length=80, unique=True)),
                ("quantity", models.IntegerField(default=1)),
                (
                    "cost_currency",
                    djmoney.models.fields.CurrencyField(
                        choices=[("USD", "USD")],
                        default="USD",
                        editable=False,
                        max_length=3,
                    ),
                ),
                (
                    "cost",
                    djmoney.models.fields.MoneyField(
                        currency_choices=(("USD", "USD"),),
                        decimal_places=2,
                        default=Decimal("0"),
                        default_currency="USD",
                        max_digits=10,
                    ),
                ),
                (
                    "quotation",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="quotation_third_party_items",
                        to="quotations.quotation",
                    ),
                ),
            ],
            options={
                "verbose_name": "QuotationThirdPatyItem",
                "verbose_name_plural": "QuotationThirdPatyItems",
            },
        ),
        migrations.CreateModel(
            name="QuotationTechnologyOption",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True, null=True)),
                ("updated_at", models.DateTimeField(auto_now=True, null=True)),
                ("is_active", models.BooleanField(default=True)),
                (
                    "technology_component",
                    models.CharField(
                        choices=[
                            ("1-Hardware", "1-Hardware"),
                            ("2-Setup", "2-Setup"),
                            ("3-Training", "3-Training"),
                            ("4-Software", "4-Software"),
                            ("5-Ongoing", "5-OnGoing"),
                        ],
                        max_length=255,
                    ),
                ),
                ("sub_component", models.CharField(max_length=50)),
                ("description", models.CharField(max_length=200)),
                ("part_number", models.CharField(max_length=80, unique=True)),
                ("quantity", models.IntegerField(default=1)),
                (
                    "cost_currency",
                    djmoney.models.fields.CurrencyField(
                        choices=[("USD", "USD")],
                        default="USD",
                        editable=False,
                        max_length=3,
                    ),
                ),
                (
                    "cost",
                    djmoney.models.fields.MoneyField(
                        currency_choices=(("USD", "USD"),),
                        decimal_places=2,
                        default=Decimal("0"),
                        default_currency="USD",
                        max_digits=10,
                    ),
                ),
                (
                    "quotation",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="quotation_technology_options",
                        to="quotations.quotation",
                    ),
                ),
                (
                    "technology_type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="technologyoptions.technologytype",
                    ),
                ),
            ],
            options={
                "verbose_name": "QuotationTechnologyOption",
                "verbose_name_plural": "QuotationTechnologyOptions",
            },
        ),
    ]
