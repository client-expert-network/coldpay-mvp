from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import F
from django.http import HttpResponseForbidden, JsonResponse
from django.views.decorators.http import require_POST, require_GET, require_http_methods
from django.contrib.auth.decorators import login_required
import json
from .forms import PortfolioForm
from apps.portfolios.models import Portfolio, PortfolioImage, PortfolioVideo
from django.contrib.auth import get_user_model

User = get_user_model()


@login_required
@require_http_methods(["GET", "POST"])
def create_portfolio(request):

    if not request.user.is_expert:
        return HttpResponseForbidden({"error": "User is not a expert"})

    if request.method == "POST":
        form = PortfolioForm(request.POST, request.FILES)
        if form.is_valid():
            portfolio = form.save(commit=False)
            portfolio.expert = request.user
            portfolio.save()

            # 이미지와 비디오 처리
            images = request.FILES.getlist("images")
            videos = request.FILES.getlist("videos")
            for image in images:
                PortfolioImage.objects.create(portfolio=portfolio, image=image)
            for video in videos:
                PortfolioVideo.objects.create(portfolio=portfolio, video=video)

            # 성공적으로 생성된 경우, 포트폴리오 상세 페이지로 
            return render(request, "portfolios/portfolio_detail.html", {"portfolio": portfolio})
    else:
        form = PortfolioForm()
    return render(request, "portfolios/create_portfolio.html", {"form": form})


@require_http_methods(["GET"])
def get_portfolios(request):
    page = request.GET.get("page", 1)
    portfolios = Portfolio.objects.all().order_by("-created_at")
    paginator = Paginator(portfolios, 10)
    paginator_boards = paginator.get_page(page)

    return render(
        request,
        "portfolios/portfolios.html",
        {"portfolios": paginator_boards},
    )



@require_http_methods(["GET"])
def get_top_portfolios(request):
    top_portfolios = Portfolio.objects.annotate(
        popularity=F("show") + 5 * F("like")
    ).order_by("-popularity")[0:5]
    return render(
        request,
        "portfolios/partial_portfolio_list.html",
        {"portfolios": top_portfolios},
    )



@require_http_methods(["GET", "POST"])
def portfolio_detail(request, portfolio_id):
    # 특정 Portfolio 객체를 가져옴
    portfolio = get_object_or_404(Portfolio, pk=portfolio_id)

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
        return JsonResponse({"likes": portfolio.like, "shows": portfolio.show})
    else:
        # 사용자가 방문시 조회수 증가를 위한 세션 키 생성
        session_key = f"shown_{portfolio_id}"
        if not request.session.get(session_key):
            # 세션 키가 없다면, 사용자가 이 포트폴리오를 처음 방문한 것임
            portfolio.show += 1
            portfolio.save()
            request.session[session_key] = True  # 세션에 키 설정하여 재방문 추적

        return render(
            request, "portfolios/portfolio_detail.html", {"portfolio": portfolio}
        )



@require_http_methods(["GET", "POST"])  # 게시물 수정 페이지
def update_portfolio(request, portfolio_id):
    portfolio = get_object_or_404(Portfolio, pk=portfolio_id)
    
    # 현재 접근한 user가 Portfolio의 작성자와 동일한지 확인
    if portfolio.expert != request.user:
        return HttpResponseForbidden("편집 권한이 없습니다.")
    
    if request.method == "POST":
        form = PortfolioForm(request.POST, instance=portfolio)
        if form.is_valid():
            portfolio = form.save()
            return redirect("portfolios/portfolio_detail", portfolio_id=portfolio.id)
    else:
        form = PortfolioForm(instance=portfolio)
        
    return render(request, 'portfolios/update_portfolio.html', {'form': form, 'portfolio': portfolio})



@require_http_methods(["POST"])  # 게시물 수정 후 저장역할
def edit_portfolio(request, portfolio_id):
    portfolio = get_object_or_404(Portfolio, pk=portfolio_id)

    portfolio.title = request.POST.get("title")
    portfolio.content = request.POST.get("content")
    portfolio.price = request.POST.get("price")
    portfolio.portfolio_start = request.POST.get("portfolio_start")
    portfolio.portfolio_end = request.POST.get("portfolio_end")
    portfolio.save()

    return redirect("/portfolios/")


@require_http_methods(["POST"])  # 게시물 DELETE
def delete_portfolio(request, portfolio_id):
    portfolio = get_object_or_404(Portfolio, pk=portfolio_id)

    # 작성자와 현재 user가 일치하는지 확인
    if portfolio.expert != request.user:
        return HttpResponseForbidden("삭제 권한이 없습니다.")
        
    if request.method == "POST":
        portfolio.delete()
        return redirect("/portfolios/")  # Django의 redirect 함수 사용
    