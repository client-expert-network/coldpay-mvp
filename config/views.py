from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.clickjacking import xframe_options_exempt
from django.views.decorators.http import require_http_methods
from django.urls import reverse
from django.http import HttpResponseRedirect
from apps.portfolios.models import Portfolio
from django.core.paginator import Paginator


@xframe_options_exempt
@require_http_methods(["GET"])
def home(request):
    page = request.GET.get("page", 1)
    portfolios = Portfolio.objects.all().order_by("-created_at")
    paginator = Paginator(portfolios, 8)
    paginator_boards = paginator.get_page(page)

    return render(
        request,
        "home.html",
        {"portfolios": paginator_boards, "write": False},)
    
    

@xframe_options_exempt
@require_http_methods(["GET", "POST"])  
def main_portfolio_detail(request, portfolio_id):    # 게시물 READ
    portfolio = get_object_or_404(Portfolio, pk=portfolio_id)
    other_portfolios = Portfolio.objects.filter(expert=portfolio.expert).exclude(id=portfolio.id)
    other_portfolio = get_object_or_404(Portfolio, pk=portfolio_id)
    if request.method == "POST":
        # 사용자가 이미 'like'를 눌렀는지 확인하는 세션 키 생성
        session_key = f"liked_{portfolio_id}"
        if request.session.get(session_key):
            # 이미 'like'를 눌렀다면, 'like'를 하나 줄임
            portfolio.like -= 1
            request.session[session_key] = False
        else:
            # 'like'를 누르지 않았다면, 'like'를 하나 늘림
            portfolio.like += 1
            request.session[session_key] = True
        portfolio.save()
        return HttpResponseRedirect(reverse('portfolio_detail', args=[portfolio_id]))
    
    else:
        # 사용자가 방문시 조회수 증가를 위한 세션 키 생성
        session_key = f"shown_{portfolio_id}"
        if not request.session.get(session_key):
            # 세션 키가 없다면, 사용자가 이 포트폴리오를 처음 방문한 것
            portfolio.show += 1
            portfolio.save()
            request.session[session_key] = True  # 세션에 키 설정하여 재방문 추적

        return render(request, 'home.html', 
        {'portfolio': portfolio,
        'other_portfolios': other_portfolios,
        'other_portfolio': other_portfolio,})