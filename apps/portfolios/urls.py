from django.urls import path

# from api.portfolios.views import get_portfolios
from .views import *

urlpatterns = [
    path("portfolios/create/", create_portfolio, name="create_portfolio"),
    path("portfolios/", get_portfolios, name="portfolios_index"),
    path("portfolios/top/", get_top_portfolios, name="top_portfolios"),
    path("portfolios/read/<str:portfolio_id>/", portfolio_detail, name="portfolio_detail"),
    path("portfolios/update/<str:portfolio_id>/", update_portfolio, name="update_portfolio"),
    path("portfolios/delete/<str:portfolio_id>/", delete_portfolio, name="delete_portfolio"),
    path("portfolios/test/", test_portfolios, name="test_portfolios"),
    path("portfolios/test/create/", create_test, name="create_test"),
    path("portfolios/test/detail/<str:portfolio_id>/", detail_test, name="test_detail"),
    path("portfolios/test/update/<str:portfolio_id>/", update_test, name="update_test"),
    path("portfolios/test/delete/<str:portfolio_id>/", delete_test, name="delete_test"),
]