from django.contrib import admin
from apps.portfolios.models import Portfolio, PortfolioImage, PortfolioVideo

admin.site.register(Portfolio)
admin.site.register(PortfolioImage)
admin.site.register(PortfolioVideo)

