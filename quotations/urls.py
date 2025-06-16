from django.urls import path

from quotations.views import AddManualItemsView
from quotations.views import ChooseQuotationTypeView
from quotations.views import ChooseTechnologyTypeView
from quotations.views import ChooseUseTypeView
from quotations.views import DeleteQuotationView
from quotations.views import QuotationCreateView
from quotations.views import QuotationIntroParaView
from quotations.views import QuotationListView
from quotations.views import QuotationScopeOfWorksView
from quotations.views import QuotationSummaryView
from quotations.views import QuotationTermsAndConditionView
from quotations.views import QuotationUpdateView
from quotations.views import TechnologyOptionsSelectionView
# from quotations.views import download_quotation_docx
# from quotations.views import download_quotation_pdf
from quotations.views import get_part_numbers_from_sub_component
from quotations.views import quotation_details
from quotations.views import quotation_update_status

app_name = "quotations"
urlpatterns = [
    path("", QuotationListView.as_view(), name="quotations"),
    # # path("get_docx",GetQuotation.as_view(), name="get-docx")
    # path("get_docx", TestDocument, name="get-docx"),
    path(
        "create/",
        QuotationCreateView.as_view(),
        name="create",
    ),
    path(
        "<int:pk>/edit/",
        QuotationUpdateView.as_view(),
        name="edit",
    ),
    path(
        "<int:pk>/delete/",
        DeleteQuotationView.as_view(),
        name="delete",
    ),
    path(
        "<int:pk>/choose-technology-type/",
        ChooseTechnologyTypeView.as_view(),
        name="choose-technology-type",
    ),
    path(
        "<int:pk>/choose-user-type-distributor-or-client/",
        ChooseUseTypeView.as_view(),
        name="choose-user-type-distributor-or-client",
    ),
    path(
        "<int:pk>/quotation-details/",
        quotation_details,
        name="quotation-details",
    ),
    path(
        "<int:pk>/add-other-items/",
        AddManualItemsView.as_view(),
        name="add-manual-items",
    ),
    path(
        "<int:pk>/choose-quotation-type/",
        ChooseQuotationTypeView.as_view(),
        name="choose-quotation-type",
    ),
    path(
        "<int:pk>/intro-para/",
        QuotationIntroParaView.as_view(),
        name="quotation-intro-para",
    ),
    path(
        "<int:pk>/terms-and-conditions/",
        QuotationTermsAndConditionView.as_view(),
        name="quotation-terms-and-conditions",
    ),
    path(
        "<int:pk>/scope-of-works/",
        QuotationScopeOfWorksView.as_view(),
        name="quotation-scope-of-works",
    ),
    path(
        "<int:pk>/quotation-summary/",
        QuotationSummaryView.as_view(),
        name="quotation-summary",
    ),
    path(
        "<int:id>/quotation-update-status/",
        quotation_update_status,
        name="quotation-update-status",
    ),
    path(
        "<int:pk>/ajax-part-numbers/",
        get_part_numbers_from_sub_component,
        name="ajax-part-numbers",
    ),
    # path(
    #     "<int:pk>/download_quotation_pdf/",
    #     download_quotation_pdf,
    #     name="download-quotation-pdf",
    # ),
    # path(
    #     "<int:pk>/download_quotation_docx/",
    #     download_quotation_docx,
    #     name="download-quotation-docx",
    # ),
    path(
        "<int:pk>/<str:component>/",
        TechnologyOptionsSelectionView.as_view(),
        name="tech-options-selection",
    ),
]
