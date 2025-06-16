from django.urls import path

from settings.views import TermsAndConditionView
from settings.views import update_terms_and_conditions
from settings.views import ManageManualItemsView
from settings.views import UpdateManualItemView
from settings.views import DeleteManualItemView

app_name = "settings"

urlpatterns = [
    path("", TermsAndConditionView.as_view(), name="settings"),
    path(
        "update-terms-and-conditions/",
        update_terms_and_conditions,
        name="update-terms-and-conditions",
    ),
    path(
        "manage-other-items/",
        ManageManualItemsView.as_view(),
        name="manage-manual-items",
    ),
    path(
        "update-other-item/<int:pk>/",
        UpdateManualItemView.as_view(),
        name="update-manual-item",
    ),
    path(
        "delete-other-item/<int:pk>/",
        DeleteManualItemView.as_view(),
        name="delete-manual-item",
    ),
]
