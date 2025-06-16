from django.urls import path

from technologyoptions.views import AddTechnologyOptionView
from technologyoptions.views import AddTechnoTypeView
from technologyoptions.views import BulkUploadTechnologyOptionsView
from technologyoptions.views import TechnologyOptionDeleteView
from technologyoptions.views import TechnologyOptionListView
from technologyoptions.views import TechnologySubcomponentCreateView
from technologyoptions.views import TechnologySubcomponentDeleteView
from technologyoptions.views import TechnologySubcomponentUpdateView
from technologyoptions.views import TechnologyTypeDeleteView
from technologyoptions.views import UpdateTechnologyOptionView
from technologyoptions.views import UpdateTechnoTypeView
from technologyoptions.views import bulk_upload_template
from technologyoptions.views import technology_sub_component_list

app_name = "technologyoptions"

urlpatterns = [
    path("", TechnologyOptionListView.as_view(), name="product-or-part-numbers"),
    path(
        "add-product-or-part-number/",
        AddTechnologyOptionView.as_view(),
        name="add-product-or-part-number",
    ),
    path(
        "update-product-or-part-number/<int:pk>/",
        UpdateTechnologyOptionView.as_view(),
        name="update-product-or-part-number",
    ),
    path(
        "delete-product-or-part-number/<int:pk>/",
        TechnologyOptionDeleteView.as_view(),
        name="delete-product-or-part-number",
    ),
    path(
        "add-technology-or-service/",
        AddTechnoTypeView.as_view(),
        name="add-techno-type",
    ),
    path(
        "update-technology-or-service/<int:pk>/",
        UpdateTechnoTypeView.as_view(),
        name="update-techno-type",
    ),
    path(
        "delete-technology-or-service/<int:pk>/",
        TechnologyTypeDeleteView.as_view(),
        name="delete-techno-type",
    ),
    path(
        "bulk-upload-products-or-part-numbers/",
        BulkUploadTechnologyOptionsView.as_view(),
        name="bulk-upload-products-or-part-numbers",
    ),
    path(
        "add-product-or-part-number/technology-sub-component-list/<str:technology_type>/<str:technology_component>/",
        technology_sub_component_list,
        name="add-technology-sub-component-list",
    ),
    path(
        "update-product-or-part-number/<int:pk>/technology-sub-component-list/<str:technology_type>/<str:technology_component>/",
        technology_sub_component_list,
        name="update-technology-sub-component-list",
    ),
    path(
        "download-bulk-upload-template/",
        bulk_upload_template,
        name="download-bulk-upload-template",
    ),
    path(
        "technology-or-service-sub-component/add/",
        TechnologySubcomponentCreateView.as_view(),
        name="add-technology-subcomponent",
    ),
    path(
        "technology-or-service-sub-component/update/<int:pk>/",
        TechnologySubcomponentUpdateView.as_view(),
        name="update-technology-subcomponent",
    ),
    path(
        "technology-or-service-sub-component/delete/<int:pk>/",
        TechnologySubcomponentDeleteView.as_view(),
        name="delete-technology-subcomponent",
    ),
]
