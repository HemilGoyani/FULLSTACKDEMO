from django.contrib import admin

from quotations.models import Client
from quotations.models import Quotation
from quotations.models import QuotationIntroPara
from quotations.models import QuotationTechnologyOption
from quotations.models import QuotationThirdPartyItem
from quotations.models import ThirdPartyItem

# Register your models here.

admin.site.register(Quotation)
# admin.site.register(QuotationTechnologyOption)
admin.site.register(QuotationThirdPartyItem)
admin.site.register(ThirdPartyItem)
admin.site.register(QuotationIntroPara)
admin.site.register(Client)


class QuotationTechnologyOptionAdmin(admin.ModelAdmin):

    list_filter = (
        "quotation",
        "technology_type",
        "technology_component",
        "sub_component",
        "part_number",
    )
    list_display = (
        "quotation",
        "technology_type",
        "technology_component",
        "sub_component",
        "part_number",
    )
    search_fields = (
        "quotation",
        "technology_type",
        "technology_component",
        "sub_component",
        "part_number",
    )
    ordering = ("quotation",)
    filter_horizontal = ()


admin.site.register(QuotationTechnologyOption, QuotationTechnologyOptionAdmin)
