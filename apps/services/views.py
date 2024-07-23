from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model
from django.forms.models import model_to_dict, inlineformset_factory
from django.contrib import messages
from .models import Category, CategoryDetail, Service, PriceOption, Review, ReviewComment
from .serializers import *
from .forms import *
import json

User = get_user_model()

@require_http_methods(["GET"])
def get_categories(request):
    categories = Category.objects.all()
    serializer = CategorySerializer(categories, many=True)
    return JsonResponse(serializer.data, safe=False)

@require_http_methods(["GET"])
def get_category_details(request, category_id):
    category = Category.objects.get(id=category_id)
    category_details = CategoryDetail.objects.filter(category=category)
    serializer = CategoryDetailSerializer(category_details, many=True)
    return JsonResponse(serializer.data, safe=False)

@require_http_methods(["GET"])
def get_services(request):
    services = Service.objects.all()
    serializer = ServiceSerializer(services, many=True)
    return render(request, "services/service_all.html", {"services": serializer.data})

@require_http_methods(["GET"])
def get_service(request, service_id):
    service = Service.objects.get(id=service_id)
    serializers = ServiceSerializer(service)
    reviews = Review.objects.filter(service=service).select_related("author")
    reviews_with_comments = []
    seller_email = service.seller.email
    for review in reviews:
        comments = ReviewComment.objects.filter(review_id=review.id)
        author_username = review.author.username
        reviews_with_comments.append({"review": review, "comments": comments, "author_username": author_username})
    return render(request, "services/service_detail.html", {
        "service": serializers.data, "reviews": reviews, "reviews_with_comments": reviews_with_comments, "seller_email": seller_email})

@csrf_exempt
@require_http_methods(["GET", "POST"])
@login_required
def create_service(request):
    if request.method == 'POST':
        user = User.objects.get(email=request.user)
        category_detail = CategoryDetail.objects.get(id=request.POST["category_detail"])
        created_service = Service.objects.create(
            seller=user,
            service_name=request.POST["service_name"],
            category_detail=category_detail,
        )
        PriceOption.objects.create(
            service=created_service,
            price=request.POST["price"],
            price_option_name=request.POST["price_option_name"],
            description=request.POST["description"],
        )
        return redirect("services:get_all_services")

    else:
        category_detail = CategoryDetail.objects.all()
    return render(request, "services/create_service.html", {"category_detail": category_detail})

@csrf_exempt
@require_http_methods(["GET", "POST"])
@login_required
def update_service(request, service_id):
    user = User.objects.get(email=request.user)
    service = get_object_or_404(Service, id=service_id, seller=user)
    price_option = get_object_or_404(PriceOption, service=service)
    category_detail = CategoryDetail.objects.all()

    if request.method == 'POST':
        service.service_name = request.POST["service_name"]
        service.seller = user
        service.save()
        price_option.price = request.POST["price"]
        price_option.price_option_name = request.POST["price_option_name"]
        price_option.description = request.POST["description"]
        price_option.save()
        return redirect("services:get_service", service_id=service.id)
        
    else:
        return render(request, "services/update_service.html", {"service": service, "price_option": price_option, "category_detail": category_detail})

@require_http_methods(["GET", "POST", "DELETE"])
@login_required
def delete_service(request, service_id):
    user = User.objects.get(email=request.user)
    service = get_object_or_404(Service, id=service_id)
    if service.seller != user:
        # 메시지가 안 뜸...
        messages.error(request, "You are not the owner of this service.")
        return redirect("services:get_all_services")
    # 메시지가 안 뜨는 문제
    messages.success(request, "Service deleted successfully.")
    service.delete()
    return redirect("services:get_all_services")


@require_http_methods(["GET"])
def get_service_reviews(request, service_id):
    service = Service.objects.get(id=service_id)
    reviews = Review.objects.filter(service=service)
    serializer = ReviewSerializer(reviews, many=True)
    return JsonResponse(serializer.data, safe=False)

