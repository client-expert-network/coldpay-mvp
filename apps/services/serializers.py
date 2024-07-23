from rest_framework import serializers
from .models import Category, CategoryDetail, Service, PriceOption, Review, ReviewComment
from django.contrib.auth import get_user_model

User = get_user_model()

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"

class CategoryDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryDetail
        fields = "__all__"

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

class ServiceSerializer(serializers.ModelSerializer):
    price_options = serializers.SerializerMethodField()
    category_detail_name = serializers.CharField(source="category_detail.name", read_only=True)
    seller_name = serializers.CharField(source="seller.username", read_only=True)
    
    class Meta:
        model = Service
        fields = "__all__"

    def get_price_options(self, obj):
        price_options = PriceOption.objects.filter(service=obj)
        serializer = PriceOptionSerializer(price_options, many=True)
        return serializer.data

class PriceOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PriceOption
        fields = "__all__"

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = "__all__"

class ReviewCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewComment
        fields = "__all__"

class ServiceCreateSerializer(serializers.Serializer):
    service_name = serializers.CharField(max_length=255)
    category_detail = serializers.CharField(max_length=255)
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    price_option_name = serializers.CharField(max_length=255)
    description = serializers.CharField()

class ReviewCreateSerializer(serializers.Serializer):
    content = serializers.CharField()

class ReviewCommentCreateSerializer(serializers.Serializer):
    content = serializers.CharField()