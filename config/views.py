from django.shortcuts import render
from django.views.decorators.clickjacking import xframe_options_exempt
from django.views.decorators.http import require_http_methods
from apps.portfolios.models import Portfolio
from django.core.paginator import Paginator

@xframe_options_exempt
@require_http_methods(["GET"])
def home(request):
    page = request.GET.get("page", 1)
    portfolios = Portfolio.objects.all().order_by("-created_at")
    paginator = Paginator(portfolios, 10)
    paginator_boards = paginator.get_page(page)

    return render(
        request,
        "home.html",
        {"portfolios": paginator_boards},)
    
    