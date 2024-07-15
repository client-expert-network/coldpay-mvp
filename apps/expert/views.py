from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.shortcuts import render
from django.http import HttpResponse
from .forms import ExpertConversionForm
from .models import *


@login_required
@require_http_methods(["GET", "POST"])
def convert_to_expert(request):
    if hasattr(request.user, "expert"):
        return HttpResponse("이미 전문가 전환 신청을 하셨습니다.")

    form = ExpertConversionForm(request.POST or None, request.FILES or None)

    if request.method == "POST":

        if form.is_valid():
            expert = form.save(commit=False)
            expert.user = request.user
            expert.save()
            return HttpResponse(
                "전문가 전환 신청이 완료되었습니다. 관리자 승인 후 전환됩니다."
            )

    context = {"form": form}
    return render(request, "expert/convert_to_expert.html", context)


@login_required
def expert_approval(request, expert_id):
    if not request.user.is_staff:
        return HttpResponse("권한이 없습니다.", status=403)

    expert = Expert.objects.get(id=expert_id)
    expert.is_approved = True
    expert.save()

    user = expert.user
    user.is_expert = True
    user.save()

    return HttpResponse("전문가 승인이 완료되었습니다.")
