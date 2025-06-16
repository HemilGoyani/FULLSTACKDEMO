from django.contrib import admin

from technologyoptions.models import TechnologyOption
from technologyoptions.models import TechnologySubComponent
from technologyoptions.models import TechnologyType

admin.site.register(TechnologyOption)
admin.site.register(TechnologyType)
# admin.site.register(TechnologySubComponent)


class TechnologySubComponentAdmin(admin.ModelAdmin):

    list_filter = ("technology_type", "technology_component", "sublist_item_name")
    list_display = ("technology_type", "technology_component", "sublist_item_name")
    search_fields = ("technology_type", "technology_component", "sublist_item_name")
    ordering = ("technology_type",)
    filter_horizontal = ()


# Now register the new TechnologySubComponentAdmin...
admin.site.register(TechnologySubComponent, TechnologySubComponentAdmin)
