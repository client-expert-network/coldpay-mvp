from django.urls import path
# from api.portfolios.views import get_portfolios
from apps.portfolios.views import *

urlpatterns = [
    path("create/", create_portfolio, name="create_portfolio"),
    path("", get_portfolios, name="portfolios_index"),
    path('top/', get_top_portfolios, name='top_portfolios'),
    path('read/<str:portfolio_id>/', portfolio_detail, name='portfolio_detail'),
    path('update/<str:portfolio_id>/', update_portfolio, name='update_portfolio'),
    path('edit/<str:portfolio_id>/', edit_portfolio, name='edit_portfolio'),
    path('delete/<str:portfolio_id>/', delete_portfolio, name='delete_portfolio'),

]