@require_http_methods(["GET"])
def get_review(request, review_id):
    review = Review.objects.get(id=review_id)
    serializer = ReviewSerializer(review)
    return JsonResponse(serializer.data, safe=False)

@csrf_exempt
@require_http_methods(["GET", "POST"])
@login_required
def create_review(request, service_id):
    if request.method == 'POST':
        review_form = CreateReviewForm(request.POST)
        if review_form.is_valid():
            user = User.objects.get(email=request.user)
            service = get_object_or_404(Service, id=service_id)
            created_review = Review.objects.create(
                service=service,
                author=user,
                content=review_form.cleaned_data["content"],
            )
            return redirect("services:get_service", service_id=service.id)
    else:
        service = get_object_or_404(Service, id=service_id)
        review_form = CreateReviewForm()
    return render(request, "services/create_review.html", {"review_form": review_form, "service": service})

@csrf_exempt   
@require_http_methods(["GET", "POST"])
@login_required
def update_review(request, review_id):
    user = User.objects.get(email=request.user)
    review = get_object_or_404(Review, id=review_id, author=user)
    
    if request.method == 'POST':
        review_form = CreateReviewForm(request.POST, instance=review)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.author = user
            review.save()
            return redirect("get_service", service_id=review.service.id)
    else:
        review_form = CreateReviewForm(instance=review)
    return render(request, "services/update_review.html", {"review_form": review_form, "review": review})

@require_http_methods(["GET", "POST"])
@login_required
def delete_review(request, review_id):
    user = User.objects.get(email=request.user)
    review = Review.objects.get(id=review_id)
    if review.author != user:
        return JsonResponse({"message": "You are not the owner of this review"}, safe=False, status=403)
    review.delete()
    return redirect("services:get_service", service_id=review.service.id)


@require_http_methods(["GET"])
def get_review_comments(request, review_id):
    review = Review.objects.get(id=review_id)
    comments = ReviewComment.objects.filter(review=review)
    serializer = ReviewCommentSerializer(comments, many=True)
    return JsonResponse(serializer.data, safe=False)

@require_http_methods(["GET"])
def get_comment(request, comment_id):
    comment = ReviewComment.objects.get(id=comment_id)
    serializer = ReviewCommentSerializer(comment)
    return JsonResponse(serializer.data, safe=False)

@csrf_exempt
@require_http_methods(["GET", "POST"])
@login_required
def create_comment(request, review_id):
    if request.method == 'POST':
        comment_form = CreateReviewCommentForm(request.POST)
        if comment_form.is_valid():
            user = User.objects.get(email=request.user)
            review = Review.objects.get(id=review_id)
            ReviewComment.objects.create(
                author=user,
                review=review,
                content=comment_form.cleaned_data["content"],
            )
            return redirect("get_service", service_id=review.service.id)
    else:
        comment_form = CreateReviewCommentForm()
    return render(request, "services/create_comment.html", {"comment_form": comment_form})
    
@csrf_exempt
@require_http_methods(["GET", "POST"])
@login_required
def update_comment(request, comment_id):
    user = User.objects.get(email=request.user)
    comment = ReviewComment.objects.get(id=comment_id)
    if comment.author != user:
        return JsonResponse({"message": "You are not the owner of this comment"}, safe=False, status=403)
    if request.method == 'POST':
        comment_form = CreateReviewCommentForm(request.POST, instance=comment)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.author = user
            comment.save()
            return redirect("get_service", service_id=comment.review.service.id)        
    else:
        comment_form = CreateReviewCommentForm(instance=comment)
    return render(request, "services/update_comment.html", {"comment_form": comment_form, "comment": comment})

@csrf_exempt
@require_http_methods(["GET", "POST"])
@login_required
def delete_comment(request, comment_id):
    user = User.objects.get(email=request.user)
    comment = ReviewComment.objects.get(id=comment_id)
    if comment.author != user:
        return JsonResponse({"message": "You are not the owner of this comment"}, safe=False, status=403)
    comment.delete()
    return redirect("get_service", service_id=comment.review.service.id)