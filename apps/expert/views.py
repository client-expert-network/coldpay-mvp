from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.shortcuts import render
from django.http import HttpResponse
from .forms import ExpertConversionForm
from .models import Expert
from django.shortcuts import get_object_or_404
from .models import ApplyExpert

@login_required
@require_http_methods(["GET", "POST"])
def convert_to_expert(request):
    if hasattr(request.user, 'applyexpert'):
        return HttpResponse("이미 전문가 전환 신청을 하셨습니다.")

    form = ExpertConversionForm(request.POST or None, request.FILES or None)

    if request.method == "POST":

        if form.is_valid():
            expert = form.save(commit=False)
            expert.user = request.user
            expert.save()
            return HttpResponse("전문가 전환 신청이 완료되었습니다. 관리자 승인 후 전환됩니다.")
    else:
        # 지원서 작성 form - 수정 필요
        form = ExpertConversionForm()
    
    context = {"form": form}
    # 임시 주소로 return, html 작성 필요
    return render(request, "expert/convert_to_expert.html", context)


# 지원서를 승인
@login_required
def expert_approval(request, apply_id):
    if not request.user.is_staff:
        return HttpResponse("권한이 없습니다.", status=403)

    # ApplyExpert 객체 - 일종의 지원서
    # 지원서
    apply_expert = get_object_or_404(ApplyExpert, id=apply_id)
    # 지원서의 유저를 expert로 변경
    user = apply_expert.user
    user.is_expert = True
    user.save()

    # 지원서 승인 상태를 변경
    apply_expert.approved = True
    apply_expert.save()

    return HttpResponse("전문가 승인이 완료되었습니다.")
