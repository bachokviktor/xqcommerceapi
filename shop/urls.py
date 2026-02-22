from django.urls import path

from . import views


app_name = "shop"

urlpatterns = [
    path("", views.ListCreateItemView.as_view(), name="list_items"),
    path("item/<int:pk>/", views.RetrieveUpdateItemView.as_view(), name="retrieve_item"),
    path("item/<int:pk>/review/", views.CreateReviewView.as_view(), name="create_review"),
    path("item/<int:pk>/review/<int:r_pk>/", views.UpdateDestroyReviewView.as_view(), name="update_review"),
    path("item/<int:pk>/cart/", views.ManageCartView.as_view(), name="manage_cart"),
]
