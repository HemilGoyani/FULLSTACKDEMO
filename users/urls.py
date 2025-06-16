from django.urls import path

from users.views import UserCreateView
from users.views import UserDeleteView
from users.views import UserListView
from users.views import UserUpdateView

app_name = "users"
urlpatterns = [
    path("", UserListView.as_view(), name="users"),
    path("add/", UserCreateView.as_view(), name="user-add"),
    path("update/<int:pk>/", UserUpdateView.as_view(), name="user-update"),
    path("delete/<int:pk>/", UserDeleteView.as_view(), name="user-delete"),
]
