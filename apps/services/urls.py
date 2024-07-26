from django.urls import path
from .views import *

app_name = "services"

urlpatterns = [
    path("categories/", get_categories, name="get_categories"),
    path("category/<str:category_id>/", get_category_details, name="get_category_details"),
    path("get/all/", get_services, name="get_all_services"),
    path("get/<str:service_id>/", get_service, name="get_service"),
    path("create/", create_service, name="create_service"),
    path("update/<str:service_id>/", update_service, name="update_service"),
    path("delete/<str:service_id>/", delete_service, name="delete_service"),
    path("review/service/<str:service_id>/", get_service_reviews, name="get_services_reviews"),
    path("review/get/<str:review_id>/", get_review, name="get_review"),
    path("review/create/<str:service_id>/", create_review, name="create_review"),
    path("review/update/<str:review_id>/", update_review, name="update_review"),
    path("review/delete/<str:review_id>/", delete_review, name="delete_review"),
    path("comment/review/<str:review_id>/", get_review_comments, name="get_review_comments"),
    path("comment/get/<str:comment_id>/", get_comment, name="get_comment"),
    path("comment/create/<str:review_id>/", create_comment, name="create_comment"),
    path("comment/update/<str:comment_id>/", update_comment, name="update_comment"),
    path("comment/delete/<str:comment_id>/", delete_comment, name="delete_comment"),
    path("order/create/<str:service_id>/", create_order, name="create_order"),
] 
