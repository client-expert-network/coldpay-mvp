from django.shortcuts import render, get_object_or_404, redirect
from apps.portfolios.models import Portfolio, PortfolioImage, PortfolioVideo
from django.core.paginator import Paginator
from django.db.models import F
from django.http import HttpResponseForbidden, JsonResponse
from django.views.decorators.http import require_POST, require_GET, require_http_methods
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import json
from .forms import PortfolioForm


@login_required 
@csrf_exempt
@require_POST  
def create_portfolio(request):
    # 전문가인지 확인
    if not request.user.is_expert:
        return HttpResponseForbidden({"error": "User is not a expert"})

    expert = request.user

    # request.POST와 request.FILES를 사용하여 데이터 처리
    portfolio = Portfolio.objects.create(
        expert=expert,
        title=request.POST.get("title"),
        content=request.POST.get("content"),
        price=request.POST.get("price"),
        portfolio_start=request.POST.get("portfolio_start"),
        portfolio_end=request.POST.get("portfolio_end"),
    )

    # 이미지와 비디오 처리를 위해 request.FILES.getlist 사용
    images = request.FILES.getlist("images")
    videos = request.FILES.getlist("videos")
    for image in images:
        PortfolioImage.objects.create(portfolio=portfolio, image=image)
    for video in videos:
        PortfolioVideo.objects.create(portfolio=portfolio, video=video)

    # 성공적으로 생성된 경우, 포트폴리오 상세 페이지로 렌더링
    return render(request, "portfolios/portfolio_detail.html", {"portfolio": portfolio})


@csrf_exempt
@require_GET  # 게시물 READ
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


@csrf_exempt
@require_GET  # HOT 게시물_필터링
def get_top_portfolios(request):
    top_portfolios = Portfolio.objects.annotate(
        popularity=F("show") + 5 * F("like")
    ).order_by("-popularity")[0:5]
    return render(
        request,
        "portfolios/partial_portfolio_list.html",
        {"portfolios": top_portfolios},
    )

    # 게시물 READ_상세보기


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


def update_portfolio(request, portfolio_id):
    portfolio = get_object_or_404(Portfolio, pk=portfolio_id)
    if request.method == "POST":
        form = PortfolioForm(request.POST, instance=portfolio)
        if form.is_valid():
            portfolio = form.save()
            return redirect("portfolios/portfolio_detail", portfolio_id=portfolio.id)
    else:
        form = PortfolioForm(instance=portfolio)
    return render(request, 'portfolios/update_portfolio.html', {'form': form, 'portfolio': portfolio})



@require_http_methods(["POST", "PUT"])  # 게시물 UPDATE
def edit_portfolio(request, portfolio_id):
    portfolio = get_object_or_404(Portfolio, pk=portfolio_id)

    # PUT 요청 처리를 위한 데이터 파싱
    if request.method == "PUT":
        data = json.loads(request.body)
    else:
        data = request.POST

    portfolio.title = data.get("title")
    portfolio.content = data.get("content")
    portfolio.price = data.get("price")
    portfolio.portfolio_start = data.get("portfolio_start")
    portfolio.portfolio_end = data.get("portfolio_end")
    portfolio.save()

    return redirect("/portfolios/")
    # return render(request, 'portfolios/portfolio_detail.html', {'portfolio': portfolio})


@require_http_methods(["POST", "DELETE"])  # 게시물 DELETE
def delete_portfolio(request, portfolio_id):
    portfolio = get_object_or_404(Portfolio, pk=portfolio_id)

    # 요청자가 게시물의 작성자와 일치하는지 확인
    # if portfolio.seller != request.user.id:
    #     return Response({"message": "게시물을 삭제할 권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)

    portfolio.delete()
    # 리다이렉트 URL 설정
    return redirect("/portfolios/")  # Django의 redirect 함수 사용
