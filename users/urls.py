from django.urls import path

from . import views

app_name = "users"

urlpatterns = [
    path("", views.ListCreateUserView.as_view(), name="list_create"),
    path("<int:pk>/", views.UserDetailView.as_view(), name="detail")
]
